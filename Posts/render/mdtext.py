#!/usr/bin/env python3
"""Markdown в текстах постов: для Telegram — форматирование, для LinkedIn — обычный текст.

Тексты постов в `_index.md` недели пишутся в Markdown. Один и тот же текст уходит в Telegram и LinkedIn:
- Telegram (`tg.py`) показывает разметку: жирный, курсив, зачёркнутый, код, ссылки;
- LinkedIn разметку не понимает: текст отправляется без неё, ссылка — «текст (адрес)».

Что понимается:
    **жирный**   *курсив*   _курсив_   ~~зачёркнутый~~   `код`   [текст](https://…)
Внутри жирного, курсива и ссылки разметка может вкладываться: **[Instagram](https://…)**.
`_` в середине слова и в адресах (management_and_happiness) курсивом не считается.

Обычный текст для LinkedIn, из корня KnowledgeOS:

    Posts/render/.venv/bin/python Posts/render/mdtext.py linkedin 2026-11-30-week-2              # все посты LinkedIn недели
    Posts/render/.venv/bin/python Posts/render/mdtext.py linkedin 2026-11-30-week-2 --only "Вт 1"
"""
import argparse
import re
import sys
from pathlib import Path

WEEKS = Path(__file__).resolve().parent.parent / "weeks"

# Порядок важен: ссылка и код раньше остальных, жирный ** раньше курсива *.
TOKEN = re.compile(
    r"(?P<link>\[(?P<lt>[^\]\n]+)\]\((?P<lu>https?://[^)\s]+)\))"
    r"|(?P<code>`(?P<ct>[^`\n]+)`)"
    r"|(?P<bold>\*\*(?P<bt>\S(?:.*?\S)?)\*\*)"
    r"|(?P<strike>~~(?P<st>\S(?:.*?\S)?)~~)"
    r"|(?P<ital>(?<![\w*])\*(?P<it>\S(?:[^*\n]*?\S)?)\*(?![\w*]))"
    r"|(?P<ital2>(?<![\w/])_(?P<i2>\S(?:[^_\n]*?\S)?)_(?!\w))"
)


def _u16(s):
    return len(s.encode("utf-16-le")) // 2


def parse(text):
    """Разбирает Markdown: (текст без разметки, [(вид, смещение UTF-16, длина UTF-16, url)])."""
    out, spans, off, pos = [], [], 0, 0
    for m in TOKEN.finditer(text):
        before = text[pos:m.start()]
        out.append(before)
        off += _u16(before)
        kind = next(k for k in ("link", "code", "bold", "strike", "ital", "ital2") if m.group(k))
        inner = {"link": "lt", "code": "ct", "bold": "bt", "strike": "st", "ital": "it", "ital2": "i2"}[kind]
        body = m.group(inner)
        if kind == "code":
            sub, sub_spans = body, []
        else:
            sub, sub_spans = parse(body)
        n = _u16(sub)
        spans.append(({"ital2": "ital"}.get(kind, kind), off, n, m.group("lu") if kind == "link" else None))
        spans.extend((k, off + o, l, u) for k, o, l, u in sub_spans)
        out.append(sub)
        off += n
        pos = m.end()
    out.append(text[pos:])
    return "".join(out), spans


def to_telegram(text):
    """Текст и entities Telethon для отправки с parse_mode=None."""
    from telethon import types
    plain, spans = parse(text)
    make = {"bold": types.MessageEntityBold, "ital": types.MessageEntityItalic,
            "strike": types.MessageEntityStrike, "code": types.MessageEntityCode}
    ents = []
    for kind, o, l, url in spans:
        if not l:
            continue
        ents.append(types.MessageEntityTextUrl(offset=o, length=l, url=url) if kind == "link" else make[kind](o, l))
    return plain, ents


def to_plain(text):
    """Обычный текст для LinkedIn: разметка снята, ссылка — «текст (адрес)»."""
    def link(m):
        label, url = m.group(1), m.group(2)
        bare = re.sub(r"^https?://(www\.)?", "", url).rstrip("/")
        return label if url in label or bare in label else f"{label} ({url})"
    text = re.sub(r"\[([^\]\n]+)\]\((https?://[^)\s]+)\)", link, text)
    return parse(text)[0]


# ---------- посты LinkedIn недели ----------

def linkedin_posts(week):
    md_file = WEEKS / week / "_index.md"
    if not md_file.exists():
        sys.exit(f"Нет недели {md_file}")
    posts = []
    for sec in re.split(r"^### ", md_file.read_text(), flags=re.M)[1:]:
        title, _, body = sec.partition("\n")
        m = re.match(r"(\S\S) (\d{1,2})\. (.+)$", title.strip())
        if not m or "LinkedIn" not in m.group(3).split(".")[0]:
            continue
        code = re.search(r"^```[^\n]*\n(.*?)\n```", body, flags=re.S | re.M)
        if code:
            posts.append((f"{m.group(1)} {m.group(2)}", title.strip(), code.group(1).strip()))
    return posts


def main():
    ap = argparse.ArgumentParser(description="Тексты постов LinkedIn недели без Markdown")
    ap.add_argument("cmd", choices=["linkedin"])
    ap.add_argument("week", help="папка недели, например 2026-11-30-week-2")
    ap.add_argument("--only", help='один день, например "Вт 1"')
    a = ap.parse_args()
    posts = [p for p in linkedin_posts(a.week) if not a.only or p[0] == a.only]
    if not posts:
        sys.exit("Постов LinkedIn не найдено.")
    for i, (_, title, text) in enumerate(posts):
        if len(posts) > 1:
            print(f"{'' if i == 0 else chr(10)}===== {title}")
        print(to_plain(text))


if __name__ == "__main__":
    main()
