---
name: transform-html-to-md
description: Преобразование HTML-файла с транскрибацией встречи в transcript.md, создание папки встречи с корректной датой у правильного клиента или менти, нормализация имен спикеров с задвоенной первой буквой.
---

# Transform HTML To MD

## Purpose

Преобразовать HTML-файл с транскрибацией в Markdown и положить результат в правильную папку встречи:

`Clients/.../{Менти}/Meetings/YYYY-MM-DD-meeting/transcript.md`

## When To Use

Использовать, когда пользователь просит:
- сделать Markdown из HTML-транскрибации;
- импортировать transcript из `.html`;
- создать папку встречи по дате;
- разложить транскрипт по правильному менти.

## Inputs

Обычно нужен один HTML-файл.

Если пользователь не указал менти явно:
- определить менти по содержимому HTML;
- затем сверить с существующими папками в `Clients`;
- учитывать `Context.md`, `Contex.md` и `AGENTS.md` на пути клиента/менти.

Если дата не указана явно:
- искать дату в HTML;
- затем в имени файла;
- использовать дату файловой системы только как fallback и сообщить об этом.

## Default Workflow

1. Найти HTML-файл, если путь не дан явно.
2. Запустить скрипт:

```bash
python3 .agents/skills/transform-html-to-md/scripts/transform_html_to_md.py path/to/transcript.html
```

3. Проверить, что создан файл:

```text
Clients/.../{Менти}/Meetings/YYYY-MM-DD-meeting/transcript.md
```

4. Быстро просмотреть начало `transcript.md`:
- заголовок содержит менти и дату;
- имена спикеров не имеют задвоенной первой буквы;
- каждая реплика содержит timestamp в формате `**Speaker** *[MM:SS]*: text`;
- Markdown читаемый, без HTML-мусора.

## Script Options

```bash
python3 .agents/skills/transform-html-to-md/scripts/transform_html_to_md.py INPUT.html
python3 .agents/skills/transform-html-to-md/scripts/transform_html_to_md.py INPUT.html --mentee "Юрий"
python3 .agents/skills/transform-html-to-md/scripts/transform_html_to_md.py INPUT.html --date 2026-05-13
python3 .agents/skills/transform-html-to-md/scripts/transform_html_to_md.py INPUT.html --output-dir "Clients/AgVend/Engineering Managers/Юрий"
```

Use `--output-dir` when the mentee name is ambiguous across clients.

## Speaker Normalization

Always remove doubled first letters in speaker labels:

```text
ВВладимир: -> Владимир:
ЮЮрий: -> Юрий:
AAndrew: -> Andrew:
```

Do this only for speaker names, not inside normal transcript text.

## Markdown Format

Use this output shape:

```markdown
# Transcript встречи: {Менти} & Владимир {YYYY-MM-DD}

**{Speaker}** *[MM:SS]*: text

**{Speaker}** *[MM:SS]*: text
```

Preserve transcript content. Do not summarize or rewrite meaning.

## Rules

- Не создавать новые top-level folders.
- Не удалять и не переименовывать существующие папки.
- Если `transcript.md` уже существует, не перезаписывать молча: сначала показать путь и спросить подтверждение, если пользователь явно не просил обновить.
- Если менти или дата не определены надежно, остановиться и задать один короткий вопрос.
- Русский язык для сообщений пользователю.
