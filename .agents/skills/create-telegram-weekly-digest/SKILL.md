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

## Data Locations

Рабочие файлы внутри vault:

```text
Posts/research/telegram/
├── channels.yaml
├── raw/
├── normalized/
└── weekly-digests/
```

Credentials хранить в корне vault, но не коммитить:

```text
KnowledgeOS/
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
cd .agents/skills/telegram-weekly-digest
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
node scripts/auth.mjs
```

Если Telegram требует code / 2FA, пользователь вводит их локально. Не просить пользователя отправлять код или пароль в чат.

## Collection Workflow

1. Определить период:
   - по умолчанию последние 7 дней;
   - если пользователь просит "прошлая неделя", использовать предыдущую ISO-неделю.
2. Прочитать `Posts/research/telegram/channels.yaml`.
3. Запустить сбор:

```bash
node .agents/skills/telegram-weekly-digest/scripts/fetch-week.mjs
```

4. Сохранить raw-файл:
   `Posts/research/telegram/raw/YYYY-Www.json`
5. Запустить нормализацию:

```bash
node .agents/skills/telegram-weekly-digest/scripts/normalize-messages.mjs
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
- чистые tool updates без organizational implications;
- повторяющиеся пересказы одной новости;
- низкосигнальные motivational posts.

Повышать приоритет:
- системные сдвиги в AI adoption;
- governance, quality, risks;
- operating model implications;
- изменения роли CTO / VP Engineering;
- ownership и decision-making;
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

- 3-5 bullets: что важно за неделю.

## Strong Signals

### 1. Короткий смысловой заголовок

- Источник: [Channel Name](https://t.me/channel/123)
- Почему это важно: 
   управленческий смысл.
- Смысл: 
   что это меняет для CTO/CEO/engineering org.
- Идеи для поста: 
   как это развить в пост, framework или advisory insight.

## Patterns

- Повторяющийся паттерн 1.
- Повторяющийся паттерн 2.

## Content Opportunities

- [[draft-topic-1]]
- [[draft-topic-2]]

## Raw Links

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
