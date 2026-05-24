---
name: apply-typograf
description: Run the npm package `typograf` on a selected Markdown or text file/folder in KnowledgeOS. Use when the user asks to typographically clean, типографировать, прогнать typograf, fix quotes/dashes/spaces, or apply Russian typography to a specific `.md`, `.markdown`, or `.txt` file or directory while preserving Markdown, Obsidian wikilinks, code blocks, inline code, links, and frontmatter.
---

# Apply Typograf

## Purpose

Типографировать выбранный файл или папку через npm-пакет `typograf`, не ломая Markdown и Obsidian-разметку.

## Default Workflow

1. Найти указанный пользователем файл или папку. Если путь не указан, задать один короткий вопрос.
2. Если зависимости еще не установлены, выполнить:

```bash
npm --prefix .agents/skills/apply-typograf install
```

3. Перед записью проверить масштаб изменений:

```bash
npm --prefix .agents/skills/apply-typograf run typograf -- "path/to/file-or-folder"
```

4. Если пользователь попросил применить изменения или dry-run выглядит ожидаемо, выполнить:

```bash
npm --prefix .agents/skills/apply-typograf run typograf -- "path/to/file-or-folder" --write
```

5. После записи показать пользователю список измененных файлов. Для важных материалов быстро проверить `git diff -- <path>`.

## Script Behavior

- По умолчанию работает в dry-run и только показывает, какие файлы изменились бы.
- Для папок рекурсивно обрабатывает `.md`, `.markdown`, `.txt`.
- Пропускает `.git`, `.obsidian`, `node_modules`, `.agents/skills/*/node_modules`.
- Сохраняет YAML frontmatter без изменений.
- Сохраняет без изменений fenced code blocks, indented code blocks, inline code, Markdown links, plain URLs, Obsidian wikilinks, Obsidian embeds and tags.
- Использует локали `ru,en-US` по умолчанию.

## Options

```bash
npm --prefix .agents/skills/apply-typograf run typograf -- "Posts/drafts/post.md"
npm --prefix .agents/skills/apply-typograf run typograf -- "Posts/drafts" --write
npm --prefix .agents/skills/apply-typograf run typograf -- "file.md" --locale ru,en-US
npm --prefix .agents/skills/apply-typograf run typograf -- "file.md" --extensions .md,.txt
npm --prefix .agents/skills/apply-typograf run typograf -- "file.md" --force --write
```

Use `--force` only for an explicitly selected single file with a non-default extension.

## Rules

- Не запускать по всему vault без явного запроса пользователя.
- Не типографировать raw imports, generated JSON, PDF sources or dependency folders.
- Не использовать `typograf` для юридических, финансовых или контрактных документов без явного подтверждения.
- Не переписывать смысл текста вручную: этот skill только применяет типографику.
