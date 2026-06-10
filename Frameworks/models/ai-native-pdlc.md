---
type: framework-note
topic:
  - AI transformation
  - engineering management
  - software delivery
status: draft
source:
  - "[[Frameworks/sources/ai-pdlc/ai-disrupt-pdlc-v3-7-2026.docx|AI_DISRUPT_PDLC_v3_7]]"
  - "[[Frameworks/source-notes/ai-disrupt-pdlc-whitepaper-2026|AI-Disrupt PDLC Whitepaper 2026]]"
---

# AI-native PDLC

AI-native PDLC - операционная модель разработки, в которой человек отвечает за намерение, спецификацию, архитектурные решения и проверку результата, а агентная среда отвечает за ускоренное исполнение в заданных границах.

## Коротко

Сдвиг не в том, что код пишется быстрее. Сдвиг в том, что жизненный цикл разработки разделяется на два разных ритма:

- **Intent Loop**: формулирование возможности, Discovery, гипотеза результата, спецификация, карта участия человека.
- **Implementation Loop**: агентное исполнение, тесты, исправления, проверки, пакет доказательств, передача сессии.

Между ними нужен [[Frameworks/models/internal-developer-platform|Internal Developer Platform]], иначе две петли работают параллельно, но не становятся единой управляемой системой.

## Модель

```mermaid
flowchart LR
    A["Сигнал: клиент, метрика, инцидент, регулятор, backlog"] --> B["Discovery"]
    B --> C["Outcome Hypothesis"]
    C --> D["SDD"]
    D --> E["Agent Runtime / IDP"]
    E --> F["Implementation Loop"]
    F --> G["Evidence Bundle"]
    G --> H["Outcome Check"]
    H --> B

    I["Governance Mesh"] -.-> B
    I -.-> D
    I -.-> E
    I -.-> F
    I -.-> G
```

## Ключевые принципы

- Среда работы агента (Harness) важнее модели: модель можно заменить, а [[Frameworks/models/agent-runtime|Agent Runtime]] накапливает организационный контекст, проверки и аудит.
- Discovery важнее prompt: плохое намерение нельзя компенсировать длинной инструкцией агенту.
- Validation важнее скорости поставки: ускорение реализации без ускорения проверки создает новое узкое место.
- Управление в процессе важнее проверок постфактум: [[Frameworks/models/governance-mesh|Governance Mesh]] должен быть встроен в спецификацию, runtime и аудит.

## Отличие от классического PDLC

| Элемент | Классический PDLC | AI-native PDLC |
| --- | --- | --- |
| Первичный артефакт | задача / код | намерение, SDD, eval plan, Evidence Bundle |
| Главный исполнитель | человек | человек + агентная среда |
| Ограничение скорости | человеческое исполнение | качество намерения, контекста и валидации |
| Контроль качества | ревью и тесты на поздних стадиях | evals, policy hooks, review agents и telemetry внутри процесса |
| Управление риском | stage gates | adaptive controls в runtime |

## Операционный минимум

Минимальный стартовый набор:

- Discovery-ритуалы: PR/FAQ, Outcome Hypothesis, решение "адаптация или перепроектирование".
- [[Frameworks/models/specification-driven-development|SDD]] как контракт изменения.
- Review-agent в теневом режиме.
- Базовый [[Frameworks/models/evidence-bundle|Evidence Bundle]].
- Метрики: lead time, change failure rate, Outcome Validation Rate, Reallocation Rate.

## Advisory use

Эта заметка полезна как рамка диагностики: клиент не "внедряет AI в разработку", пока у него нет изменения PDLC. До этого он внедряет инструменты индивидуальной продуктивности.

Вопрос для executive-дискуссии:

> Что в вашей инженерной организации изменилось в контуре намерения, проверки результата и управления риском, кроме появления AI-инструментов у разработчиков?

## Связанные заметки

- [[Frameworks/models/specification-driven-development|Specification-Driven Development]]
- [[Frameworks/models/evidence-bundle|Evidence Bundle]]
- [[Frameworks/models/governance-mesh|Governance Mesh]]
- [[Frameworks/models/agent-runtime|Agent Runtime]]
- [[Frameworks/models/ai-native-engineering-metrics|AI-native engineering metrics]]
- [[Frameworks/models/architecture-of-manageability|architecture of manageability]]
