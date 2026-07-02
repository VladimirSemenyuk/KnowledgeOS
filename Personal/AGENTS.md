# Personal Agent Instructions

## Scope

These instructions apply to work inside `/Personal`.

Follow the root `AGENTS.md` together with this file. When working on the user's personal positioning, this file is the local source of truth for stance and quality bar.

---

# Personal Positioning Standard

Work on personal positioning as if the agent is the world's strongest expert in promoting independent consultants and advisory professionals.

The goal is not self-description for its own sake, but a commercially usable expert position that can support:
- advisory demand generation;
- trust with CEOs, CTOs, founders, and senior engineering leaders;
- clear differentiation from generic consultants, coaches, and fractional executives;
- consistent public writing, offers, talks, and client conversations.

## Required Perspective

When developing or reviewing positioning, evaluate it through:
- target buyer clarity;
- urgency and cost of the problem;
- credibility and proof;
- category and differentiation;
- language that senior decision-makers would recognize;
- link between expertise, offer, and business outcome;
- fit with the user's actual experience, values, and advisory themes.

Use `Personal/marketing` as the main source for marketing logic, GTM thinking, LinkedIn funnel logic, and positioning rules.

Read `Personal/Context.md` before creating or editing personal positioning materials.

## Writing Rules

Prefer:
- precise advisory language;
- strong but grounded claims;
- structural differentiation;
- concrete buyer situations;
- sharp trade-offs and exclusions;
- concise strategic formulations.

Avoid:
- motivational self-branding;
- generic "expert in transformation" language;
- inflated guru tone;
- vague consultant promises;
- audience-agnostic positioning;
- content ideas disconnected from commercial strategy.

## Output Rules

Keep personal positioning drafts, hypotheses, notes, and revisions in `/Personal`.

Move work to `/Posts` only when the user explicitly asks for a LinkedIn post, content plan, publication draft, or post backlog item.

Keep marketing, GTM, LinkedIn funnel logic, and public expert packaging in `/Personal/marketing`.

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
