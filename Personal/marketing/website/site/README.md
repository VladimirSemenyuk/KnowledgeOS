---
type: website-build
status: ready-ru
created: 2026-11-11
language: ru
visibility: private
---

# Сайт-визитка — сборка RU

Статический одностраничник по [[Personal/marketing/website/personal-card-wireframe|макету]] и [[Personal/Context|Позиционирование и метод]]. Только русская версия.

## Состав

- `index.html` — вся страница: разметка и стили в одном файле, без JS.
- `favicon.ico`, `site.webmanifest`, `assets/icons/` — фавикон «ВС» (Montserrat SemiBold, белое на #121212), иконки 32, 180, 192, 512.
- `assets/img/vladimir-semenyuk.jpg` — фото, 640×640.
- `assets/img/reviews/` — фото авторов отзывов (вырезаны из скриншота, 124×124; заменить исходниками).
- `assets/files/metanavyki-i-instrumenty.pdf` — раздатка к pmclub Upskill Week.
- `assets/files/vostrebovannost-menedzhera-v-krizis.pdf` — слайды pmclub Upskill Week (из `Talks/2026-11-12-upskill-week/v2/slides.pdf`).
- `assets/files/kogda-komanda-rastyot.pdf` — слайды воркшопа в Стратоплане 31.03.2026 (из `Talks/2026-03-31-stratoplan/slides.pdf`).
- `assets/files/kak-it-organizacii-stanovyatsya-ai-native.pdf` — слайды выступления на TechRec, разрешение на публикацию есть.

## Типографика

- Неразрывные пробелы после предлогов, союзов и частиц, между числом и словом, перед тире, в «им. Баумана».
- Кавычки «ёлочки», неразрывный дефис в «ТОП‑3».
- `lang="ru"` и `hyphens: auto` для переносов в абзацах, `text-wrap: balance` для заголовков.
- Шрифты: Open Sans — текст, Montserrat SemiBold — заголовки (Google Fonts, кириллица). Трекинг: заголовки −4%, текст −2%.

## Публикация: GitHub Pages + домен GoDaddy

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

- Согласие авторов на публикацию отзывов с фото.
- EN-версия — позже.
