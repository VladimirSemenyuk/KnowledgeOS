"""Тесты tg.py без Telegram: разбор недели (даты, время, тексты, медиа) и поиск поста в отложенных.

Запуск из корня KnowledgeOS:
    Posts/render/.venv/bin/python -m unittest discover -s Posts/render/tests -v
"""
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import tg  # noqa: E402
from tg import MSK, day_to_date, find_in_queue, same_post, table_times  # noqa: E402


class DayToDate(unittest.TestCase):
    def test_same_month(self):
        self.assertEqual(day_to_date(date(2026, 11, 23), 25), date(2026, 11, 25))

    def test_next_month(self):
        self.assertEqual(day_to_date(date(2026, 11, 30), 1), date(2026, 12, 1))
        self.assertEqual(day_to_date(date(2026, 11, 30), 4), date(2026, 12, 4))

    def test_next_year(self):
        self.assertEqual(day_to_date(date(2026, 12, 28), 1), date(2027, 1, 1))
        self.assertEqual(day_to_date(date(2026, 12, 28), 31), date(2026, 12, 31))

    def test_day_before_week_start_is_error(self):
        with self.assertRaises(SystemExit):
            day_to_date(date(2026, 11, 23), 20)


class TableTimes(unittest.TestCase):
    MD = """
| День | Время | Канал | Формат |
| ---- | ----- | ----- | ------ |
| Пн 23 | 09:30 | Instagram | Reels |
| Вт 24 | 12:15 | LinkedIn, Telegram | Пост |
| Ср 25 |  | LinkedIn, Telegram | Пост |
| Сб 28 | 18:00 | Telegram | Видео |

Текст между таблицами.

| Секунды | Текст |
|---|---|
| Вт 24 | 23:59 |
"""

    def test_only_telegram_rows(self):
        self.assertEqual(table_times(self.MD), {"Вт 24": "12:15", "Ср 25": "", "Сб 28": "18:00"})

    def test_table_without_time_column(self):
        md = "| День | Канал |\n|---|---|\n| Вт 24 | LinkedIn, Telegram |\n"
        self.assertEqual(table_times(md), {"Вт 24": ""})


WEEK = """# Неделя

| День | Время | Канал | Формат |
| ---- | ----- | ----- | ------ |
| Пн 30 | 11:00 | Instagram | Reels |
| Вт 1 | 12:30 | LinkedIn, Telegram | Пост |
| Ср 2 |  | LinkedIn, Telegram | Карусель |

### Пн 30. Instagram. Reels, не для Telegram

![[Posts/weeks/W/instagram/img/r.png|160]]

```
Instagram
```

### Вт 1. LinkedIn и Telegram. Пост 1

![[Posts/weeks/W/linkedin/img/li1.png|200]]

```
**Первый** пост
```

### Ср 2. LinkedIn и Telegram. Пост 2, карусель

![[Posts/weeks/W/linkedin/img/li2-01.png|200]]

```
Второй пост
```

### Чт 3. LinkedIn. Только LinkedIn

```
Не в Telegram
```

### Пт 4. LinkedIn и Telegram. Без картинки

![[Posts/weeks/W/linkedin/img/li4.png|200]]
Telegram: нет картинки

```
Четвёртый пост
```

### Сб 5. Telegram. Видео

Telegram: видео ~/Movies/reels-1-final.mp4

```
Пятый пост
```

### Заметки

Не пост.
"""


class ParseWeek(unittest.TestCase):
    NAME = "2026-11-30-week-x"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        weeks = root / "Posts" / "weeks"
        week = weeks / self.NAME
        img = week / "linkedin" / "img"
        img.mkdir(parents=True)
        (week / "_index.md").write_text(WEEK.replace("/W/", f"/{self.NAME}/"))
        for f in ("li1.png", "li2-01.png", "li2-02.png", "li2-03.png", "li2-cover.png", "li4.png"):
            (img / f).write_bytes(b"")
        self.saved = tg.WEEKS, tg.ROOT
        tg.WEEKS, tg.ROOT = weeks, root
        self.img = img
        self.posts = {p["day"]: p for p in tg.parse_week(self.NAME)}

    def tearDown(self):
        tg.WEEKS, tg.ROOT = self.saved
        self.tmp.cleanup()

    def test_only_telegram_sections(self):
        self.assertEqual(list(self.posts), ["Вт 1", "Ср 2", "Пт 4", "Сб 5"])

    def test_time_from_table_or_default(self):
        self.assertEqual(self.posts["Вт 1"]["when"], datetime(2026, 12, 1, 12, 30, tzinfo=MSK))
        self.assertEqual(self.posts["Вт 1"]["time_src"], "таблица")
        self.assertEqual(self.posts["Ср 2"]["when"], datetime(2026, 12, 2, 10, 0, tzinfo=MSK))
        self.assertEqual(self.posts["Ср 2"]["time_src"], "ритм")
        self.assertEqual(self.posts["Сб 5"]["when"].date(), date(2026, 12, 5))

    def test_text_is_first_code_block_verbatim(self):
        self.assertEqual(self.posts["Вт 1"]["text"], "**Первый** пост")

    def test_single_image(self):
        self.assertEqual(self.posts["Вт 1"]["media"], [self.img / "li1.png"])

    def test_carousel_collects_numbered_images_only(self):
        self.assertEqual(self.posts["Ср 2"]["media"], [self.img / f"li2-0{i}.png" for i in (1, 2, 3)])

    def test_no_image_line(self):
        self.assertEqual(self.posts["Пт 4"]["media"], [])

    def test_video(self):
        p = self.posts["Сб 5"]
        self.assertTrue(p["video"])
        self.assertEqual(p["media"], [Path.home() / "Movies" / "reels-1-final.mp4"])

    def test_check_reports_missing_text_and_file(self):
        p = dict(self.posts["Вт 1"], text="", media=[self.img / "nope.png"], when=datetime.now(MSK) + timedelta(days=1))
        problems = tg.check(p)
        self.assertIn("нет текста (блок ```)", problems)
        self.assertTrue(any("nope.png" in x for x in problems))

    def test_check_past_time(self):
        p = dict(self.posts["Вт 1"], when=datetime.now(MSK) - timedelta(hours=1))
        self.assertIn("время уже прошло", tg.check(p))


def msg(id, when, text="", group=None):
    return SimpleNamespace(id=id, date=when, message=text, grouped_id=group)


class SamePost(unittest.TestCase):
    def test_ignores_whitespace_and_tail(self):
        self.assertTrue(same_post("Почему  повысят\nне вас?" + "x" * 100, "Почему повысят не вас?" + "x" * 100))

    def test_first_80_chars(self):
        head = "а" * 80
        self.assertTrue(same_post(head + "конец один", head + "конец другой"))
        self.assertFalse(same_post("а" * 79 + "б", "а" * 80))

    def test_empty_never_matches(self):
        self.assertFalse(same_post("", ""))
        self.assertFalse(same_post(None, ""))


class FindInQueue(unittest.TestCase):
    T = datetime(2026, 12, 1, 10, 0, tzinfo=MSK)

    def post(self, text="**Почему** повысят не вас", when=None):
        return {"text": text, "when": when or self.T}

    def test_by_time(self):
        q = [msg(1, self.T, "старый текст"), msg(2, self.T + timedelta(days=1), "другой пост")]
        self.assertEqual([m.id for m in find_in_queue(q, self.post())], [1])

    def test_by_text_when_time_changed(self):
        # текст в очереди без разметки: сравнивается с текстом поста после разбора Markdown
        q = [msg(1, self.T + timedelta(hours=3), "Почему повысят не вас"), msg(2, self.T + timedelta(days=1), "другой")]
        self.assertEqual([m.id for m in find_in_queue(q, self.post())], [1])

    def test_album_and_split_text(self):
        q = [msg(3, self.T, "", group=77), msg(1, self.T, "", group=77), msg(2, self.T, "", group=77),
             msg(4, self.T + timedelta(minutes=1), "длинный текст отдельно"),
             msg(5, self.T + timedelta(days=1), "", group=88)]
        self.assertEqual([m.id for m in find_in_queue(q, self.post())], [1, 2, 3, 4])

    def test_other_posts_untouched(self):
        q = [msg(1, self.T - timedelta(days=1), "вчерашний"), msg(2, self.T + timedelta(hours=2), "сегодня позже"),
             msg(3, self.T + timedelta(days=1), "завтрашний")]
        self.assertEqual(find_in_queue(q, self.post()), [])


class RealWeeks(unittest.TestCase):
    """Недели в репозитории разбираются; даты постов — внутри своей недели."""

    def test_all_weeks(self):
        weeks = sorted(p.name for p in tg.WEEKS.iterdir() if (p / "_index.md").exists())
        self.assertTrue(weeks)
        for w in weeks:
            start = date.fromisoformat(w[:10])
            for p in tg.parse_week(w):
                with self.subTest(week=w, day=p["day"]):
                    self.assertTrue(0 <= (p["when"].date() - start).days < 7)
                    # «Вт 2» вместо «Вт 1»: число не совпадает с днём недели — пост уйдёт не в тот день
                    self.assertEqual(tg.WEEKDAYS[p["when"].weekday()], p["day"].split()[0])


if __name__ == "__main__":
    unittest.main()
