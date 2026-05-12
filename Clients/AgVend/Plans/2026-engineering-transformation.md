
| AgVend Engineering Transformation Plan 2026 *From AI-Assisted to AI-Native: Q2–Q4 2026* |
| :-------------------------------------------------------------------------------------- |

# **Why We Are Doing This**

AgVend’s growth ambitions require us to ship more, faster — without growing headcount proportionally. That constraint is not a limitation. It is the forcing function for becoming a better engineering organization.

The companies setting the standard today operate engineering teams that are a fraction of the size of their industry peers, yet consistently out-ship them. These organizations are not doing more with less by working harder. They are structured differently: small, high-agency teams where every engineer owns outcomes end-to-end, AI handles execution, and humans focus on judgment, architecture, and quality.

That is where we are going this year. By end of Q4 2026, AgVend’s engineering org will operate the same way: agents handling the execution of code, tests, and pipelines — engineers owning the outcomes. We will ship more roadmap per engineer than we ever have. We will catch defects earlier and cheaper. And we will do it without a proportional increase in headcount.

| The Primary Goal Grow output without growing headcount. Every initiative in this plan — agentic adoption, shift-left testing, CI/CD automation, role redefinition — serves this objective. More leverage per engineer. More value per sprint. More product in customers’ hands per quarter. |
| :---- |

# **Executive Summary**

This plan covers Q2–Q4 2026\. It addresses three core objectives:

* Get every engineer to Phase 2 agentic fluency — humans orchestrating, not executing — by the end of Q4.

* Eliminate the manual testing bottleneck through shift-left practices, AI-generated test suites, and automated CI/CD quality gates.

* Build a culture of end-to-end ownership where every Engineer is accountable for delivery from ticket inception to production and beyond.

| Core Principle One engineer with agentic tools can now maintain systems that previously required entire teams — not because AI writes perfect code, but because engineers who know how to architect, orchestrate, test, and maintain oversight get 10x leverage. The goal of this transformation is leverage. Every initiative below is designed to unlock it, systematically and safely. |
| :---- |

# **AI Adoption Framework**

All transformation activities are anchored to two phases of AI adoption. The target is 100% at Phase 2 by the end of Q4 2026\.

|  | Phase 1 | Phase 2 |
| ----- | ----- | ----- |
| **Label** | Local Agentic Workflows | Software Factory |
| **What it looks like** | Engineers deploy local CLI agents. Engineers delegate entire tasks, steer the agent through iterative feedback loops. | Humans orchestrating, not executing. Multiple autonomous agents running concurrently across the full SDLC. |
| **Target** | **100% by end of Q3** | **100% by end of Q4** |

# **1\. Role Redefinition**

Effective April 01, 2026\. All roles are formally updated to reflect the agentic era. The titles Engineering Manager, Tech Lead, and Developer remain — the scope of each evolves.

## **Engineering Manager**

The Engineering Manager owns the conditions under which the team does its best work. This means people, process, and organizational context — not technical implementation. In a team of senior engineers, the EM's job is not to direct technical decisions but to ensure the team has clarity, safety, and the absence of friction to move fast and own their work fully.

**PEOPLE**

* Own career development for every engineer on the team: regular 1:1s, growth conversations, promotion cases, and honest feedback that helps people improve

* Identify and address performance issues early — directly, clearly, and with a documented path forward

* Maintain team health: psychological safety, workload balance, and the kind of environment where engineers flag problems rather than hide them

* Own hiring and onboarding for the team; ensure new engineers reach full effectiveness quickly

**DELIVERY & PROCESS**

* Own the team's delivery process — sprint health, delivery speed, dependency management, and removing blockers that engineers cannot remove themselves

* Shield the team from organizational noise; ensure engineers have sustained focus time and are not pulled into meetings or context switches that fragment their work

* Maintain visibility into what the team is building and why — not to micromanage, but to represent the team's work accurately to stakeholders and escalate when priorities conflict

* Surface systemic process problems to leadership before they become delivery failures

**AI ADOPTION**

* Drive phase progression on the team: not by writing agents.md or building skills, but by creating the conditions where engineers invest in these things — recognizing progress, and removing the organizational friction that keeps people from adopting agentic coding.

* Conduct regular adoption checkpoints with each engineer: where they are, what is blocking them, what they need to move forward

* Bring adoption blockers and patterns to the EM sync; translate team-level signals into organizational decisions

* Model the behavior: EMs who have not personally experienced working with agents cannot coach the shift effectively. Demonstrated fluency at the process level — not the technical level — is expected

## **Tech Lead**

Tech Lead ensures that decisions made independently across different ownership zones do not conflict at the system level. In a team of senior engineers, the Tech Lead is first among equals, not a hierarchical authority.

A Tech Lead is a Developer who carries additional architectural responsibility. They write code every day, own a zone of the codebase, work with agents as an executor, and are accountable for their own delivery end-to-end — exactly as every other Developer on the team does. The Tech Lead role adds responsibilities on top of that; it does not replace or reduce them. The majority of a Tech Lead's time is spent writing and shipping code.

**KEY RESPONSIBILITIES**

* Write code daily and own a zone of the codebase: architectural decisions within that zone, code quality, test coverage, and technical debt — the same expectations that apply to every Developer on the team.  
* Track architectural integrity across the system as a whole — not implementation details, but cross-component dependencies and system-wide patterns that no single zone owner has full visibility into.  
* Make the final call in situations where two independent ownership zones cannot reach agreement — not because they know better, but because they hold the mandate.  
* Review a small, targeted set of PRs that carry meaningful business or technical risk — not as a default gate on all code, but as a deliberate, high-judgment intervention where the stakes warrant it. Broad PR coverage is not the expectation. What qualifies as a high-risk PR is defined in collaboration with the Engineering Manager.  
* Provide Engineering Managers with sufficient context to make people and process decisions — without pulling EMs into technical detail.  
* Participate in the AI Enablement Team at the practitioner layer if an active practitioner; otherwise, ensure the conditions for the team's AI Enablement Team representative to do their work effectively. The Tech Lead and the AI Enablement Team representative are not required to be the same person — these are distinct responsibilities that may sit with different engineers depending on the team.

## **Developer**

The Developer is the primary role with full ownership: from the moment a task is received through to its operation in production. In a team of senior engineers, every developer makes implementation decisions independently within their ownership zone and does not seek approval unless a decision crosses its boundaries.

Developer value is measured not by volume of code written but by the quality of decisions made and outcomes delivered to production. The role shifts from "I write correct code" to "I define what correct means in this context" — and encode that into standards, agents.md, and skills within their zone.

**KEY RESPONSIBILITIES**

* Own their area of the codebase fully: architectural decisions within the zone, code quality, test coverage, technical debt

* Make their zone legible to others: documentation, tests, and agents.md should be sufficient for any senior engineer to review a PR, onboard into the area, or continue the work without the owner present. Deep domain knowledge is not a personal asset — it is a team liability if it exists only in one person's head

* Define standards for their zone: what constitutes a correct solution, which patterns apply, which constraints matter — and encode this into agents.md and skills so that agents reproduce these standards consistently

* Work with agents as an executor: formulate tasks with precise context, review output at the level of architectural decisions and edge cases rather than syntax

* When an agent fails on a task it should be able to handle — invest in improving the context (agents.md, skill, agent instruction) rather than completing the task manually. This is part of delivery, not additional work on top of it

* Serve as the final approval gate for all code in their zone — regardless of whether it was written by an agent or a human

* When working on a change that carries meaningful business or technical risk, the Developer is required to seek a formal PR review before merging. That review should come from the Tech Lead, or from another Developer with established expertise in the relevant area.

* Work respectfully within shared zones: when development takes you into a zone owned by another Developer, make a reasonable effort to brief the owner before work begins — share your intended approach, surface relevant constraints, and invite their input. The owner's context on patterns, prior decisions, and known edge cases in that area is institutional knowledge that should inform your work. A formal code review is not required but is encouraged when time permits. This is not a gatekeeping step — it is a courtesy that protects architectural coherence and reduces the risk of undocumented side effects. 

* All PR reviews should take no more than 5–10% of a Developer's time. If it consistently takes longer, something is wrong upstream. Making a PR reviewable is the author's responsibility. If the problem persists — raise it with EM.

## **Quality Engineer (formerly QA Engineer)**

Quality Engineers are test strategists and pipeline owners, not manual testers. They define what to test, design coverage strategies, validate AI-generated test suites, and own the health of the test pipeline. No Quality Engineer should be doing anything in Q3 that an agent can do.

While the primary expectation is that Developers write tests for the code they produce, Quality Engineers are not purely strategic. There are specific, well-defined scenarios where Quality Engineers are expected to write automated tests themselves — and owning that work is part of the role.

**KEY RESPONSIBILITIES**

* Join sprint planning to define acceptance criteria and edge cases before development starts.

* Design test strategies and coverage standards; validate AI-generated test suites for completeness.

* Own the CI/CD test pipeline health: flaky test management, coverage reporting, and quality gate configuration.

* Focus on what agents get wrong: edge case strategy, accessibility compliance, regulatory testing, complex integration scenarios, and exploratory manual testing of high-risk changes that resist automation.

* Own regression test coverage as a living backlog. Quality Engineers are responsible for maintaining a prioritized, continuously updated view of which areas of the product lack sufficient automated coverage — spanning end-to-end, integration, and regression surfaces. This backlog is a first-class artifact, reviewed regularly with the Engineering Manager and developers.

* Write automated tests when the scope warrants it. During Three Amigos sessions, when a feature spans an entire module or a large, interconnected set of functionality, the Quality Engineer may take ownership of building the automated test suite for that scope rather than leaving it distributed across individual Developers. This is a judgment call made during planning, not an exception requiring approval.

* Close historical coverage gaps. Where the codebase carries legacy functionality with insufficient or no automated test coverage, Quality Engineers are responsible for stepping in and building that coverage. This work is prioritized against the regression backlog and treated as delivery work, not optional improvement.

## **System Reliability Engineers (SRE/Production QA)**

System Reliability Engineers own the reliability lifecycle — from proactive detection and structured incident response to post-mortem follow-through and systemic prevention. They are not bug triagers — they are reliability process owners and the internal "customer" of all production quality work. Their core mission: detect problems before customers do, ensure structured resolution, and make sure incidents don't repeat.

As AgVend transitions to an AI-native architecture, this role evolves from manual incident execution toward reliability strategy and AI-augmented operations.

**KEY RESPONSIBILITIES**

* Own the full incident lifecycle: detection → acknowledgement → coordination → resolution → post-mortem → follow-up. Act as first-line on-call and incident coordinator for SEV0–SEV2.

* Own proactive monitoring and alert quality: define what to monitor, set thresholds, eliminate noise, ensure every alert links to a runbook.

* Route Sentry and production bugs into dev teams. SRE owns routing rules and per-team error tracking, not individual triage.

* Facilitate blameless post-mortems, maintain searchable post-mortem database, track action items to closure and escalate when overdue.

* Maintain the runbook catalog for known failure modes.

* Define and track reliability metrics (MTTD, MTTR, incident volume, repeat rate).

* Act as internal "customer" for reliability tasks — SRE creates the requirement, dev teams and DevOps execute. SRE verifies fixes move metrics.

**AI-NATIVE EVOLUTION**

* Curate structured incident data (post-mortems, runbooks, timelines) as the knowledge base for AI-driven reliability tooling.

* Progressively introduce AI-assisted triage: alert correlation, noise reduction, post-mortem similarity search, auto-generated incident briefs. 

* Build self-healing pipelines for known failure patterns, starting with low-risk automation (auto-restart, auto-scale, auto-rollback). 

* Define guardrails for AI-driven actions and maintain human oversight for critical decisions. 

* Long-term: evolve toward a model where AI agents handle detection, diagnosis, and remediation; SRE focuses on system design, resilience planning, and governance.

## **AI-Assisted Design Engineers**

The HTML/CSS specialists are redeployed to use agentic frontend tools to generate UI at scale. They become owners of the design system, component library, and accessibility standards — the highest-leverage use of frontend expertise in an agentic environment. One engineer owns AI-assisted accessibility testing, a gap that agents frequently miss and that carries compliance risk.

## **Technical Product Manager**

The Technical Product Manager (Tech PM) is the primary point of contact between customer needs and engineering execution. They are not responsible for P\&L, portfolio strategy, or go-to-market. They own two things: launching features independently, and enabling Product Managers to launch products.

This distinction matters. For most of AgVend's engineering output — the continuous stream of improvements, enhancements, and feature additions — the Tech PM operates autonomously. For new product launches, they operate in service of the Product Manager, taking the product vision and translating it into everything engineering needs to execute.

**FEATURE OWNERSHIP (Independent Mode)**

When a Tech PM owns a feature or improvement initiative, they are the full operator of that initiative from discovery through delivery:

* Develop a deep understanding of customer needs through direct engagement: review support tickets, join customer calls, synthesize feedback from Customer Success, and identify patterns that signal genuine friction or unmet demand

* Define and articulate the problem before proposing a solution — the Tech PM's job is to be the voice of the customer in every sprint planning conversation, not the author of a feature list

* Translate customer needs into machine-readable Jira requirements: structured user stories, numbered acceptance criteria, explicit scope boundaries, and links to relevant domain context. Requirements must be written so that an agent can parse them and a Developer can act on them without a follow-up conversation

* Maintain a domain glossary that agents and Developers reference when interpreting tickets — reduce ambiguity at the source, not downstream

* Flag and resolve ambiguities before sprint starts, directly in the Jira ticket. Not in Slack. Not in a meeting. In the ticket, so the resolution is traceable

* Own the definition of done from a customer perspective: acceptance criteria are specific, testable, and agreed upon with the Quality Engineer before development begins

**PRODUCT LAUNCH SUPPORT (Partner Mode)**

When a Product Manager is leading a new product launch, the Tech PM operates as their execution partner. The PM owns the vision, the market strategy, and the positioning. The Tech PM owns the decomposition:

* Collaborate with the Product Manager to fully understand the product vision, customer value proposition, and launch goals before any engineering work begins

* Break the product into a coherent, prioritized set of features — not a flat backlog, but a structured decomposition that reflects dependencies, launch sequencing, and MVP boundaries

* Own all Jira issue creation for the initiative: epics, stories, tasks, and subtasks. Every piece of work that touches engineering must exist as a properly structured, fully specified ticket before it enters a sprint

* Act as a point of contact for engineering questions about requirements — the Product Manager should not be pulled into every sprint-level clarification conversations; the Tech PM shields them from that

* Track delivery against the decomposition and surface scope creep, blocking dependencies, or requirement gaps to the Product Manager early — not at the end of the sprint

* Ensure that what ships matches what was promised: acceptance criteria close the loop between product vision and engineering output

**AI-NATIVE OPERATION**

The Tech PM role is the front end of the agentic pipeline. Requirements written by Tech PMs are the primary input layer that agents consume. This means the quality of a Tech PM's Jira output directly determines the ceiling of agentic leverage across the engineering org.

* Write requirements structured for machine consumption: no ambiguous pronouns, no implicit context, no resolution deferred to a Slack thread

* Use agents to draft requirements, acceptance criteria generation, and edge case identification — but own the output. A requirement submitted to engineering is the Tech PM's artifact, regardless of how it was generated

* Maintain and evolve requirement templates and the domain glossary over time — each sprint, these should be more accurate and more complete than the last

* Review agent-flagged ambiguities before sprint starts; every unresolved flag is a future rework event

# **2\. AI Enablement Team**

The AI Enablement Team is AgVend's standing function for AI process, innovation, standards, and adoption across the entire engineering organization. This is not an advisory body. It is the authoritative team that determines how AgVend engineers work with AI — and is accountable for making that transformation real across every squad.

The AI Enablement Team is led by the CTO and composed of all Engineering Managers and a set of key developers selected for demonstrated technical depth and agentic fluency. It meets weekly without exception.

## **Mandate**

The AI Enablement Team owns the full lifecycle of AI-native engineering practice at AgVend: from tracking what is happening in the industry, to defining what AgVend adopts, to ensuring that adoption actually occurs at the team level. Every decision this team makes becomes an organizational standard.

## **What the Team Does**

**INTELLIGENCE AND HORIZON SCANNING**

The team maintains a continuous, structured view of the external landscape — tracking frontier model capabilities, monitoring how leading engineering organizations are structuring human-agent collaboration, evaluating new tooling across the full SDLC, and identifying methodology shifts before they become industry defaults. The output is a living map of what AgVend should be watching, testing, and safely ignoring — reviewed at every weekly meeting.

**TOOLCHAIN GOVERNANCE**

The team owns all tooling decisions for AI-assisted and agentic engineering at AgVend. When a new tool emerges, the team defines the evaluation criteria, runs a structured assessment, and makes the call: adopt, pilot, or pass. This prevents the fragmentation that occurs when squads adopt tools independently, creating incompatible workflows and inconsistent quality.

**PROTOTYPING AND PROOF-OF-CONCEPT WORK**

When something shows enough promise, the team sponsors a time-boxed prototype against a real use case, a real codebase, and a defined success criterion. The goal is a concrete, honest answer to whether something works in AgVend's environment at AgVend's scale. Findings — including failed experiments — are documented and shared with the full engineering org.

**WORKFLOW DESIGN AND PROCESS STANDARDIZATION**

The team designs the workflows that connect tools into a coherent agentic pipeline: how context is structured, where human review is positioned, how handoffs between agents and developers are managed. Once ratified, these workflows are the expected way work gets done — not suggestions.

**STANDARDS DEFINITION AND MAINTENANCE**

The team owns the full body of engineering standards for AI-native development: AGENTS.md requirements, skill library conventions, approved prompt patterns, agent output validation criteria, and quality bars for every artifact the agentic pipeline produces. Standards are versioned and reviewed on a regular cadence.

**SHARED KNOWLEDGE INFRASTRUCTURE**

The team builds and maintains the organizational knowledge layer that makes agents more effective over time: the shared skill library, reusable prompt templates, AGENTS.md blueprints, domain glossaries, and documented agent failure modes with remediation patterns. The team governs what enters this library, ensures it stays current, and retires patterns that no longer reflect how the codebase or models behave.

**AGENT FAILURE ANALYSIS AND CONTINUOUS IMPROVEMENT**

When agents fail in consistent, recurring patterns across squads, the team diagnoses root cause — whether a gap in AGENTS.md, a missing skill, a flawed prompt pattern, or a workflow design issue — and issues fixes that propagate org-wide rather than being solved in isolation.

**ADOPTION ARCHITECTURE AND PHASE PROGRESSION**

The team designs the path from Phase 1 to Phase 2: the prerequisites, the required workflows, the enablement needed, and how progress is measured. Adoption metrics are reviewed weekly. Where squads are stalling, the team identifies whether the blocker is tooling, knowledge, workflow, or organizational friction — and addresses it directly.

**SECURITY, RISK, AND GOVERNANCE**

The team owns the guardrails for agentic operation: what agents are permitted to do autonomously versus what requires human approval, how agent actions are logged and auditable, what security rules are enforced at the agent instruction level, and how the organization's data and IP are protected as external models and tools enter the pipeline.

## **Membership**

The CTO chairs the AI Enablement Team and holds final decision authority on all standards, tooling, and adoption mandates. Engineering Managers are standing members. Key developers are included based on relevance to active explorations and prototyping work; composition may rotate as priorities shift.

## **Engineering Managers as Adoption Owners**

The AI Enablement Team defines what good looks like. Engineering Managers are accountable for closing the gap between that definition and their team's actual behavior. When the team mandates a new standard or workflow, it is the Engineering Manager's job to ensure their team understands it, has the conditions to adopt it, and is moving. Adoption blockers surface at the weekly meeting. Unresolved blockers escalate. Every decision the AI Enablement Team makes has an owner, a target team, a deadline, and an Engineering Manager accountable for delivery.

# **3\. Requirements as Machine-Readable Instructions**

Tech Product Managers are required to write clear, structured requirements. On the engineering side, the transformation is about consuming those requirements well — using agents to translate PM clarity into executable specifications.

The critical insight is that every iteration improves the system itself. Developers encode architectural decisions, patterns, and constraints into agents.md and technical documentation. Quality Engineers encode test strategies and coverage standards into the Test Management System. Over time, the codebase and its surrounding documentation become a machine-readable knowledge base — reducing the amount of human context required for each subsequent task and making each agent interaction more accurate than the last.

The full ownership loop:

| Tech PM | Developer | Quality Engineer |
| ----- | ----- | ----- |
| Writes clear, machine-readable requirements with testable acceptance criteria in Jira. Structures tickets so agents can parse them directly: explicit user stories, numbered acceptance criteria, defined scope boundaries, and links to relevant domain context. Maintains requirement templates and a domain glossary that agents reference when interpreting tickets. Reviews agent-flagged ambiguities before sprint starts and resolves them in the ticket — not in Slack threads. Over time, the PM’s structured Jira output becomes the primary input layer for the agentic pipeline. | Translates requirements into agent-consumable specs by enriching PRD with domain context, constraints, and architectural patterns. Maintains technical documentation as a living knowledge base that agents consume directly. Orchestrates agents against the spec; flags ambiguities before sprint starts. Invests in improving agent context after every failure — the knowledge layer compounds over time. | Validates coverage against original acceptance criteria; owns edge case strategy. Maintains test strategies and coverage standards in the Test Management System as part of shift-left — this is the structured, machine-readable record of what "tested" means for each domain. Ensures agent-generated test suites meet the bar defined in TMS. |

By the end of Q3, this loop is agentic end-to-end: an agent reads the Jira ticket, cross-references acceptance criteria against the codebase, scaffolds the task decomposition, generates tests from the requirements, and flags ambiguities back to the Tech PM before a sprint starts. The human’s role is to review, approve, and decide — not to execute.

This is possible because knowledge accumulates in the system, not in people’s heads. Each sprint, Tech PMs refine requirement templates and domain glossaries in Jira. Developers improve agents.md and technical documentation. Quality Engineers refine test strategies in TMS. The agents read richer context every iteration. By Q4, human involvement in routine implementation is minimal — the engineer’s time is spent on judgment calls, edge cases, and improving the knowledge layer that makes the next cycle faster still.

# 

# **4\. Shift Left & Test Automation**

The fundamental change in how AgVend approaches quality is this: quality is the Developer's job, not QE's job. Shift left means testing happens at the moment code is written, not after it leaves the Developer's hands. QE's role is to define strategy, own the pipeline, and focus on what agents and developers miss — not to be the last line of defense before production.

| What Shift Left Means at AgVend Quality is the Developer’s job, not QE’s job. Quality Engineers validate strategy and coverage — they do not execute manual regression. No ticket is complete without tests. Quality Engineers join sprint planning to define acceptance criteria before development starts, not after. This is the cultural shift that makes shift left real. |
| :---- |

### **What Shift Left Means at AgVend**

Traditional development treats testing as a phase that happens after development is complete. Shift left eliminates that phase. When a Developer writes a function, they write the test for it. When a feature is built, its automated test suite is committed alongside it. Defects are caught at the moment of creation — when they are cheapest and fastest to fix — not days or weeks later when the code has already been reviewed, merged, and forgotten.

This requires a cultural shift as much as a technical one. Developers who have historically handed work to QA for validation need to internalize that the handoff itself is the problem. A ticket is not done when the code works. It is done when the code is tested, the tests pass, and the coverage is committed.

### **Three Amigos: Defining Success Before Work Begins**

For large, complex features, quality cannot be an afterthought — it has to be designed in from the first conversation. This is where the Three Amigos practice comes in.

Before any complex feature enters development, three people get in a room: the **Tech Product Manager**, the **Quality Engineer**, and the **Developer**. Each brings a distinct lens:

The **Tech Product Manager** comes with the business intent — what problem are we solving, what does success look like for the customer, what are the edge cases that would make this feature fail in the real world even if it technically works.

The **Quality Engineer** comes with a testing strategy — what are the highest-risk areas of this feature, what scenarios are agents and automated tests likely to miss, where does human judgment need to be applied, and what does the acceptance criteria need to say for this feature to be considered shippable.

The **Developer** comes with technical reality — what does the architecture look like, where are the integration points that could break, what dependencies exist, and what is actually testable given the implementation approach.

The output of a Three Amigos session is not a meeting summary. It is a concrete testing strategy attached to the feature before a single line of code is written: acceptance criteria that are specific and testable, a list of edge cases that must be covered, clarity on which scenarios will be automated versus require human validation, and agreement on what "done" looks like. This becomes the contract that the Developer builds against and the Quality Engineer validates against.

Three Amigos is not a process for every ticket. It is reserved for features that are large, complex, cross-service, or carry meaningful risk. The Tech Lead and Engineering Manager identify which features warrant it during sprint planning.

### 

### **Automation and the Developer's Role**

Developers write tests. Not as a separate activity after the feature is built, but as part of building it. The expectation going forward is that every PR includes the tests for the code it introduces. Agents are a tool in this process — Developers use agentic tools to generate test suites and validate coverage — but the Developer owns the output. Accepting agent-generated tests without review is the same as accepting agent-generated code without review: the engineer is always the final gate.

The CI/CD pipeline enforces this. Quality gates on every PR make it immediately visible when tests are missing, when coverage has weakened, or when an agent has deleted a failing test instead of fixing it. These are not suggestions — they are hard gates that block merge.

For the transition period, the QE team will own the catch-up work on existing test coverage gaps in the codebase. That work is separate from the forward-looking expectation: from this point on, new code ships with tests written by the Developer who wrote it.

### 

### **The CI/CD Quality Pipeline**

Testing is embedded inside the pipeline, not downstream of it. Every PR triggers automated unit and integration tests, static analysis, linting, and AI code review. The full suite runs on merge to main. Diff-aware test execution ensures that CI runs only the tests relevant to a given change on PRs, keeping pipeline time fast without sacrificing coverage signals.

As the pipeline matures, self-healing test infrastructure detects flaky tests, clusters them by root cause, and generates remediation PRs for human review. Engineers are notified for final decisions — they are not the first responder to every test failure.

The Quality Engineer owns the health of this pipeline: the configuration of quality gates, the coverage reporting, the flaky test strategy, and the tooling that makes it all visible. Developers feed it. Quality Engineers govern it.

# **5\. QA Team Transformation**

Reduce from 22 manual/automation QA to 1 Quality Engineer per Squad. The 4 SRE/Production QA engineers are excluded from this transition and evolve on a separate Platform Reliability track.

| Quality Bar Release Defect Rate must improve quarter-over-quarter throughout the transition. This metric is tracked monthly by the CTO and Engineering Managers specifically in the context of this transition. |
| :---- |

## **Timeline & Role Paths**

### **Q2: Clarity for Everyone**

Engineering Managers hold individual conversations with every QA team member by the end of April. Leadership already has a clear picture of who is excited to make the shift and who will not. Every person leaves that conversation with a documented role path:

* Quality Engineer path: confirmation of selection, training plan, and Q3 milestone expectations

* Exit: for those who will not make the shift, a clear timeline and transition support

### **Criteria for Quality Engineer Selection**

Quality Engineers are selected on the following dimensions:

| Dimension | What to look for |
| ----- | ----- |
| **Test strategy thinking** | Can they design coverage strategy, not just execute test cases? Do they think about edge cases proactively? |
| **AI tool aptitude** | Are they already using AI tools? Can they evaluate AI-generated test suites critically? |
| **Automation mindset** | Do they gravitate toward removing manual work, or toward executing it? |
| **Communication** | Can they work upstream with Tech PMs and Tech Leads to define acceptance criteria, not just validate them? |

### **Q2–Q3: Skill Development for Quality Engineers**

Quality Engineers are expected to develop proficiency across two tracks on their path to the new role:

* Test Automation Engineering: Playwright, Integration API testing, CI/CD pipeline configuration, coverage tooling

* Agentic Quality Strategy: How to prompt agents to generate test suites, how to evaluate AI-generated tests for completeness, how to detect and remediate common agent failure modes in tests

This is not a formal training program — it is a demonstration of capability. Quality Engineers are expected to show measurable progress against these tracks by the end of Q3. Engineering Managers assess readiness and provide guidance, but the initiative to develop these skills sits with the individual.

### **Q3: Transition Complete**

By the end of Q3, the Quality Engineers are operating as pipeline owners and test strategists. Manual regression testing for core service flows has been replaced by automated coverage. Remaining transitions are complete. Platform Reliability engineers are operating with expanded observability and deployment oversight capabilities.

# 

# **6\. CI/CD & Infrastructure**

The infrastructure foundation is strong: 100% containerized, 95% IaC via Terraform/Helm, AWS/k8s, CircleCI pipelines already running. The gaps to close are feature flags, ephemeral staging environments, and rollback capability.

## **Q2 Actions**

* Feature flags across all services: decouple deployment from release. New features deploy to production but remain hidden until explicitly enabled. This enables continuous delivery without continuous risk.

* Per-branch ephemeral preview environments: noted as possible in the current setup — make it standard practice for every PR.

* Diff-aware test execution: only tests relevant to a given commit run in CI on PRs. Full suite on merge-to-main.

## **Q3 Actions**

* Automated rollback: the current absence of rollback is a growing risk as deployment frequency increases. Implement tag-based rollback with automated smoke tests post-deploy.

* Self-healing pipeline: automated vulnerability detection, flaky test clustering, AI-assisted remediation with PR submission for human approval. Engineers are the decision gate, not the first responder.

* Deployment frequency target: multiple times per week per service.

## **Q4 Target State**

* Daily deployments to production for the main monolith.

* Platform Reliability engineers own deployment health monitoring end-to-end.

* Self-healing CI is active across all core services.

# **7\. Sprint Cadence & Delivery Model**

## **Ticket Decomposition**

No ticket exceeds 5 days of effort (20 Jira points maximum). Agentic teams compress implementation time; ticket sizing must reflect this. Developers own decomposition quality during sprint planning. Engineering Managers track and enforce it.

## **Updated Definition of Done**

A ticket is done when all of the following are true:

* Code is merged

* Agent-generated tests are committed and passing

* Coverage threshold is met (PR gate enforces this)

* Feature is deployed to staging

* Acceptance criteria validated against Tech PM requirements

* Architectural decision record or usage guide updated if applicable (Context-First DoD)

# **8\. Metrics Dashboard**

| \# | Metric | What it measures | Q3 Target | Q4 Target |
| :---: | ----- | ----- | :---: | :---: |
| **1** | **AI Phase Level per engineer** | Are we actually transforming? Manager-assessed quarterly with engineer input and evidence. | 0% at Phase 1 | 100% at Phase 2 |
| **2** | **Test Coverage % (integration, UI E2E)** | Is automation replacing manual QA? Tracked per surface, not as a blended average. | 50% coverage | 80%+ coverage |
| **3** | **Product Value Points** | Are we delivering more, faster? As agentic adoption matures, total Product Value points go up. | Measurable improvement QoQ | Measurable improvement QoQ |
| **4** | **Ticket Reopen Rate** | Are Developers owning quality end-to-end? High reopen rate \= quality still being offloaded to QE. | Baseline established | Declining QoQ |
| **5** | **Deployment Frequency** | Is faster delivery actually reaching production? Currently: bi-weekly / ad hoc. Target: multiple times per week. | Weekly per service | Multiple times/week |
| **6** | **Release Defect Rate** | Release Defect Rate \= production bugs opened within 7 days of a release ÷ tickets shipped in that release | No change / improvement over Q2 | Improvement over Q3 |
| **7** | **PR Lead Time (Time to Merge)** | Time from first commit (or PR creation) to merge. | \<48h | \<24h |

