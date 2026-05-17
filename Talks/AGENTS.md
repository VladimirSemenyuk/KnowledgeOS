# Talks Agent Instructions

## Purpose

This folder manages public talks, conference presentations, webinars, and private speaking engagements.

The goal is to turn raw context into a clear, structured, audience-specific talk:
- thesis;
- narrative arc;
- slide outline;
- timing;
- examples;
- speaker notes;
- follow-up assets.

Talks are part of the repository's intellectual property and should preserve the strategic advisory style of the vault.

---

# Core Principles

Prefer:
- clear executive framing;
- systemic insight;
- practical management implications;
- role, process, governance, and operating model language;
- concise slide-level structure;
- strong transitions between sections;
- reusable intellectual assets.

Avoid:
- motivational keynote tone;
- startup hype;
- generic AI enthusiasm;
- generic consulting claims;
- over-explaining obvious context;
- engagement-bait hooks;
- ungrounded predictions.

---

# Folder Structure

Each talk should live in a dedicated folder:

`YYYY-MM-DD-event-name`

Examples:
- `2026-06-06-techrec`
- `2026-09-15-ai-leadership-forum`

Do not rename existing talk folders unless explicitly requested.

Preferred files inside a talk folder:
- `raw-info.md` — source material, notes, client/event context, extracted insights;
- `talk-outline.md` — main talk structure, slide sequence, timing, thesis;
- `speaker-notes.md` — expanded talking points, transitions, examples;
- `slide-copy.md` — concise slide-ready wording;
- `qa.md` — likely questions and structured answers;
- `follow-up.md` — post-talk materials, links, references, next-step ideas.

Create only the files needed for the current task.

---

# Talk Metadata

Main talk files should use YAML frontmatter when practical:

```yaml
type: talk
status: draft
date:
event:
topic:
audience:
duration:
presentation_url:
source:
goal:
```

Use statuses:
- `idea`;
- `draft`;
- `review`;
- `ready`;
- `delivered`;
- `archived`.

Keep metadata factual and concise.

---

# Writing Style

Russian is preferred unless the talk context requires another language.

For Russian talk materials:
- write slide titles, theses, speaker notes, and conclusions in Russian by default;
- avoid unnecessary English terms when a precise Russian equivalent exists;
- keep English only for product names, company names, direct quotes, established technical terms, or event language;
- if an English term is useful for the audience, introduce it once in parentheses and then use the Russian equivalent;
- prefer Russian management vocabulary over consulting slang.

Use:
- short sections;
- bullets;
- slide-level headings;
- timing markers;
- explicit key thought per slide;
- operational conclusions.

Avoid:
- decorative phrasing;
- excessive rhetorical questions;
- long paragraphs;
- unexplained buzzwords;
- vague statements like "AI changes everything".

Each slide or section should have:
- one key thought;
- supporting theses;
- clear relation to the audience;
- practical implication.

---

# Narrative Structure

Preferred talk structure:

1. Context and tension.
2. Main thesis.
3. Systemic explanation.
4. Practical implications.
5. Risks or failure modes.
6. Leadership conclusion.

For business and leadership audiences, frame AI transformation through:
- organizational operating model;
- architecture of manageability;
- decision systems;
- ownership;
- quality and risks;
- governance;
- role redesign.

For technical audiences, add:
- engineering workflows;
- agentic delivery;
- quality gates;
- CI/CD;
- testing strategy;
- architecture boundaries;
- knowledge layer.

For HR and recruiting audiences, translate technical shifts into:
- observable behaviors;
- hiring criteria;
- onboarding;
- performance management;
- competency models;
- role expectations.

---

# Slide Outline Rules

When editing `talk-outline.md`:
- preserve frontmatter;
- preserve slide numbering unless restructuring is explicitly requested;
- keep each slide focused on one idea;
- include timing when duration is known;
- keep total timing realistic;
- separate "key thought" from supporting theses;
- avoid turning slides into full articles.

Recommended slide block format:

```markdown
## Слайд N. Название

Тайминг: X минут

Ключевая мысль:

...

Тезисы:

- ...
- ...
```

---

# Source Handling

Use `raw-info.md` as the primary local source when it exists.

When adding ideas:
- keep them consistent with the talk goal and audience;
- avoid importing unrelated vault concepts just because they are available;
- preserve Obsidian wikilinks;
- add source links or references when useful.

Do not overwrite raw notes with polished narrative. Raw material and talk structure should remain separate.

---

# Reuse And IP

Talks may become:
- LinkedIn posts;
- client materials;
- frameworks;
- workshop outlines;
- podcast notes;
- articles.

When extracting reusable ideas, prefer atomic notes or dedicated follow-up files rather than bloating the talk outline.

Do not dilute strong proprietary language into generic management vocabulary.

---

# Safety Rules

Never add confidential client details, contracts, legal terms, pricing, or financial data unless explicitly requested.

When a talk is based on client work:
- generalize sensitive examples;
- remove identifying details unless already public;
- preserve strategic insight without exposing private context.

Never mass-delete talk materials.
