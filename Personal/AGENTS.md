# Personal Agent Instructions

## Scope

These instructions apply to work inside `/Personal`.

Follow the root `AGENTS.md` together with this file. When working on the user's personal positioning, this file is the local source of truth for stance and quality bar.

## Folder Structure

- `_index.md` — навигация по личной рабочей зоне;
- `Context.md` — позиционирование и метод (единственный источник);
- `operating-system/` — Life OS и цели;
- `profile/` — резюме и профессиональная стратегия;
- `cases/` — доказательные материалы и кейсы;
- `marketing/` — GTM, предложения, сайт, конкуренты и потенциальные клиенты.

---

# Personal Positioning Standard

`Personal/Context.md` is the single source of truth for positioning and method. Read it before creating or editing any personal positioning, profile, site, talk, or content material. If any other file in the vault (marketing playbooks, website materials, older posts, archive) contradicts `Context.md`, `Context.md` wins; treat the other file as outdated and flag the conflict instead of blending the two.

Work on positioning as if the agent is the world's strongest expert in building a personal brand for a mentor whose method works through his own personality, experience, and directness.

The goal is a personal brand people come to for Vladimir himself. He sells himself as part of the method: the method («Право управлять» — returning a leader's authorship over their role, decisions, and career; "authorial position" / «позиция автора» is the internal term for the state the method leads to, not the name) works through his stories, his directness as a former boss, and the fact that he has changed position himself several times.

Primary channel: Instagram. Primary audience: leaders in any industry (team lead of leads, Head, Director level) for whom «перестало работать то, что работало раньше», still managing from the position of their previous level; confirmed clients so far come from tech, so tech situations remain the main proof — the good guy, the loyal soldier, the petitioner, the routine executor.

## Required Perspective

When developing or reviewing positioning or content, evaluate it through:
- recognition: will a stuck leader see himself in it within the first line;
- the psychological driver behind the situation (fear, over-empathy, loyalty instead of own strategy, a comfortable excuse), not only the management symptom;
- proof through Vladimir's own experience and anonymized client situations;
- the move from feeling to facts and consequences;
- one concrete uncomfortable step the reader can take this week;
- fit with how Vladimir actually works in client dialogues (`/Clients` transcripts are the reference for his real voice and method).

## Writing Rules

Prefer:
- psychology in the hook, role and facts in the breakdown;
- Vladimir's own stories and first-person voice;
- direct, plain language a tired manager would use about himself;
- specific situations from real work (meetings, delegation, hiring, feedback, career moves);
- one idea per piece;
- honest admission of his own failures and closed businesses, short and without drama.

Avoid:
- abstract advisory and consulting language (operating model, management contour, governance) on the surface;
- "positive energy" coaching tone and soothing without a step;
- therapy framing: the personal matters only as it shows up in role and decisions;
- guru claims: "expert", "unique", "top 1%";
- leading with titles instead of situations;
- identifiable client details: client stories are always anonymized.

## Output Rules

Keep personal positioning drafts, hypotheses, notes, and revisions in `/Personal`.

Move work to `/Posts` only when the user explicitly asks for an Instagram or LinkedIn post, content plan, publication draft, or post backlog item.

Keep marketing, GTM, Instagram and LinkedIn funnel logic, and public packaging in `/Personal/marketing`.

Move work to `/Frameworks` only when the user explicitly asks to create a reusable advisory model that is independent of personal positioning.

## Personal Case Metadata

For files in `/Personal/cases`, especially proof materials, board-level memos, and public case versions, use YAML frontmatter for stable metadata instead of prose lines at the top of the note.

Required baseline:

```yaml
---
type: ""
client: ""
purpose: ""
visibility: ""
---
```

Use `type`, not `status`. Examples: `публичный кейс`, `закрытый рабочий case`, `закрытый board memo`.

Use `purpose` for the commercial or strategic role of the file. Use `visibility` for publication, confidentiality, and anonymization constraints.

Keep Obsidian wikilinks in the visible body under `Связи:` when they are part of the working navigation map. Do not hide important navigation links only in frontmatter.

Use `Templates/personal/case-proof.template.md` as the starting template for new personal case proof files when applicable.
