# Knowledge Agent Instructions

## Purpose

This repository is a strategic advisory knowledge system focused on:
- AI transformation
- engineering management
- organizational design
- CTO/CEO advisory
- decision systems
- architecture of manageability

The repository is an intellectual property asset.

---

# Philosophy

Main focus:
- system management & governance
- architecture over heroics
- management over micromanagement
- ownership over control
- organizational operating models
- ownership clarity
- decision systems

Prefer:
- structural thinking
- repeatable systems
- organizational leverage

Avoid:
- motivational tone
- startup hype
- generic consulting language
- generic management language
- excessive explanations

---

# General Rules

- Preserve Markdown formatting.
- Preserve Obsidian wikilinks.
- Never mass-delete files.
- Never rename folders unless explicitly instructed.
- Prefer incremental edits over destructive rewrites.
- Keep writing concise, structured, and executive-oriented.
- Consider relevant `Context.md` files before creating, editing, or summarizing materials.

## Context Efficiency

Use the smallest reliable context set for the task.

Default exclusions unless explicitly needed:
- `.obsidian/`
- `.git/`
- `node_modules/`
- `.DS_Store`
- `package-lock.json`
- raw Telegram JSON files in `Posts/research/telegram/raw/` and `Posts/research/telegram/normalized/`
- PDF binaries in `sources/` when a processed Markdown note already exists

Prefer indexes and search before opening many files:
- use `rg` for anti-duplication and source discovery;
- use `Posts/content-index.md` before scanning `Posts/drafts/` or `Posts/published/`;
- use `Posts/research/high-performing-posts-index.md` before opening the full reference corpus;
- open full source files only when writing, fact-checking, updating status, or resolving ambiguity.

## Instruction Hierarchy

- Root `AGENTS.md` defines vault-wide rules.
- Local `AGENTS.md` files add folder-specific rules and should be followed together with the root file.
- `Context.md` files contain working context, positioning, audience, and constraints for the relevant folder or client.
- When rules conflict, prefer the more specific local instruction unless it weakens confidentiality, safety, or language quality.

## Что агент умеет делать на основе skills

В этом vault есть локальные skills в `.agents/skills/`. Если запрос пользователя совпадает с одной из возможностей ниже, агент должен использовать соответствующий skill и следовать его `SKILL.md`, а не придумывать процесс заново.

Доступные рабочие процессы KnowledgeOS:

- `transform-html-to-md` — преобразовать HTML-транскрипт встречи в `transcript.md`, создать правильную папку встречи, определить клиента или менти, если это возможно, сохранить содержание транскрипта и нормализовать имена спикеров.
- `summarize-meeting` — создать краткий executive-style `summary.md` по `transcript.md`, используя клиентский контекст, наблюдения об управленческом росте, главные выводы, действия и следующие шаги.
- `import-pdf-report` — превратить PDF-отчет в краткую русскоязычную source note для базы знаний: извлечь важные модели, цифры, графики, риски и advisory-выводы, затем проверить заметку против источника.
- `create-telegram-weekly-digest` — собрать недельные сигналы из настроенных Telegram-каналов, отфильтровать их через advisory-позиционирование и создать Markdown digest в `Posts/research/telegram/weekly-digests/`.
- `import-linkedin-posts` — импортировать или обновить опубликованные LinkedIn-посты и аналитику в `Posts/published`, избежать дублей и обновить `Posts/metrics.md`.
- `prepare-post-ideas-digest` — подготовить в чат сводку идей для LinkedIn-постов на основе последних клиентских `summary.md`, Telegram digest и/или указанных пользователем источников; по каждой идее показать тезисы, смыслы, стадию воронки [[linkedin-gtm-playbook#TOFU верхний этап контентной воронки|TOFU]]/[[linkedin-gtm-playbook#MOFU средний этап контентной воронки|MOFU]]/[[linkedin-gtm-playbook#BOFU нижний этап контентной воронки|BOFU]] и готовность к добавлению в `Posts/themes-backlog.md`.
- `apply-typograf` — запускать npm-пакет `typograf` по выбранному Markdown/TXT-файлу или папке, предварительно проверять dry-run и сохранять Markdown-разметку, Obsidian wikilinks, ссылки, кодовые блоки и frontmatter.

Правила использования этих возможностей:

- Если пользователь просит один из этих рабочих процессов, выполнить его end-to-end, когда это возможно.
- Сначала прочитать файл skill, затем релевантные `AGENTS.md` и `Context.md`.
- Сохранять исходные материалы: не переписывать транскрипты, raw notes или импортированные посты, если skill прямо не требует трансформации.
- В финальном ответе указывать созданные или измененные файлы.
- Не добавлять идеи в `Posts/themes-backlog.md` без явного решения пользователя.
- Если skill требует credentials, browser login, Telegram authorization, network access или отсутствующий source file, останавливаться только в точке, где нужно действие пользователя, и объяснять точный следующий шаг.

---

# Writing Style

Russian is the default language for generated notes, summaries, posts, frameworks, and client materials.

Preferred style:
- clear
- systemic
- analytical
- high signal-to-noise ratio
- minimal fluff

Avoid:
- motivational tone
- startup hype
- generic consulting language
- excessive explanations

Use:
- short sections
- bullets
- frameworks
- operational language

---

# Russian Language And Terminology

This is the canonical language policy for the vault. Local `AGENTS.md` files may add audience-specific exceptions, but should not duplicate the full glossary.

For Russian-language files:
- Use Russian for concepts, headings, explanations, summaries, recommendations, and conclusions.
- Avoid unnecessary English terms when a precise Russian equivalent exists.
- English terms require a reason: product names, company names, role titles, direct quotes, metrics, system names, internal company terminology, established technical terms without a good Russian equivalent, or intentionally preserved source terminology.
- If an English term is important for precision or audience context, introduce it once in parentheses and then continue in Russian.
- Do not mix English and Russian casually inside one sentence.
- Prefer mature Russian management language over consulting slang.

## Preferred Translation Glossary

Translate these English terms by default:

- strategy → стратегия
- execution → исполнение / реализация
- ownership → зона ответственности / владение
- accountability → ответственность
- alignment → согласованность
- governance → управление / управленческий контур
- operating model → операционная модель
- decision-making → принятие решений
- stakeholder / stakeholders → участник / заинтересованная сторона / стейкхолдеры
- roadmap → план развития / дорожная карта / роудмеп
- insight / insights → вывод / наблюдение
- action item / action items → действие / следующие шаги
- framework → модель / рамка / фреймворк
- workflow → процесс / порядок работы
- process → процесс
- role → роль
- scope → рамка / объем / зона
- mandate → мандат
- capability → способность / компетенция / возможность
- capacity → пропускная способность команды / доступный ресурс
- business value → ценность для бизнеса
- data → данные, except when referring to a named function, team, product, or established technical term
- compliance → комплаенс / регуляторный контур / соблюдение требований
- value proposition → ценностное предложение
- performance → результативность / производительность
- delivery → поставка / реализация / delivery, when used as established engineering term
- quality gates → контрольные точки качества / quality gates, when used as engineering practice
- feedback loop → контур обратной связи
- escalation path → путь эскалации / порядок эскалации
- risk management → управление рисками
- change management → управление изменениями
- transformation → трансформация
- adoption → внедрение / принятие
- enablement → поддержка внедрения / создание условий
- playbook → рабочая инструкция / сценарий / playbook, when used as artifact type
- checklist → чеклист / контрольный список
- summary → резюме / краткое содержание
- narrative → логика изложения / нарратив
- positioning → позиционирование
- engagement → взаимодействие / вовлечение / клиентская работа, depending on context

## Terms To Keep In English

Keep English when translation would reduce precision, break source fidelity, or conflict with established usage:

- Product, company, and platform names: `LinkedIn`, `OpenAI`, `AutoDS`, `AgVend`, `Obsidian`.
- Role titles when they are formal titles or client terminology: `CTO`, `CEO`, `Engineering Manager`, `Product Manager`.
- Technical and engineering abbreviations: `API`, `CI/CD`, `SLA`, `SLO`, `KPI`, `OKR`, `GDPR`.
- AI and engineering terms without a stable Russian equivalent: `AI-native`, `agentic`, `prompt`, `LLM`, `RAG`.
- Direct quotes, source terminology, and internal company language.
- Public content funnel labels: [[linkedin-gtm-playbook#TOFU верхний этап контентной воронки|TOFU]], [[linkedin-gtm-playbook#MOFU средний этап контентной воронки|MOFU]], [[linkedin-gtm-playbook#BOFU нижний этап контентной воронки|BOFU]].

When keeping an English term, do it intentionally and consistently. Do not leave English in Russian text by inertia.

---

# Vault Structure

Main folders:

- /Personal — private working notes, personal operating system, reflections, goals, and non-client knowledge.
- /Clients — client-specific advisory materials, meeting notes, transcripts, strategy documents, and engagement context.
- /Templates — reusable structures for notes, meetings, summaries, posts, client work, and repeatable knowledge workflows.
- /Posts — LinkedIn and public writing pipeline, including drafts, published posts, and post analytics.
- /Frameworks — reusable intellectual property: models, concepts, decision systems, operating models, and advisory frameworks.
- /Talks — public talks, conference presentations, webinars, speaking materials, and related preparation notes.

Do not create new top-level folders unless explicitly requested.

## Personal Positioning

Work about the user's personal positioning belongs in `/Personal`.

This includes:
- personal expert positioning;
- professional role and advisory stance;
- personal value proposition;
- positioning hypotheses, revisions, and strategic self-description.
- personal advisory cases and proof materials, which belong in `/Personal/cases`.
- positioning, GTM, LinkedIn funnel logic, and public expert packaging, which belong in `/Personal/marketing`.

Use `Personal/marketing` as the source of marketing logic, GTM thinking, LinkedIn funnel logic, and public positioning rules.

Use `/Personal/marketing/competitors` for competitive analysis connected to positioning, category definition, offer language, GTM logic, and LinkedIn angles.

Keep `/Personal/cases` as the place for personal advisory cases and proof materials.

Do not put working materials about personal positioning in `/Posts` or `/Frameworks` unless the user explicitly asks to create:
- a public LinkedIn draft or publication artifact, which belongs in `/Posts`;
- a reusable advisory model unrelated to personal positioning, which belongs in the most specific `/Frameworks` area.

When preparing LinkedIn themes or drafts, connect personal positioning from `/Personal` with the rules from `Personal/marketing`, while keeping the publishing workflow in `/Posts`.

## Frameworks Structure

`/Frameworks` contains reusable intellectual property, source notes, and advisory models. Treat this folder as the system of record for repeatable concepts, not as a dumping ground for temporary research.

Current framework areas:

- `/Frameworks/ai-transformation` — AI transformation models, AI-native organization materials, internal developer platform notes, and source notes from AI/engineering reports. Keep original PDFs and source documents in `/Frameworks/ai-transformation/sources`.
- `/Frameworks/governance` — management systems, decision systems, organizational operating models, architecture of manageability, quality and risks, systemic management, and related governance models. Use `/Frameworks/governance/sources` for source materials and `/Frameworks/governance/cobit` for COBIT-specific materials.

Marketing, public positioning, LinkedIn GTM, and funnel-stage definitions live in `/Personal/marketing`, because they are rules of personal positioning rather than reusable advisory frameworks.

When creating or updating framework materials:

- Put reusable advisory models in the most specific existing framework folder.
- Put imported reports and source-based summaries near the topic they support, not in `/Posts` or `/Clients`.
- Preserve links from source notes to related framework concepts using Obsidian wikilinks.
- Do not create new framework subfolders unless the existing areas do not fit and the user intent is explicit.
- Keep framework notes concise, durable, and reusable across clients.

---

# LinkedIn Post Format

Use `Posts/AGENTS.md` and `Posts/Context.md` as the source of truth for LinkedIn planning, drafting, status changes, funnel logic, and editorial constraints.

Vault-wide baseline:
- strong hook;
- tension/problem;
- systemic insight;
- practical conclusion;
- no emojis, engagement bait, or generic inspiration.

---

# Diagram Rules

Use Mermaid when possible.

Preferred diagrams:
- org structures
- decision flows
- responsibility systems
- escalation paths

---

# Markdown Conventions

Use:
- kebab-case filenames
- concise note titles
- atomic notes

Navigation files for folders should be named `_index.md`.

User-facing Obsidian templates should live in `/Templates` and use the suffix `.template.md`, for example `lead-card.template.md`. Technical templates inside `.agents/skills/...` belong to workflow automation and should not be moved for this rule alone.

Avoid:
- FINAL_v2_FINAL naming
- duplicate notes
- large unstructured documents

---

# AI Transformation Terminology

Preferred terms:
- AI-native organization
- architecture of manageability
- decision systems
- organizational operating model
- quality and risks
- systemic management

Avoid generic buzzwords.

---

# Safety Rules

Never modify:
- contracts
- legal documents
- financial documents

without explicit approval.
