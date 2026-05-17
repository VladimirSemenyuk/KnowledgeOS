#!/usr/bin/env python3
import argparse
import datetime as dt
import re
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def guess_title(text: str, pdf: Path) -> str:
    lines = [line.strip() for line in text.splitlines()]
    first_page: list[str] = []
    page_started = False
    for line in lines:
        if line.startswith("--- PAGE 1"):
            page_started = True
            continue
        if page_started and line.startswith("--- PAGE"):
            break
        if page_started and line and len(line) <= 100:
            first_page.append(line)
    if first_page:
        return re.sub(r"\s+", " ", " ".join(first_page[:4]))

    candidates = [line for line in lines if line and not line.startswith("--- PAGE") and len(line) <= 100]
    if candidates:
        return re.sub(r"\s+", " ", " ".join(candidates[:2]))
    return pdf.stem.replace("-", " ").strip()


def excerpt(text: str, pattern: str, limit: int = 12) -> list[str]:
    matches = []
    regex = re.compile(pattern, re.IGNORECASE)
    for line in text.splitlines():
        clean = re.sub(r"\s+", " ", line.strip())
        if clean and regex.search(clean):
            matches.append(clean)
        if len(matches) >= limit:
            break
    return matches


def yaml_list(values: list[str]) -> str:
    return "\n".join(f"  - {value}" for value in values)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a KnowledgeOS PDF source-note scaffold.")
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--text", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--topic", action="append", default=[])
    parser.add_argument("--title")
    parser.add_argument("--author", default="")
    parser.add_argument("--version", default="")
    args = parser.parse_args()

    text = read_text(args.text)
    title = args.title or guess_title(text, args.pdf)
    topics = args.topic or ["AI transformation"]
    today = dt.date.today().isoformat()

    signal_lines = excerpt(
        text,
        r"AI|ROI|productivity|quality|risk|governance|platform|metric|organization|developer|delivery|cost|value",
        limit=20,
    )
    signal_block = "\n".join(f"- {line}" for line in signal_lines) or "- Добавить после чтения отчета."

    content = f"""---
type: source-note
source_type: pdf-report
topic:
{yaml_list(topics)}
status: processed
source_title: {title}
source_author: {args.author}
source_version: {args.version}
source_file: "{args.pdf}"
processed_date: {today}
---

# {title}

## Executive Summary

- TODO: 3-7 bullets с главным выводом отчета.

## Самое важное для моей базы знаний

### 1. TODO

- TODO

### 2. TODO

- TODO

### 3. TODO

- TODO

## Модели / фреймворки / формулы

```text
TODO
```

## Цифры и доказательная база

| Показатель | Значение | Интерпретация |
|---|---:|---|
| TODO | TODO | TODO |

## Управленческая интерпретация

### Для CEO

- TODO

### Для CTO / VP Engineering

- TODO

### Для Engineering Managers

- TODO

## Диагностические вопросы

- TODO

## Возможные фреймворки на основе отчета

```mermaid
flowchart TD
    A["TODO"] --> B["TODO"]
```

## Идеи для постов

### Пост 1: TODO

Hook:

> TODO

Тезис:

- TODO

## Связанные заметки

- [[AI-native organization]]
- [[architecture of manageability]]
- [[decision systems]]
- [[organizational operating model]]
- [[quality and risks]]
- [[systemic management]]

## Источник

- PDF: `{args.pdf}`
- Извлеченный текст: `{args.text}`

## Raw extraction signals

Эти строки нужны только как стартовые маркеры. Перед финализацией заметки удалить или заменить на нормальный анализ.

{signal_block}
"""

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(content, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
