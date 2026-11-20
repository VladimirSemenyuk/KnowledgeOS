#!/usr/bin/env python3
"""Автопостинг в Telegram-канал: посты недели встают в штатную отложенную публикацию канала.

Работает от аккаунта автора (Telethon), сервер не нужен: скрипт ставит сообщения
в «Отложенные» канала, дальше публикует сам Telegram. Очередь видна и правится в приложении.

Запуск из корня KnowledgeOS через окружение `.venv`:

    R=Posts/render
    $R/.venv/bin/python $R/tg.py login                       # один раз, в своём терминале: телефон и код
    $R/.venv/bin/python $R/tg.py plan 2026-11-30-week-2      # что встанет в очередь, ничего не отправляет
    $R/.venv/bin/python $R/tg.py send 2026-11-30-week-2      # поставить в отложенные
    $R/.venv/bin/python $R/tg.py update 2026-11-30-week-2 --only "Вт 1"  # заменить пост версией из _index.md
    $R/.venv/bin/python $R/tg.py delete 2026-11-30-week-2 --only "Вт 1"  # убрать пост из отложенных
    $R/.venv/bin/python $R/tg.py queue                       # что уже стоит в отложенных канала

Пост недели находится в отложенных по времени (из таблицы или ритма) или по первым 80 знакам текста.
`send` повторно не ставит найденный пост. `update` удаляет найденные сообщения поста и ставит заново:
так меняются текст, картинки и время. Время берётся из колонки «Время»; если она пуста, `update`
оставляет время поста в очереди (могли выставить в приложении), а не ставит 10:00 по ритму. Если поменялись и время, и начало текста, старый пост
не найдётся — сначала `delete` до правки или удалить вручную в приложении.
`update` и `delete` показывают, что сделают, и спрашивают подтверждение; `--yes` — без вопроса.
`--only "Вт 1"` — только один день.

Откуда что берётся в `_index.md` недели:
- пост — раздел `### <День> <число>. LinkedIn и Telegram. …` (или `. Telegram. …`);
- текст — первый блок ``` в разделе, переносится дословно, без разметки;
- картинка — первая `![[…]]` в разделе; если её имя кончается на `-01.png`,
  уходит альбом из всех `-NN.png` рядом (карусель). Строка `Telegram: нет картинки` — пост без картинки;
- видео — строка `Telegram: видео ~/Movies/reels-1-final.mp4`: уходит нативным видео, текст подписью;
  обложка в ленте — первый кадр ролика;
- ссылки `[текст](https://…)` в тексте становятся ссылками Telegram, остальное — без разметки;
- время — колонка «Время» строки «LinkedIn, Telegram» в таблице недели, пусто — по ритму, 10:00 МСК.

Подпись к картинке в Telegram — до 1024 знаков. Текст длиннее: сначала картинка, через минуту — текст.

Настройки — `Posts/render/.env.tg`, сессия — `Posts/render/.tg.session`; оба вне git.
Сессия даёт полный доступ к аккаунту: не копировать, не отправлять.
"""
import argparse
import asyncio
import os
import re
import subprocess
import sys
import tempfile
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
WEEKS = HERE.parent / "weeks"
ENV_FILE = HERE / ".env.tg"
SESSION = HERE / ".tg"  # Telethon допишет .session
MSK = timezone(timedelta(hours=3))
DEFAULT_TIME = "10:00"  # LinkedIn и Telegram по ритму, Posts/content-plan.md
CAPTION_LIMIT = 1024
WEEKDAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
DAYS = set(WEEKDAYS)


def load_env():
    if not ENV_FILE.exists():
        sys.exit(f"Нет {ENV_FILE}: скопируйте .env.tg.example и заполните.")
    env = {}
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    missing = [k for k in ("TG_API_ID", "TG_API_HASH", "TG_CHANNEL") if not env.get(k)]
    if missing:
        sys.exit(f"В {ENV_FILE.name} не заполнено: {', '.join(missing)}")
    return env


# ---------- разбор недели ----------

def week_dir(name):
    d = WEEKS / name
    if not (d / "_index.md").exists():
        sys.exit(f"Нет недели {d}")
    return d


def day_to_date(start: date, day_num: int) -> date:
    d = start.replace(day=1)
    for shift in range(0, 2):
        y, m = d.year + (d.month - 1 + shift) // 12, (d.month - 1 + shift) % 12 + 1
        try:
            cand = date(y, m, day_num)
        except ValueError:
            continue
        if 0 <= (cand - start).days < 14:
            return cand
    sys.exit(f"Не понял дату: число {day_num} в неделе от {start}")


def table_times(md: str):
    """{'Вт 1': '10:00'} для строк таблицы, где канал содержит Telegram."""
    times = {}
    header = None
    for line in md.splitlines():
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == "День":
            header = cells
            continue
        if not header or re.match(r"^-+$", cells[0] or "-"):
            continue
        row = dict(zip(header, cells))
        if "Telegram" in row.get("Канал", ""):
            t = row.get("Время", "").strip()
            times[row["День"]] = t
    return times


def parse_week(name):
    d = week_dir(name)
    md = (d / "_index.md").read_text()
    start = date.fromisoformat(name[:10])
    times = table_times(md)
    posts = []
    sections = re.split(r"^### ", md, flags=re.M)[1:]
    for sec in sections:
        title, _, body = sec.partition("\n")
        m = re.match(r"(\S\S) (\d{1,2})\. (.+)$", title.strip())
        if not m or m.group(1) not in DAYS:
            continue
        channels = m.group(3).split(".")[0]
        if "Telegram" not in channels:
            continue
        day = f"{m.group(1)} {m.group(2)}"
        code = re.search(r"^```[^\n]*\n(.*?)\n```", body, flags=re.S | re.M)
        text = code.group(1).strip() if code else ""

        media = []
        video = re.search(r"^Telegram:\s*видео\s+(.+?)\s*$", body, flags=re.M | re.I)
        if video:
            media = [Path(os.path.expanduser(video.group(1).strip("`")))]
        elif not re.search(r"^Telegram:\s*нет картинки", body, flags=re.M | re.I):
            emb = re.search(r"!\[\[([^\]|]+\.(?:png|jpe?g))", body)
            if emb:
                first = ROOT / emb.group(1)
                mm = re.match(r"(.+)-01(\.\w+)$", first.name)
                if mm:
                    media = sorted(first.parent.glob(f"{mm.group(1)}-[0-9][0-9]{mm.group(2)}"))
                else:
                    media = [first]

        t = times.get(day) or DEFAULT_TIME
        hh, mi = map(int, t.split(":"))
        when = datetime.combine(day_to_date(start, int(m.group(2))), time(hh, mi), MSK)
        posts.append({"day": day, "title": title.strip(), "text": text, "media": media, "video": bool(video),
                      "when": when, "time_src": "таблица" if times.get(day) else "ритм"})
    return posts


def check(p):
    problems = []
    if not p["text"]:
        problems.append("нет текста (блок ```)")
    for f in p["media"]:
        if not f.exists():
            problems.append(f"нет файла {show_path(f)}")
    if len(p["media"]) > 10:
        problems.append(f"альбом {len(p['media'])} картинок, в Telegram максимум 10")
    if p["when"] <= datetime.now(MSK) + timedelta(minutes=2):
        problems.append("время уже прошло")
    return problems


def describe(p):
    n = len(p["media"])
    media = "без картинки" if not n else (show_path(p["media"][0]) if n == 1 else f"альбом {n}: {p['media'][0].name}…")
    if p.get("video"):
        media = f"видео {media}"
    split = n and len(plain_text(p["text"])) > CAPTION_LIMIT
    mode = "картинка, через минуту текст" if split else ("текст подписью" if n else "текст")
    first = p["text"].splitlines()[0] if p["text"] else "—"
    return (f"{WEEKDAYS[p['when'].weekday()]} {p['when']:%d.%m %H:%M} МСК ({p['time_src']})  {p['title']}\n"
            f"    {media}; {mode}; {len(p['text'])} знаков\n"
            f"    «{first[:90]}»")


def show_path(f):
    try:
        return f.relative_to(ROOT).as_posix()
    except ValueError:
        return str(f).replace(str(Path.home()), "~", 1)


LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")


def plain_text(text):
    return LINK.sub(r"\1", text)


def with_links(text):
    """Текст без разметки и ссылки Telegram для `[текст](url)`; смещения — в UTF-16, как требует API."""
    from telethon import types
    out, entities, pos, off = [], [], 0, 0
    u16 = lambda s: len(s.encode("utf-16-le")) // 2
    for m in LINK.finditer(text):
        before = text[pos:m.start()]
        out.append(before)
        off += u16(before)
        label = m.group(1)
        entities.append(types.MessageEntityTextUrl(offset=off, length=u16(label), url=m.group(2)))
        out.append(label)
        off += u16(label)
        pos = m.end()
    out.append(text[pos:])
    return "".join(out), entities


def video_meta(f):
    """Длительность, размер и первый кадр (обложка) через ffmpeg из imageio_ffmpeg."""
    import imageio_ffmpeg
    exe = imageio_ffmpeg.get_ffmpeg_exe()
    info = subprocess.run([exe, "-hide_banner", "-i", str(f)], capture_output=True, text=True).stderr
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
    wh = re.search(r"Video: .*?, (\d{2,5})x(\d{2,5})", info)
    if not d or not wh:
        sys.exit(f"Не прочитал параметры видео {f}")
    dur = int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3))
    thumb = Path(tempfile.mkdtemp()) / "thumb.jpg"
    subprocess.run([exe, "-hide_banner", "-loglevel", "error", "-y", "-i", str(f), "-frames:v", "1",
                    "-vf", "scale=320:320:force_original_aspect_ratio=decrease", "-q:v", "3", str(thumb)], check=True)
    return dur, int(wh.group(1)), int(wh.group(2)), thumb


# ---------- Telegram ----------

def client(env):
    from telethon import TelegramClient
    return TelegramClient(str(SESSION), int(env["TG_API_ID"]), env["TG_API_HASH"])


async def scheduled(cl, channel):
    # Прямой запрос: iter_messages(scheduled=True) в Telethon 1.46 пропускает свежепоставленные сообщения.
    from telethon import functions, types
    r = await cl(functions.messages.GetScheduledHistoryRequest(peer=channel, hash=0))
    return [m for m in getattr(r, "messages", []) if isinstance(m, types.Message)]


def is_photo(m):
    from telethon import types
    return isinstance(m.media, types.MessageMediaPhoto)


def same_post(msg_text, text):
    """Совпадают первые 80 знаков без учёта пробелов и переносов строк."""
    a, b = (" ".join((s or "").split())[:80] for s in (msg_text, text))
    return bool(a) and a == b


def find_in_queue(queue, p):
    """Сообщения отложенной очереди, относящиеся к посту недели.

    Совпадение по времени поста (картинка в when, текст в when + 1 мин) или по началу текста;
    затем добавляются остальные картинки альбома и соседнее сообщение разнесённого поста.
    """
    slot = (p["when"], p["when"] + timedelta(minutes=1))
    hit = {m.id: m for m in queue if m.date in slot or same_post(m.message, plain_text(p["text"]))}
    groups = {m.grouped_id for m in hit.values() if m.grouped_id}
    dates = {m.date for m in hit.values()}
    for m in queue:
        if m.grouped_id in groups or any(abs(m.date - d) <= timedelta(minutes=1) for d in dates):
            hit[m.id] = m
    return sorted(hit.values(), key=lambda m: (m.date, m.id))


def describe_found(msgs):
    d = msgs[0].date.astimezone(MSK)
    text = next((m.message for m in msgs if m.message), "")
    first = text.splitlines()[0][:80] if text else "без текста"
    return f"{WEEKDAYS[d.weekday()]} {d:%d.%m %H:%M} МСК, сообщений {len(msgs)}: «{first}»"


async def delete_scheduled(cl, channel, msgs):
    from telethon import functions
    await cl(functions.messages.DeleteScheduledMessagesRequest(peer=channel, id=[m.id for m in msgs]))


async def post_one(cl, channel, p):
    text, entities = with_links(p["text"])
    files, when = [str(f) for f in p["media"]], p["when"]
    extra = {}
    if p.get("video"):
        from telethon import types
        dur, w, h, thumb = video_meta(p["media"][0])
        extra = dict(supports_streaming=True, thumb=str(thumb),
                     attributes=[types.DocumentAttributeVideo(duration=dur, w=w, h=h, supports_streaming=True)])
    if files and len(text) <= CAPTION_LIMIT:
        await cl.send_file(channel, files if len(files) > 1 else files[0],
                           caption=text, formatting_entities=entities or None, parse_mode=None,
                           schedule=when, **extra)
    else:
        if files:
            await cl.send_file(channel, files if len(files) > 1 else files[0], schedule=when, **extra)
            when = when + timedelta(minutes=1)
        await cl.send_message(channel, text, formatting_entities=entities or None, parse_mode=None,
                              link_preview=False, schedule=when)


async def cmd_send(env, posts):
    async with client(env) as cl:
        channel = await cl.get_entity(env["TG_CHANNEL"])
        queue = await scheduled(cl, channel)
        for p in posts:
            if find_in_queue(queue, p):
                print(f"уже в очереди  {p['title']}  (заменить — команда update)")
                continue
            await post_one(cl, channel, p)
            print(f"поставлено    {p['when']:%d.%m %H:%M} МСК  {p['title']}")


def confirm(question, yes):
    if yes:
        return True
    try:
        return input(f"{question} [y/N] ").strip().lower() in ("y", "yes", "д", "да")
    except EOFError:
        return False


async def cmd_update(env, posts, yes):
    """Заменяет пост в отложенных версией из _index.md: старые сообщения удаляются, новые ставятся."""
    async with client(env) as cl:
        channel = await cl.get_entity(env["TG_CHANNEL"])
        queue = await scheduled(cl, channel)
        plan = [(p, find_in_queue(queue, p)) for p in posts]
        for p, old in plan:
            note = p["time_src"]
            if old and p["time_src"] == "ритм":  # время, выставленное в приложении, не сбивать ритмом
                p["when"], note = old[0].date.astimezone(MSK), "из очереди; другое — в колонке «Время»"
            print(f"{p['title']}\n    было:  {describe_found(old) if old else 'в очереди не найдено, поставлю как новый'}"
                  f"\n    будет: {p['when']:%d.%m %H:%M} МСК ({note})")
        if not confirm("Заменить?", yes):
            sys.exit("Ничего не изменено.")
        for p, old in plan:
            if old:
                await delete_scheduled(cl, channel, old)
            await post_one(cl, channel, p)
            print(f"{'заменено' if old else 'поставлено'}   {p['when']:%d.%m %H:%M} МСК  {p['title']}")


async def cmd_delete(env, posts, yes):
    async with client(env) as cl:
        channel = await cl.get_entity(env["TG_CHANNEL"])
        queue = await scheduled(cl, channel)
        plan = []
        for p in posts:
            old = find_in_queue(queue, p)
            print(f"{p['title']}\n    {describe_found(old) if old else 'в очереди не найдено'}")
            if old:
                plan.append((p, old))
        if not plan:
            sys.exit("Удалять нечего.")
        if not confirm(f"Удалить из отложенных постов: {len(plan)}?", yes):
            sys.exit("Ничего не удалено.")
        for p, old in plan:
            await delete_scheduled(cl, channel, old)
            print(f"удалено       {p['title']}")


async def cmd_queue(env):
    async with client(env) as cl:
        channel = await cl.get_entity(env["TG_CHANNEL"])
        queue = sorted(await scheduled(cl, channel), key=lambda m: m.date)
        if not queue:
            print("Отложенных сообщений нет.")
        posts = []  # альбом — одна строка
        for m in queue:
            if m.grouped_id and posts and posts[-1]["group"] == m.grouped_id:
                posts[-1]["n"] += 1
                posts[-1]["text"] = posts[-1]["text"] or m.message
                continue
            posts.append({"group": m.grouped_id, "n": 1, "date": m.date, "text": m.message,
                          "kind": "фото" if is_photo(m) else ("файл" if m.media else "текст")})
        for p in posts:
            kind = f"альбом {p['n']}" if p["n"] > 1 else p["kind"]
            first = p["text"].splitlines()[0][:80] if p["text"] else ""
            d = p["date"].astimezone(MSK)
            print(f"{WEEKDAYS[d.weekday()]} {d:%d.%m %H:%M} МСК  {kind:9}  {first}")


async def cmd_login(env):
    cl = client(env)
    await cl.start()
    me = await cl.get_me()
    ch = await cl.get_entity(env["TG_CHANNEL"])
    print(f"Вход выполнен: {me.first_name}. Канал: {getattr(ch, 'title', env['TG_CHANNEL'])}")
    await cl.disconnect()


def main():
    ap = argparse.ArgumentParser(description="Отложенная публикация недели в Telegram-канал")
    ap.add_argument("cmd", choices=["login", "plan", "send", "update", "delete", "queue"])
    ap.add_argument("week", nargs="?", help="папка недели, например 2026-11-30-week-2")
    ap.add_argument("--only", help='один день, например "Вт 1"')
    ap.add_argument("--yes", action="store_true", help="update/delete без вопроса")
    args = ap.parse_args()

    if args.cmd == "delete":
        if not args.week:
            sys.exit("Укажите папку недели.")
        posts = parse_week(args.week)
        if args.only:
            posts = [p for p in posts if p["day"] == args.only]
        if not posts:
            sys.exit("Постов для Telegram в неделе не найдено.")
        asyncio.run(cmd_delete(load_env(), posts, args.yes))
    elif args.cmd in ("plan", "send", "update"):
        if not args.week:
            sys.exit("Укажите папку недели.")
        posts = parse_week(args.week)
        if args.only:
            posts = [p for p in posts if p["day"] == args.only]
        if not posts:
            sys.exit("Постов для Telegram в неделе не найдено.")
        bad = False
        for p in posts:
            print(describe(p))
            for pr in check(p):
                print(f"    ✖ {pr}")
                bad = True
        if args.cmd == "plan":
            return
        if bad:
            sys.exit("Есть проблемы — ничего не отправлено. Исправьте или выберите день через --only.")
        if args.cmd == "update":
            asyncio.run(cmd_update(load_env(), posts, args.yes))
        else:
            asyncio.run(cmd_send(load_env(), posts))
    elif args.cmd == "queue":
        asyncio.run(cmd_queue(load_env()))
    else:
        asyncio.run(cmd_login(load_env()))


if __name__ == "__main__":
    main()
