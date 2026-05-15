# Инсайты о том, как AI-преобразование меняет организацию и роли

Источник: клиентские встречи, summary в `Clients` и [[2026-engineering-transformation]] на 2026-05-15.

---

# Короткий вывод

AI-преобразование в AgVend — это не внедрение инструментов поверх старой engineering-модели.

Это переход к AI-native operating model, где:

- AI берет execution layer;
- люди отвечают за judgment, архитектуру, качество и governance;
- требования, кодовая база, тестовые стратегии и документация становятся machine-readable system;
- роли меняются вокруг end-to-end ownership;
- организация растит output без пропорционального роста headcount.

Главный сдвиг: AI повышает требования к управляемости. Чем больше execution отдается агентам, тем важнее ясные роли, стандарты, контекст, quality gates и ownership.

---

# 1. AI-native модель меняет источник leverage

## Наблюдение

Цель AgVend — увеличить output без пропорционального роста команды.

Это достигается не за счет "работать больше", а за счет новой модели:

- инженеры оркестрируют агентов;
- агенты выполняют кодинг, тесты и pipeline-work;
- люди принимают решения, проверяют качество и улучшают системный контекст.

## Системный инсайт

AI leverage возникает не от самого факта использования инструментов.

Он появляется, когда организация перестраивает:

- роли;
- Definition of Done;
- требования;
- engineering standards;
- тестирование;
- CI/CD;
- governance.

Без этого AI остается локальным productivity tool, а не организационным operating model.

---

# 2. EM становится владельцем adoption conditions

## Наблюдение

Engineering Manager в AI-трансформации не должен писать за инженеров `AGENTS.md`, skills или технические инструкции.

Его зона:

- создавать условия для adoption;
- проводить регулярные adoption checkpoints;
- видеть, где команда застревает;
- выносить блокеры в EM sync / AI Enablement Team;
- различать технические проблемы, сопротивление и организационную фрикцию;
- удерживать поведенческие ожидания новой модели.

## Системный инсайт

EM становится не владельцем технической реализации AI, а владельцем управленческих условий, при которых AI-native поведение становится нормой.

Ключевой вопрос EM:

не "используют ли люди AI",
а "что в системе мешает команде перейти к agentic delivery".

---

# 3. Инженер становится владельцем результата и контекста

## Наблюдение

В AI-native модели инженер больше не является только исполнителем кода.

Он отвечает за полный цикл:

- понять требование;
- декомпозировать задачу;
- сформулировать agent-consumable context;
- оркестрировать агента;
- проверить код, тесты и edge cases;
- довести изменение до production;
- улучшить `AGENTS.md`, skills и документацию после повторяющихся agent failures.

## Системный инсайт

Ценность инженера смещается:

- от объема написанного кода;
- к качеству решений;
- к способности определить, что значит "correct";
- к способности улучшать knowledge layer, на котором работают агенты.

AI не снижает требования к инженеру.  
AI убирает возможность оставаться в узкой исполнительской роли.

---

# 4. Tech Lead перестает быть default gate

## Наблюдение

AI-native модель конфликтует со старой привычкой делать Tech Lead обязательной точкой проверки.

Если каждый значимый шаг требует внешнего подтверждения, agentic delivery теряет скорость и ownership.

## Новая роль

Tech Lead:

- удерживает архитектурную целостность;
- решает конфликты между ownership-зонами;
- подключается к high-risk изменениям;
- не ревьюит все подряд;
- помогает EM видеть технический контекст без втягивания в детали.

## Системный инсайт

Tech Lead в AI-native организации — не замена ответственности инженера.

Он нужен там, где агентская автономность и локальное ownership могут создать системный конфликт.

---

# 5. Tech PM становится input layer для agentic pipeline

## Наблюдение

Требования становятся первичным входом для agentic delivery.

Tech PM отвечает за то, чтобы Jira-ticket был пригоден для людей и агентов:

- structured user stories;
- numbered acceptance criteria;
- explicit scope boundaries;
- domain context links;
- domain glossary;
- resolved ambiguities before sprint start;
- testable definition of done.

## Системный инсайт

Качество требований напрямую ограничивает потолок AI leverage.

Если требование не machine-readable, downstream-слой компенсирует это встречами, Slack-уточнениями, ручной интерпретацией и rework.

Tech PM больше не просто "пишет задачи".  
Он владеет качеством входного слоя для agentic pipeline.

---

# 6. QE переходит от manual testing к quality system ownership

## Наблюдение

AI-трансформация AgVend требует shift-left testing.

Старый паттерн:

- разработчик пишет код;
- двигает задачу в `ready for testing`;
- QA проверяет;
- ответственность за качество фактически уходит из engineering ownership.

Новый паттерн:

- developer пишет и проверяет тесты вместе с кодом;
- agent-generated tests committed and passing;
- QE задает test strategy и coverage standards;
- QE валидирует качество AI-generated test suites;
- QE владеет pipeline health, flaky tests, coverage reporting и quality gates.

## Системный инсайт

QE перестает быть сервисной функцией проверки.

QE становится владельцем quality system, которая делает agentic delivery безопасной.

---

# 7. Machine-readable knowledge layer становится активом организации

## Наблюдение

План AgVend описывает full ownership loop:

- Tech PM структурирует требования и доменный контекст в Jira;
- Developer переводит требования в specs, `AGENTS.md` и техническую документацию;
- QE фиксирует test strategies и coverage standards в Test Management System;
- агенты используют накопленный контекст для следующего цикла.

## Системный инсайт

Организационное знание должно накапливаться в системе, а не в головах людей.

Документация меняет функцию:

- не архив;
- не onboarding-приложение;
- не формальность;
- а operational substrate для AI-native delivery.

Каждый sprint должен улучшать не только продукт, но и machine-readable контекст, который делает следующий sprint быстрее и надежнее.

---

# 8. AI Enablement Team становится governance-контуром

## Наблюдение

AI Enablement Team в AgVend — это standing function под лидерством CTO.

Она владеет:

- AI tooling decisions;
- workflow design;
- engineering standards для agentic development;
- `AGENTS.md` requirements;
- skill library conventions;
- prompt patterns;
- validation criteria;
- shared knowledge infrastructure;
- agent failure analysis;
- adoption architecture;
- security, risk and governance.

## Системный инсайт

AI adoption нельзя оставлять на уровне локальных инициатив команд.

Без governance организация получает:

- фрагментацию инструментов;
- несовместимые workflows;
- разные quality bars;
- локальные решения повторяющихся agent failures;
- отсутствие единого стандарта безопасности и аудита.

AI Enablement Team превращает AI adoption в управляемый organizational standard: решение, владелец, target team, deadline, EM accountable for delivery.

---

# 9. Definition of Done расширяется до AI-native delivery contract

## Наблюдение

В AI-native модели ticket done не тогда, когда код написан.

Новая рамка DoD включает:

- code merged;
- tests committed and passing;
- coverage threshold met;
- feature deployed to staging;
- acceptance criteria validated against Tech PM requirements;
- ADR или usage guide обновлены при необходимости.

## Системный инсайт

Definition of Done становится контрактом между ролями.

Он фиксирует:

- что инженер не перекладывает качество на QE;
- что требования проверяются против customer intent;
- что test coverage является частью delivery;
- что knowledge layer поддерживается в актуальном состоянии;
- что agentic output проходит human judgment.

---

# 10. CI/CD становится условием AI-native скорости

## Наблюдение

AgVend связывает AI-native delivery с инфраструктурными изменениями:

- feature flags;
- ephemeral preview environments;
- diff-aware test execution;
- automated rollback;
- self-healing pipeline;
- daily deployments для main monolith;
- Platform Reliability ownership of deployment health.

## Системный инсайт

Нельзя требовать частых релизов и agentic execution, если pipeline не поддерживает безопасное движение.

CI/CD становится частью AI operating model:

- агенты ускоряют создание изменений;
- pipeline должен ускорять проверку;
- rollback снижает цену ошибки;
- self-healing CI уменьшает ручную нагрузку;
- человек остается decision gate, а не first responder на каждый сбой.

---

# 11. SRE / Production QA смещается к AI-augmented reliability governance

## Наблюдение

SRE / Production QA отделяется от QA-трансформации.

Роль эволюционирует от incident execution и bug triage к reliability lifecycle ownership:

- detection;
- acknowledgement;
- coordination;
- resolution;
- post-mortem;
- follow-up;
- runbook catalog;
- alert quality;
- reliability metrics;
- AI-assisted triage;
- self-healing pipelines.

## Системный инсайт

Reliability становится отдельным AI-augmented governance-контуром.

SRE не просто чинит production.  
SRE создает структурированные данные, runbooks и post-mortems, на которых затем могут работать AI-инструменты для triage, correlation и remediation.

---

# 12. AI-Assisted Design Engineer становится владельцем design system

## Наблюдение

HTML/CSS специалисты переопределяются как AI-Assisted Design Engineers.

Их новая зона:

- agentic frontend generation at scale;
- design system;
- component library;
- accessibility standards;
- AI-assisted accessibility testing.

## Системный инсайт

Execution-роли не исчезают автоматически. Они должны быть перепроектированы вокруг системного leverage.

Frontend expertise становится ценным не как ручное производство экранов, а как способность управлять design system и quality bar, который агенты воспроизводят массово.

---

# 13. Критерии пригодности людей меняются из-за AI-native модели

## Наблюдение

AI-native модель меняет критерии оценки инженеров и quality-ролей.

На первый план выходят:

- самостоятельность;
- end-to-end ownership;
- способность декомпозировать задачи;
- способность формулировать контекст для агента;
- способность проверять AI-generated output;
- готовность улучшать documentation / `AGENTS.md` / skills;
- способность работать без постоянного QA или Tech Lead gate.

## Системный инсайт

Часть людей, которые были приемлемы в старой модели, могут не подойти для AI-native организации.

Это должно решаться не через субъективное раздражение, а через критерии:

- какое AI-native поведение ожидается;
- какие факты подтверждают соответствие;
- какой срок наблюдения;
- какое решение принимается при отсутствии прогресса.

---

# 14. Метрики становятся системой управления AI-переходом

## Наблюдение

Встречи и план AgVend выделяют набор метрик:

- AI Phase Level per engineer;
- Test Coverage по surface;
- Product Value Points;
- Ticket Reopen Rate;
- Deployment Frequency;
- Release Defect Rate;
- PR Lead Time;
- production incidents;
- MTTR;
- доля задач с AI-участием;
- качество прохождения задач через новый QA/QE-процесс.

## Системный инсайт

Метрики нужны не после стабилизации.  
Они нужны во время перехода, чтобы видеть adoption, качество и системные ограничения.

Ограничение: метрика AI-использования не должна становиться персональной целью разработчика. Иначе команда начнет оптимизироваться под показатель, а не под результат.

Правильная рамка: метрики показывают качество трансформационной системы и удобство созданных инструментов.

---

# Общая карта изменений ролей

| Роль | Старая логика | AI-native логика |
|---|---|---|
| CTO / AI Enablement | Реакция на локальные AI-инициативы | AI standards, toolchain, workflows, governance, adoption architecture |
| EM | Контроль delivery и людей | Adoption conditions, blockers, поведенческие ожидания, управленческий ритм AI-перехода |
| Tech Lead | Default technical gate | Architectural integrity, high-risk decisions, conflicts between ownership zones |
| Developer | Пишет код и передает на тестирование | Orchestrates agents, owns outcome, tests, context and production result |
| QE / QA | Проверяет после разработки | Quality system, coverage strategy, TMS, pipeline health, AI-generated tests validation |
| SRE / Production QA | Реакция на production bugs | Reliability lifecycle, runbooks, structured incident data, AI-assisted triage |
| Tech PM | Backlog items для людей | Machine-readable requirements as input layer for agentic pipeline |
| AI-Assisted Design Engineer | Ручная верстка | Design system, component library, accessibility standards for agentic UI generation |

---

# Главные риски

- AI adoption остается локальным productivity practice, а не operating model.
- Роли формально переименованы, но старые гейты и handoffs сохраняются.
- EM управляет активностью, а не условиями adoption.
- Developer использует агента, но не владеет результатом и контекстом.
- Tech Lead снова становится обязательным review bottleneck.
- QE остается ручным сервисом проверки.
- Tech PM пишет человеческие требования, но не machine-readable input.
- `AGENTS.md`, skills и документация не обновляются после agent failures.
- AI tooling фрагментируется по командам без governance.
- CI/CD не успевает за скоростью agentic execution.
- Метрики AI-использования превращаются в персональную отчетность.

---

# Практические выводы

1. AI-native transformation должна проектироваться как operating model, а не tooling rollout.
2. Каждая роль должна иметь явные AI-native behaviors.
3. Machine-readable контекст должен быть частью delivery.
4. QE и CI/CD — критические элементы AI safety, а не вспомогательные функции.
5. AI Enablement Team нужен как governance-контур.
6. EM отвечает за adoption conditions, не за техническую реализацию за команду.
7. Developer owns output даже тогда, когда code/tests generated by agents.
8. Tech PM quality становится потолком agentic leverage.
9. Метрики должны измерять зрелость системы, а не стимулировать имитацию AI adoption.

---

# Возможная рамка для дальнейшей работы

Для AgVend полезно отдельно собрать:

- AI-native behaviors по каждой роли;
- machine-readable artifacts по каждой роли;
- старые гейты, которые мешают agentic delivery;
- новые quality gates;
- adoption metrics;
- ownership loop: Tech PM → Developer → QE → CI/CD → SRE;
- governance decisions для AI Enablement Team.

Это может стать базой для отдельного framework note про [[AI-native organization]] и [[architecture of manageability]].
