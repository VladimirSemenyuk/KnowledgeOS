---
type: website-build
status: published
published: 2026-11-14
created: 2026-11-11
language: ru
visibility: private
---

# Сайт — сборка RU

Статический одностраничник по [[Personal/Context|Позиционирование и метод]] и [[Personal/BRAND|BRAND.md]]; описание — в [[Personal/marketing/website/PRODUCT|PRODUCT.md]]. Пересобран 2026-11-14 под метод «Право управлять»: компактная версия на 7 экранов в визуальной территории «Доска после разбора» ([DESIGN.md](../DESIGN.md)). Только русская версия.

## Состав

- `index.html` — вся страница: разметка и стили в одном файле, немного JS для шапки и маркерных пометок.
- `talks/index.html` — страница выступлений для организаторов: слайды, темы, форматы. Стили — подмножество `index.html`, JS только для шапки (как на главной). Новое выступление: добавить `<article class="talk">`, PDF положить в `assets/files/`, обновить `llms.txt` и `lastmod` в `sitemap.xml`.
- `assets/img/og-cover.jpg` — обложка для ссылок, 1200×630; исходник — [`../og-cover.html`](../og-cover.html). Пересборка из папки `website/`:
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --force-device-scale-factor=1 --window-size=1200,630 --virtual-time-budget=5000 --screenshot=og.png "file://$PWD/og-cover.html"`, затем `sips -s format jpeg -s formatOptions 88 og.png --out site/assets/img/og-cover.jpg`.
- `favicon.ico`, `site.webmanifest`, `assets/icons/` — фавикон «ВС» (Montserrat SemiBold, белое на #121212), иконки 32, 180, 192, 512.
- `assets/img/vladimir-semenyuk.jpg` — чёрно-белый портрет 880×1100 (из `Talks/2026-11-12-upskill-week/img/me.jpeg`).
- `assets/img/reviews/` — фото авторов отзывов (вырезаны из скриншота, 124×124; заменить исходниками).
- `assets/files/metanavyki-i-instrumenty.pdf` — раздатка к pmclub Upskill Week.
- `assets/files/vostrebovannost-menedzhera-v-krizis.pdf` — слайды pmclub Upskill Week (из `Talks/2026-11-12-upskill-week/v2/slides.pdf`).
- `assets/files/kogda-komanda-rastyot.pdf` — слайды воркшопа в Стратоплане 31.03.2026 (из `Talks/2026-03-31-stratoplan/slides.pdf`).
- `assets/files/kak-it-organizacii-stanovyatsya-ai-native.pdf` — слайды выступления на TechRec, разрешение на публикацию есть. С 2026-11-17 показываются на странице `talks/`; на главной нет: тема относится к технологическому консалтингу.

- `tests/` — тесты для руководителей (с 2026-11-19). Проект — [`../paei-test.md`](../paei-test.md), тексты — [`../paei-texts.md`](../paei-texts.md).
  - `tests/index.html` — список тестов; `tests/assets/tests.css` и `tests.js` — общий движок: вопросы с пометками маркером, подсчёт, шифрование, «Поделиться», картинка для сторис.
  - `tests/paei/` — тест PAEI: `index.html` (вступление, вопросы, контакт), `data.js` (вопросы, роли, тексты, пороги, открытый ключ), `og.jpg`.
  - `tests/paei/r/<код>/` — 65 страниц результатов с превью. Не править руками: после изменения `data.js` пересобрать из папки `website/` командой `python3 tools/tests-build.py paei` (около двух минут, нужен Chrome).
  - `tests/key/` — служебная страница: Владимир вставляет закрытый ключ один раз в своём браузере, после этого ссылки на результаты показывают имя, контакт и ответы. Закрытый ключ не хранится ни на сайте, ни в репозитории — только в менеджере паролей. Потерян ключ — сгенерировать новую пару, заменить `publicKey` в `data.js`; старые ссылки останутся без расшифровки.
  - На тесты не ссылаемся с главной и из меню: вход только по прямой ссылке.

## Типографика

- Неразрывные пробелы после предлогов, союзов и частиц, между числом и словом, перед тире, в «им. Баумана».
- Кавычки «ёлочки», неразрывный дефис в «ТОП‑3».
- `lang="ru"`, `text-wrap: balance` для заголовков и `pretty` для абзацев; автоматические переносы выключены.
- Шрифт: Onest (Google Fonts, кириллица). Трекинг: заголовки −3…−4%, текст −1%.

## Публикация: GitHub Pages + домен GoDaddy

Опубликован на https://semenyuk.pro 2026-11-14. Обновление: закоммитить изменения в KnowledgeOS и запустить `Personal/marketing/website/deploy-site.sh` — он выкладывает папку `site/` в репозиторий `semenyuk.pro`. Настройка ниже нужна только при переносе на новый репозиторий или домен.

Домен: `semenyuk.pro` (заменяет прежний advisory-сайт). В папке уже есть `CNAME` и `.nojekyll`.

### GitHub

1. Создать публичный репозиторий, например `semenyuk.pro`.
2. Add file → Upload files → перетащить **содержимое** этой папки (не саму папку; `.DS_Store` не нужен). Скрытые `CNAME` и `.nojekyll` в Finder: Cmd+Shift+.
3. Settings → Pages → Source: Deploy from a branch → `main` / `(root)` → Save.
4. Custom domain: `semenyuk.pro` → Save.

### GoDaddy → DNS → Manage DNS

Удалить старые A-записи `@` и CNAME `www`, а также Forwarding, если включён. **MX и TXT для почты не трогать.**

| Тип | Имя | Значение |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | `<github-логин>.github.io` |

### После

- Через 10 минут — несколько часов GitHub проверит DNS. Включить **Enforce HTTPS** в Settings → Pages.
- Рекомендуется подтвердить домен: GitHub → Settings (профиль) → Pages → Add a domain → добавить выданную TXT-запись в GoDaddy.
- Если старый сайт был в Framer, отвязать там кастомный домен.

## Аналитика: Яндекс.Метрика

Счётчик `114369053` стоит в `index.html`, `talks/index.html` и на всех страницах `tests/` (на `tests/key/` — без Вебвизора и карты кликов, поля имени, контакта и ключа скрыты от Вебвизора классами `ym-disable-keys ym-hide-content`): код в `<head>`, `<noscript>` сразу после `<body>`. Включены Вебвизор, карта кликов, точный показатель отказов и учёт внешних ссылок. Проверено локально 2026-11-19: просмотр и цели доходят.

Цели — JS-события. Ссылка с атрибутами `data-goal` и `data-place` при клике отправляет цель с параметром `place`:

- `tg_write` — «Написать в Telegram»: `home-nav`, `home-hero`, `home-cases`, `home-final`, `home-footer`, `talks-nav`, `talks-final`, `talks-footer`;
- `tg_channel` — переход в канал «Управление и Счастье»: `home-footer`;
- `email_write` — письмо: `home-hero`, `home-footer`, `talks-footer`.
- тесты: `tg_write` с местами `test-nav`, `result-nav`, `tests-nav`, `*-footer`; события из `tests.js` — `test_start`, `test_finish`, `tg_send`, `share`, `story_image`, `copy_link` (параметр `test` — идентификатор теста).

**Новая страница** получает счётчик сразу: скопировать из `index.html` блок от комментария `<!-- Яндекс.Метрика ... -->` до `</script>` перед `</head>` и строку `<noscript>` сразу после `<body>`. Без этого `deploy-site.sh` остановит публикацию и назовёт страницу без счётчика.

Новая кнопка связи получает те же атрибуты. В интерфейсе Метрики цели создаются вручную: «Цели → JavaScript-событие», идентификатор как выше.

Ссылки для профилей (источник визита):

- Instagram: `https://semenyuk.pro/?utm_source=instagram&utm_medium=profile`
- LinkedIn: `https://semenyuk.pro/?utm_source=linkedin&utm_medium=profile`
- Threads: `https://semenyuk.pro/?utm_source=threads&utm_medium=profile`
- Telegram-канал: `https://semenyuk.pro/?utm_source=telegram&utm_medium=channel`
- Ссылка в конкретном посте: добавить `&utm_campaign=<дата-тема>`, например `2026-11-23-delegirovanie`.

Ссылка `t.me/vladimirsemenyuk` не передаёт источник, поэтому на вводном звонке спрашивать «откуда узнали» и записывать ответ в карточку лида.

## Открытые вопросы

- EN-версия — позже.
