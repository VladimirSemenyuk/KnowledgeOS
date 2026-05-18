---
name: create-telegram-weekly-digest
description: Собирает через GramJS сообщения из выбранных Telegram-каналов за неделю, фильтрует их по advisory-предпочтениям пользователя и создает краткую Markdown-подборку в Posts/research/telegram.
---

# Telegram Weekly Digest

## Purpose

Собрать недельную подборку сильных Telegram-сигналов для тем:

- AI transformation;
- engineering management;
- organizational design;
- CTO/CEO advisory;
- decision systems;
- architecture of manageability;
- quality and risks;
- systemic management.

## Required Context

Перед генерацией digest прочитать:

- `AGENTS.md`;
- `Posts/Context.md`;
- `Posts/research/telegram/channels.yaml`, если существует;
- последний digest из `Posts/research/telegram/weekly-digests`, если существует.

Соблюдать стиль vault:

- русский язык;
- кратко;
- системно;
- executive-oriented;
- без motivational tone;
- без startup hype;
- без generic consulting language.
- без случайных английских слов внутри русских формулировок.

Языковое правило:

- переводить смысл источников на русский, если это не прямая цитата;
- оставлять английский для названий компаний, продуктов, каналов, метрик, прямых цитат и технических терминов без точного русского эквивалента;
- предпочитать `выводы`, `наблюдения`, `модель`, `рамка`, `процесс`, `зона ответственности`, `принятие решений`, `управленческий контур`.

## Data Locations

Рабочие файлы внутри vault:

```text
Posts/research/telegram/
├── channels.yaml
├── raw/
├── normalized/
└── weekly-digests/
```

Credentials хранить в корне vault, но не коммитить. Скрипты ищут credentials в таком порядке:

1. `TELEGRAM_WEEKLY_CREDENTIAL_ROOT`, если переменная задана.
2. `.agents/skills/create-telegram-weekly-digest/.private/`.
3. Текущий vault root.
4. `/Users/vladimir/Obsidian/KnowledgeOS`.

```text
KnowledgeOS/.agents/skills/create-telegram-weekly-digest/.private/
├── .telegram-weekly.env
└── .telegram-weekly.session.txt
```

Эти файлы должны быть в `.gitignore`.

Никогда не коммитить:

- `TELEGRAM_API_ID`;
- `TELEGRAM_API_HASH`;
- phone number;
- 2FA password;
- GramJS string session;
- private messages.

## First Run

Если `Posts/research/telegram/channels.yaml` отсутствует:

1. Скопировать структуру из `references/config.example.yaml`.
2. Попросить пользователя заполнить каналы.
3. Не угадывать каналы самостоятельно.

Если GramJS dependencies не установлены:

```bash
cd .agents/skills/create-telegram-weekly-digest
npm install
```

Перед авторизацией создать `.telegram-weekly.env` в корне `KnowledgeOS`:

```bash
TELEGRAM_API_ID=123456
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=+10000000000
```

Если session отсутствует:

```bash
node .agents/skills/create-telegram-weekly-digest/scripts/auth.mjs
```

Если Telegram требует code / 2FA, пользователь вводит их локально. Не просить пользователя отправлять код или пароль в чат.

## Collection Workflow

1. Определить период:
   - по умолчанию последние 7 дней;
   - если пользователь просит "прошлая неделя", использовать предыдущую ISO-неделю.
2. Прочитать `Posts/research/telegram/channels.yaml`.
3. Запустить сбор:

```bash
node .agents/skills/create-telegram-weekly-digest/scripts/fetch-week.mjs
```

Если сбор падает с `connect EPERM` или сообщением про sandbox network policy, повторить этот же fetch с `sandbox_permissions=require_escalated`. Это ожидаемый путь для прямого подключения GramJS к Telegram DC из Codex.

4. Сохранить raw-файл:
   `Posts/research/telegram/raw/YYYY-Www.json`
5. Запустить нормализацию:

```bash
node .agents/skills/create-telegram-weekly-digest/scripts/normalize-messages.mjs
```

6. Сохранить normalized-файл:
   `Posts/research/telegram/normalized/YYYY-Www.json`
7. Прочитать normalized JSON и `references/scoring-rubric.md`.
8. Создать digest:
   `Posts/research/telegram/weekly-digests/YYYY-Www-telegram-digest.md`

## Filtering Logic

Исключать:

- рекламу;
- вакансии;
- анонсы без управленческого вывода;
- чистые обновления инструментов без организационных последствий;
- повторяющиеся пересказы одной новости;
- низкосигнальные motivational posts.

Повышать приоритет:

- системные сдвиги в AI adoption, если термин важен в источнике;
- управление, качество, риски;
- последствия для операционной модели;
- изменения роли CTO / VP Engineering;
- зоны ответственности и принятие решений;
- AI в реальных процессах, а не в витринных демо;
- признаки зрелости или деградации управления.

## Digest Format

```markdown
---
title: "Telegram digest YYYY-Www"
period: "YYYY-MM-DD - YYYY-MM-DD"
source: telegram
status: research
---

# Telegram digest YYYY-Www

## Executive Summary

- 3-5 пунктов: что важно за неделю.

## Сигналы

### 1. Короткий смысловой заголовок

- Источник: [Channel Name](https://t.me/channel/123)
- Почему это важно:
  управленческий смысл.
- Смысл:
  что это меняет для CTO/CEO/инженерной организации.
- Идеи для поста:
  как это развить в пост, framework или advisory-наблюдение.

## Паттерны

- Повторяющийся паттерн 1.
- Повторяющийся паттерн 2.

## Возможности для контента

- [[draft-topic-1]]
- [[draft-topic-2]]

## Ссылки на источники

- https://t.me/...
```

## Verification

Перед финальным ответом проверить:

- raw JSON создан;
- normalized JSON создан;
- digest создан;
- credentials не попали в vault;
- Telegram links сохранены;
- подборка не содержит generic news без управленческого вывода.

В финальном ответе кратко указать:

- период;
- число прочитанных сообщений;
- число кандидатов после нормализации;
- путь к digest;
- если не удалось подключиться к Telegram, какой шаг нужен от пользователя.
