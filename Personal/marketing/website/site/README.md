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
- `assets/img/og-cover.jpg` — обложка для ссылок, 1200×630; исходник — [`../og-cover.html`](../og-cover.html). Пересборка из папки `website/`:
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --force-device-scale-factor=1 --window-size=1200,630 --virtual-time-budget=5000 --screenshot=og.png "file://$PWD/og-cover.html"`, затем `sips -s format jpeg -s formatOptions 88 og.png --out site/assets/img/og-cover.jpg`.
- `favicon.ico`, `site.webmanifest`, `assets/icons/` — фавикон «ВС» (Montserrat SemiBold, белое на #121212), иконки 32, 180, 192, 512.
- `assets/img/vladimir-semenyuk.jpg` — чёрно-белый портрет 880×1100 (из `Talks/2026-11-12-upskill-week/img/me.jpeg`).
- `assets/img/reviews/` — фото авторов отзывов (вырезаны из скриншота, 124×124; заменить исходниками).
- `assets/files/metanavyki-i-instrumenty.pdf` — раздатка к pmclub Upskill Week.
- `assets/files/vostrebovannost-menedzhera-v-krizis.pdf` — слайды pmclub Upskill Week (из `Talks/2026-11-12-upskill-week/v2/slides.pdf`).
- `assets/files/kogda-komanda-rastyot.pdf` — слайды воркшопа в Стратоплане 31.03.2026 (из `Talks/2026-03-31-stratoplan/slides.pdf`).
- `assets/files/kak-it-organizacii-stanovyatsya-ai-native.pdf` — слайды выступления на TechRec, разрешение на публикацию есть. С 2026-11-14 на странице не показываются: тема относится к технологическому консалтингу.

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

## Открытые вопросы

- EN-версия — позже.
