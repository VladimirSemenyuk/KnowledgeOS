---
name: import-pdf-report
description: Convert PDF reports into concise KnowledgeOS Markdown source notes. Use when Codex needs to extract important insights from a PDF report, summarize it in Russian for the advisory knowledge base, preserve Obsidian wikilinks, create executive-oriented markdown, and place the result in the correct vault folder such as Frameworks/ai-transformation.
---

# Import PDF Report

## Purpose

Convert a PDF report into a high-signal Markdown source note for KnowledgeOS.

Use this skill for:
- AI / engineering / management / organizational reports in PDF;
- extracting the important ideas, models, formulas, figures, risks, and advisory implications;
- creating reusable Obsidian notes, not raw PDF text dumps.

## Required Context

Before writing the final note, read:
- `AGENTS.md`;
- relevant `Context.md` files if the destination is inside `Posts/`, `Clients/`, or another context-heavy area;
- nearby notes in the destination folder to match naming and style.

Default destination for AI transformation / engineering management reports:

```text
Frameworks/ai-transformation/
```

Use kebab-case filenames.

## Bundled Tools

Use bundled tools from this skill directory:

```text
.agents/skills/import-pdf-report/scripts/extract_pdf_text.swift
.agents/skills/import-pdf-report/scripts/create_source_note_scaffold.py
```

`extract_pdf_text.swift` uses macOS PDFKit and usually needs no package installation.

## Workflow

1. Confirm the PDF path exists.
2. Extract text:

```bash
swift .agents/skills/import-pdf-report/scripts/extract_pdf_text.swift "/path/to/report.pdf" /private/tmp/report.txt
```

If the PDF is outside the vault and sandbox blocks access, rerun with escalation.

3. Inspect the extracted text:

```bash
wc -l /private/tmp/report.txt
sed -n '1,220p' /private/tmp/report.txt
rg -n "ROI|AI|productivity|quality|risk|governance|platform|metric|organization|developer|delivery|cost|value" /private/tmp/report.txt
```

4. Create a markdown scaffold:

```bash
python3 .agents/skills/import-pdf-report/scripts/create_source_note_scaffold.py \
  --pdf "/path/to/report.pdf" \
  --text /private/tmp/report.txt \
  --output Frameworks/ai-transformation/report-name.md \
  --topic "AI transformation" \
  --topic "engineering management"
```

5. Edit the scaffold into a finished note. Do not leave generic placeholders.
6. Before finalizing, run a coverage pass for tables, figures, charts, diagrams, formulas, and numbered exhibits in the original extraction. Search explicitly for visual / tabular markers:

```bash
rg -n "Table|Figure|Fig\\.|Chart|Exhibit|Diagram|Formula|Equation|Таблица|Рисунок|Диаграмма|График|Формула|Уравнение" /private/tmp/report.txt
```

For each relevant table or diagram:
- decide whether it contains advisory signal, evidence, model logic, or reusable structure;
- add it to the note as a concise Markdown table, bullet synthesis, Mermaid diagram, or short interpretation;
- if it is not useful enough to include, make that exclusion deliberate and mention it in the final verification notes only if it affects completeness.

7. Run reverse fact-check before the final response:
- extract every concrete claim in the note: numbers, named findings, causal statements, maturity levels, formulas, dates, framework labels, recommendations, and risk statements;
- verify each claim against the PDF extraction or the original PDF pages when text extraction is ambiguous;
- correct any mismatch immediately;
- remove claims that cannot be traced to the source or clearly mark them as interpretation;
- ensure the note does not overstate the source, especially around ROI, productivity, quality, risks, and governance.

## Output Standard

The output must be concise, analytical, and useful for future advisory work.

Required sections:
- `Коротко`;
- `Самое важное для моей базы знаний`;
- key frameworks / models / formulas from the report;
- practical interpretation for CEO / CTO / engineering leaders;
- diagnostic questions;
- possible frameworks or post ideas if relevant;
- `Связанные заметки`;
- `Source`.

Prefer:
- Russian;
- short sections;
- bullets and tables;
- Mermaid for decision flows, operating models, risk systems, and ROI logic;
- Obsidian wikilinks for reusable concepts.

Avoid:
- raw OCR dumps;
- long quotations;
- motivational tone;
- startup hype;
- generic consulting language;
- copying the report structure mechanically.

## Extraction Notes

If extracted text is messy:
- use headings and repeated page markers to find structure;
- search for important terms with `rg`;
- read the executive summary, model / methodology pages, calculation examples, recommendations, and appendix;
- summarize tables manually instead of preserving broken PDF layout.
- for tables and diagrams, reconstruct the meaning rather than copying broken layout; preserve exact numbers, labels, axes, and relationships when they carry analytical value.

If PDFKit extraction returns little or no text, tell the user OCR is needed. Do not pretend the report was processed.

## Coverage And Fact-Checking Standard

The final note must be checked against the original report in both directions:

1. Source to note:
- important tables, charts, diagrams, formulas, frameworks, and numbered exhibits are represented or intentionally excluded;
- important quantitative evidence is not lost;
- appendices are checked for definitions, formulas, benchmarks, and methodology caveats.

2. Note to source:
- every specific number, comparison, framework, and recommendation in the note can be traced back to the report;
- analytical interpretation is separated from source facts;
- source caveats, sample limits, methodology limits, and definitions are preserved when they change the meaning of a claim.

Common corrections to make during this pass:
- fix rounded numbers that changed the meaning;
- restore missing denominators, time periods, sample sizes, or measurement units;
- distinguish "the report says" from "advisory implication";
- remove invented hierarchy, stages, or causal links not present in the report;
- add omitted visual evidence if it materially supports the main conclusion.

## Frontmatter Pattern

```markdown
---
type: source-note
source_type: pdf-report
topic:
  - AI transformation
status: processed
source_title:
source_author:
source_version:
source_file:
processed_date: YYYY-MM-DD
---
```

## Verification

Before final response:
- confirm the markdown file exists;
- open the beginning and end of the file;
- run the table / figure / diagram marker search and compare results against the final note;
- run a reverse fact-check pass from note claims back to source text / PDF pages;
- fix omissions or factual drift before responding;
- run `git status --short`;
- mention only files created or changed by this task;
- do not stage or commit unless explicitly asked.
