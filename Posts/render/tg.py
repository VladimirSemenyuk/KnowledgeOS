#!/usr/bin/env python3
"""Автопостинг в Telegram-канал: посты недели встают в штатную отложенную публикацию канала.

Работает от аккаунта автора (Telethon), сервер не нужен: скрипт ставит сообщения
в «Отложенные» канала, дальше публикует сам Telegram. Очередь видна и правится в приложении.

Запуск из корня KnowledgeOS через окружение `.venv`:

    R=Posts/render
    $R/.venv/bin/python $R/tg.py login                       # один раз, в своём терминале: телефон и код
    $R/.venv/bin/python $R/tg.py plan 2026-11-30-week-2      # что встанет в очередь, ничего не отправляет
    $R/.venv/bin/python $R/tg.py send 2026-11-30-week-2      # поставить в отложенные
    $R/.venv/bin/python $R/tg.py queue                       # что уже стоит в отложенных канала

`send` повторно не ставит пост, если в отложенных уже есть сообщение с тем же началом текста.
`--only "Вт 1"` — только один день.

Откуда что берётся в `_index.md` недели:
- пост — раздел `### <День> <число>. LinkedIn и Telegram. …` (или `. Telegram. …`);
- текст — первый блок ``` в разделе, переносится дословно, без разметки;
- картинка — первая `![[…]]` в разделе; если её имя кончается на `-01.png`,
  уходит альбом из всех `-NN.png` рядом (карусель). Строка `Telegram: нет картинки` — пост без картинки;
- время — колонка «Время» строки «LinkedIn, Telegram» в таблице недели, пусто — по ритму, 10:00 МСК.

Подпись к картинке в Telegram — до 1024 знаков. Текст длиннее: сначала картинка, через минуту — текст.

Настройки — `Posts/render/.env.tg`, сессия — `Posts/render/.tg.session`; оба вне git.
Сессия даёт полный доступ к аккаунту: не копировать, не отправлять.
"""
import argparse
import asyncio
import re
import sys
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
        if not re.search(r"^Telegram:\s*нет картинки", body, flags=re.M | re.I):
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
        posts.append({"day": day, "title": title.strip(), "text": text, "media": media,
                      "when": when, "time_src": "таблица" if times.get(day) else "ритм"})
    return posts


def check(p):
    problems = []
    if not p["text"]:
        problems.append("нет текста (блок ```)")
    for f in p["media"]:
        if not f.exists():
            problems.append(f"нет файла {f.relative_to(ROOT)}")
    if len(p["media"]) > 10:
        problems.append(f"альбом {len(p['media'])} картинок, в Telegram максимум 10")
    if p["when"] <= datetime.now(MSK) + timedelta(minutes=2):
        problems.append("время уже прошло")
    return problems


def describe(p):
    n = len(p["media"])
    media = "без картинки" if not n else (p["media"][0].relative_to(ROOT).as_posix() if n == 1 else f"альбом {n}: {p['media'][0].name}…")
    split = n and len(p["text"]) > CAPTION_LIMIT
    mode = "картинка, через минуту текст" if split else ("текст подписью" if n else "текст")
    first = p["text"].splitlines()[0] if p["text"] else "—"
    return (f"{WEEKDAYS[p['when'].weekday()]} {p['when']:%d.%m %H:%M} МСК ({p['time_src']})  {p['title']}\n"
            f"    {media}; {mode}; {len(p['text'])} знаков\n"
            f"    «{first[:90]}»")


# ---------- Telegram ----------

def client(env):
    from telethon import TelegramClient
    return TelegramClient(str(SESSION), int(env["TG_API_ID"]), env["TG_API_HASH"])


async def scheduled(cl, channel):
    return [m async for m in cl.iter_messages(channel, scheduled=True)]


def same_post(msg_text, text):
    a, b = (msg_text or "").strip()[:80], text.strip()[:80]
    return bool(a) and a == b


async def cmd_send(env, posts):
    async with client(env) as cl:
        channel = await cl.get_entity(env["TG_CHANNEL"])
        queue = await scheduled(cl, channel)
        for p in posts:
            if any(same_post(m.message, p["text"]) for m in queue):
                print(f"уже в очереди  {p['title']}")
                continue
            text, files, when = p["text"], [str(f) for f in p["media"]], p["when"]
            if files and len(text) <= CAPTION_LIMIT:
                await cl.send_file(channel, files if len(files) > 1 else files[0],
                                   caption=text, parse_mode=None, schedule=when)
            else:
                if files:
                    await cl.send_file(channel, files if len(files) > 1 else files[0], schedule=when)
                    when = when + timedelta(minutes=1)
                await cl.send_message(channel, text, parse_mode=None, link_preview=False, schedule=when)
            print(f"поставлено    {p['when']:%d.%m %H:%M} МСК  {p['title']}")


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
                          "kind": "фото" if m.photo else ("файл" if m.media else "текст")})
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
    ap.add_argument("cmd", choices=["login", "plan", "send", "queue"])
    ap.add_argument("week", nargs="?", help="папка недели, например 2026-11-30-week-2")
    ap.add_argument("--only", help='один день, например "Вт 1"')
    args = ap.parse_args()

    if args.cmd in ("plan", "send"):
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
        asyncio.run(cmd_send(load_env(), posts))
    elif args.cmd == "queue":
        asyncio.run(cmd_queue(load_env()))
    else:
        asyncio.run(cmd_login(load_env()))


if __name__ == "__main__":
    main()
