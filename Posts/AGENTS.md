# LinkedIn Writing Instructions

## Purpose

This folder is the editorial system for LinkedIn content.

Use it to:
- find strong topics;
- turn notes and meeting insights into posts;
- plan publication rhythm;
- track performance;
- keep LinkedIn content aligned with advisory positioning.

## Editorial System

Use files by role:
- `Context.md` – positioning, audience, content logic, strategic constraints.
- `themes-backlog.md` – raw observations, funnel topics, tensions, client-derived insights.
- `series-map.md` – weekly series, funnel sequencing, anti-duplication logic.
- `content-calendar.md` – dates, funnel type, topic, status, links.
- `drafts/` – posts being prepared.
- `published/` – posts already published.
- `research/high-performing-posts.md` – proven patterns and reference corpus.

Default workflow:
1. Read `Context.md` for positioning and audience.
2. Check `themes-backlog.md` for available topic raw material.
3. Check `series-map.md` for current or future series.
4. Check `content-calendar.md` for planned dates and status.
5. Check `drafts/` and `published/` to avoid repeating posts.
6. Use `research/high-performing-posts.md` for patterns, not for copying wording.

Do not use `content-calendar.md` as a backlog.
Do not use `themes-backlog.md` as a publishing plan.
Do not put raw topic dumps into `AGENTS.md`.

## Post Status Workflow

When changing a post status, update all relevant editorial artifacts in one pass:

1. Update `content-calendar.md`:
   - find the row by `publish_date`, topic, or wikilink;
   - change the `Status` column to the requested status.
2. Move the post Markdown file between folders when status changes imply a folder change:
   - `draft` or `ready` posts belong in `drafts/`;
   - `published` posts belong in `published/`.
3. Update the post Markdown frontmatter:
   - set `status:` to the same value as in `content-calendar.md`;
   - preserve existing `publish_date`, `funnel`, `source`, `audience`, and other metadata;
   - if a published post has a known LinkedIn URL, add or update `linkedin_url:`.

Do not leave calendar status, folder location, and post frontmatter out of sync.
When moving files, preserve the filename and Obsidian wikilinks.

## Series Planning

Plan posts in series by default.

Minimum series:
- 1 week;
- 3 posts;
- [[Frameworks/marketing/linkedin-gtm-playbook#TOFU верхний этап контентной воронки|TOFU]], [[Frameworks/marketing/linkedin-gtm-playbook#MOFU средний этап контентной воронки|MOFU]], [[Frameworks/marketing/linkedin-gtm-playbook#BOFU нижний этап контентной воронки|BOFU]];
- Monday, Wednesday, Friday rhythm.

Before planning a week:
- choose one primary series from `series-map.md`;
- check whether an existing series should continue;
- select one [[Frameworks/marketing/linkedin-gtm-playbook#TOFU верхний этап контентной воронки|TOFU]], one [[Frameworks/marketing/linkedin-gtm-playbook#MOFU средний этап контентной воронки|MOFU]], and one [[Frameworks/marketing/linkedin-gtm-playbook#BOFU нижний этап контентной воронки|BOFU]];
- update `content-calendar.md` only after the sequence is coherent;
- keep unused topics in `series-map.md` or `themes-backlog.md`.

Every planned week should answer:

> What changes for the reader after these three posts?

## Anti-Duplication

Before adding or planning a topic, check:
- `content-calendar.md`;
- `series-map.md`;
- `themes-backlog.md`;
- `drafts/`;
- `published/`.

Acceptable reuse:
- developing the same series on the next week;
- moving from [[Frameworks/marketing/linkedin-gtm-playbook#TOFU верхний этап контентной воронки|TOFU]] observation to [[Frameworks/marketing/linkedin-gtm-playbook#MOFU средний этап контентной воронки|MOFU]] framework;
- moving from [[Frameworks/marketing/linkedin-gtm-playbook#MOFU средний этап контентной воронки|MOFU]] framework to [[Frameworks/marketing/linkedin-gtm-playbook#BOFU нижний этап контентной воронки|BOFU]] advisory review;
- returning to a theme through a different management object: CTO, EM, product, quality, data, AI adoption.

Avoid:
- same thesis with different wording;
- same conflict without a new management conclusion;
- repeated [[Frameworks/marketing/linkedin-gtm-playbook#BOFU нижний этап контентной воронки|BOFU]] offer without a new diagnostic angle;
- several posts in a row about the same pain without funnel progression.

## Language

Russian is preferred unless explicitly requested otherwise. Use the canonical language policy and glossary from the root `AGENTS.md`.

For Russian LinkedIn posts:
- keep English terms only when they are intentionally used as part of the author's positioning, source fidelity, or public content format;
- apply the glossary especially strictly to casual `insights`, `action items`, `framework`, `workflow`, and `ownership`.

## Style

Use:
- clear systemic thinking;
- concise executive language;
- short paragraphs;
- analytical tension;
- operational conclusions.

Avoid:
- motivational tone;
- startup hype;
- engagement bait;
- generic consulting language;
- emojis;
- excessive explanations.
- the word "разрыв" in LinkedIn posts.

Punctuation:
- prefer "–" over the long dash in LinkedIn posts.

## Post Structure

Preferred structure:
- strong hook;
- tension/problem;
- core insight;
- practical conclusion;
- soft CTA when appropriate.

## Post Generation Workflow

Default input:
- voice note;
- transcript;
- summary;
- source note.

When generating a post from source material, produce the preparation layer first:
- hook;
- core insight;
- tension;
- practical conclusion;
- CTA.

Do not treat the first generated version as final copy.

Human editing is expected after generation:
- add personal position;
- remove generic phrases;
- sharpen the argument;
- verify truthfulness.

Final editorial pass will be added later.

## Funnel Logic

Always classify posts using the funnel notes:
- [[Frameworks/marketing/linkedin-gtm-playbook#TOFU верхний этап контентной воронки|TOFU]]
- [[Frameworks/marketing/linkedin-gtm-playbook#MOFU средний этап контентной воронки|MOFU]]
- [[Frameworks/marketing/linkedin-gtm-playbook#BOFU нижний этап контентной воронки|BOFU]]

## Topic Selection

Prioritize topics that:
- connect to AI transformation, engineering management, organizational design, CTO/CEO advisory, decision systems, ownership clarity, архитектура управления, operating model, quality and risks;
- emerge from real client patterns or repeated leadership problems;
- can be written without disclosing confidential information;
- support long-term positioning, not only reach.

## High-Performing Reference Corpus

Before planning, drafting, or editing LinkedIn posts, consider:
- `Posts/research/high-performing-posts.md`

Use it to:
- identify topics and formats that already generated reach, comments, and strategic signal;
- reuse proven structural patterns for hooks, tension, systemic insight, and conclusions;
- compare new ideas against posts that already worked;
- plan content around repeatable patterns, not isolated lucky posts;
- preserve advisory positioning while improving performance.

When planning the content calendar:
- include successful patterns from the reference corpus as one input into topic selection;
- balance proven formats with new strategic themes;
- do not optimize only for reach if the topic weakens positioning;
- extract the pattern, not the wording.

## Confidentiality

Do not reveal client names, sensitive details, private meeting content, commercial terms, legal content, or financial information unless explicitly approved.

When using client-derived insights, generalize:
- role instead of person;
- pattern instead of event;
- structural issue instead of private detail.
