"""Тесты mdtext.py: разбор Markdown постов для Telegram и обычный текст для LinkedIn.

Запуск из корня KnowledgeOS:
    Posts/render/.venv/bin/python -m unittest discover -s Posts/render/tests -v
"""
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import mdtext  # noqa: E402
from mdtext import parse, to_plain, to_telegram  # noqa: E402


def u16(s):
    return len(s.encode("utf-16-le")) // 2


def spans_text(text):
    """[(вид, кусок текста под разметкой, url)] — проверка смещений через сам текст."""
    plain, spans = parse(text)
    enc = plain.encode("utf-16-le")
    return plain, [(k, enc[o * 2:(o + l) * 2].decode("utf-16-le"), u) for k, o, l, u in spans]


class Parse(unittest.TestCase):
    def test_plain_text_untouched(self):
        self.assertEqual(parse("Просто текст, без разметки."), ("Просто текст, без разметки.", []))

    def test_each_kind(self):
        cases = {
            "**жирный**": ("bold", "жирный"),
            "*курсив*": ("ital", "курсив"),
            "_курсив_": ("ital", "курсив"),
            "~~зачёркнутый~~": ("strike", "зачёркнутый"),
            "`код`": ("code", "код"),
        }
        for md, (kind, body) in cases.items():
            with self.subTest(md=md):
                self.assertEqual(spans_text(f"до {md} после"), (f"до {body} после", [(kind, body, None)]))

    def test_link(self):
        self.assertEqual(spans_text("см. [канал](https://t.me/x) тут"),
                         ("см. канал тут", [("link", "канал", "https://t.me/x")]))

    def test_offsets_after_emoji_are_utf16(self):
        # эмодзи занимает две позиции UTF-16: Telegram считает смещения именно так
        plain, spans = parse("🔥 Важно: **жирный** текст")
        self.assertEqual(plain, "🔥 Важно: жирный текст")
        self.assertEqual(spans, [("bold", u16("🔥 Важно: "), 6, None)])
        self.assertEqual(spans[0][1], len("🔥 Важно: ") + 1)

    def test_offsets_after_several_spans(self):
        _, got = spans_text("😀 **раз** и 🙂 *два* и [три](https://a.b/c)")
        self.assertEqual(got, [("bold", "раз", None), ("ital", "два", None), ("link", "три", "https://a.b/c")])

    def test_nested_bold_link(self):
        plain, got = spans_text("Пишите в **[Instagram](https://instagram.com/x)**!")
        self.assertEqual(plain, "Пишите в Instagram!")
        self.assertEqual(got, [("bold", "Instagram", None), ("link", "Instagram", "https://instagram.com/x")])

    def test_nested_inside_bold(self):
        _, got = spans_text("**жирный и *курсив* внутри**")
        self.assertEqual(got, [("bold", "жирный и курсив внутри", None), ("ital", "курсив", None)])

    def test_code_content_is_literal(self):
        self.assertEqual(spans_text("`**не жирный**`"), ("**не жирный**", [("code", "**не жирный**", None)]))

    def test_underscore_inside_words_and_urls(self):
        for text in ("канал management_and_happiness",
                     "https://t.me/management_and_happiness",
                     "snake_case и ещё_одно_слово"):
            with self.subTest(text=text):
                self.assertEqual(parse(text), (text, []))

    def test_lone_asterisks_stay(self):
        for text in ("2 * 3 * 4 = 24", "звёздочка * одна", "** пусто **", "__ пусто __"):
            with self.subTest(text=text):
                self.assertEqual(parse(text), (text, []))

    def test_bold_does_not_cross_lines(self):
        text = "**начало\nконец**"
        self.assertEqual(parse(text), (text, []))

    def test_only_http_links(self):
        text = "[не ссылка](ftp://x) и [тоже](мимо)"
        self.assertEqual(parse(text), (text, []))


class ToTelegram(unittest.TestCase):
    def test_entities(self):
        from telethon import types
        plain, ents = to_telegram("🔥 **жирный** и [ссылка](https://t.me/x)")
        self.assertEqual(plain, "🔥 жирный и ссылка")
        self.assertIsInstance(ents[0], types.MessageEntityBold)
        self.assertEqual((ents[0].offset, ents[0].length), (3, 6))
        self.assertIsInstance(ents[1], types.MessageEntityTextUrl)
        self.assertEqual((ents[1].offset, ents[1].length, ents[1].url), (12, 6, "https://t.me/x"))

    def test_no_markup_no_entities(self):
        self.assertEqual(to_telegram("Привет!"), ("Привет!", []))


class ToPlain(unittest.TestCase):
    def test_markup_removed(self):
        self.assertEqual(to_plain("**жирный**, *курсив*, ~~нет~~, `код`"), "жирный, курсив, нет, код")

    def test_link_becomes_label_and_url(self):
        self.assertEqual(to_plain("Читайте [канал](https://t.me/x)."), "Читайте канал (https://t.me/x).")

    def test_link_with_address_in_label_not_doubled(self):
        self.assertEqual(to_plain("[semenyuk.pro](https://semenyuk.pro/)"), "semenyuk.pro")
        self.assertEqual(to_plain("[https://t.me/x](https://t.me/x)"), "https://t.me/x")

    def test_nested_link(self):
        self.assertEqual(to_plain("**[Instagram](https://instagram.com/x)**"), "Instagram (https://instagram.com/x)")


WEEK = """# Неделя

### Пн 30. Instagram. Reels

```
не LinkedIn
```

### Вт 1. LinkedIn и Telegram. Пост 1

```
**Первый** пост
```

### Ср 2. Telegram. Только канал

```
не LinkedIn
```

### Чт 3. LinkedIn. Пост 2

Комментарий до текста.

```text
Второй [пост](https://a.b)
```
"""


class LinkedinPosts(unittest.TestCase):
    def test_only_linkedin_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            week = Path(tmp) / "2026-11-30-week-x"
            week.mkdir()
            (week / "_index.md").write_text(WEEK)
            old, mdtext.WEEKS = mdtext.WEEKS, Path(tmp)
            try:
                posts = mdtext.linkedin_posts("2026-11-30-week-x")
            finally:
                mdtext.WEEKS = old
        self.assertEqual([(d, t) for d, _, t in posts], [("Вт 1", "**Первый** пост"), ("Чт 3", "Второй [пост](https://a.b)")])


class RealWeeks(unittest.TestCase):
    """Все посты недель в репозитории разбираются, разметка ложится в границы текста."""

    def test_entities_within_text(self):
        import tg
        weeks = sorted(p.name for p in mdtext.WEEKS.iterdir() if (p / "_index.md").exists())
        self.assertTrue(weeks)
        for w in weeks:
            for p in tg.parse_week(w) + [{"day": d, "text": t} for d, _, t in mdtext.linkedin_posts(w)]:
                with self.subTest(week=w, day=p["day"]):
                    plain, spans = parse(p["text"])
                    for _, o, l, _ in spans:
                        self.assertTrue(0 <= o and o + l <= u16(plain))
                    self.assertNotIn("**", plain)


if __name__ == "__main__":
    unittest.main()
