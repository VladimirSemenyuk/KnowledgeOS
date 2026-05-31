---
type: framework-note
topic:
  - AI transformation
  - engineering management
  - metrics
status: draft
source:
  - "[[Frameworks/sources/ai-pdlc/ai-disrupt-pdlc-v3-7-2026.docx|AI_DISRUPT_PDLC_v3_7]]"
---

# AI-native engineering metrics

AI-native engineering metrics - система метрик, которая измеряет не только скорость генерации кода, но и результат, качество, автономию, валидацию, стоимость и управляемость агентной разработки.

## Коротко

Главный риск AI в engineering - принять рост output за рост ценности. Поэтому метрики должны связывать:

- скорость;
- стабильность;
- качество;
- подтвержденный outcome;
- стоимость токенов;
- зрелость автономии;
- покрытие платформенными политиками.

## Базовые категории

| Категория | Что измеряет | Примеры метрик |
| --- | --- | --- |
| Velocity | скорость доставки | Lead Time, Spec-to-Deploy, Discovery Cycle Time |
| Quality | стабильность и надежность | Change Failure Rate, Agent-introduced Regression Rate |
| Efficiency | использование ресурсов | Token Cost per Feature, Reallocation Rate, CTOR |
| Business Impact | влияние на бизнес | Outcome Validation Rate, ARR contribution |
| Autonomy | зрелость агентного исполнения | Median Task Horizon, Self-Recovery Rate |
| Outcome Effectiveness | связь результата и затрат | Cost-to-Outcome Ratio, Outcome Yield |

## Метрики Discovery

- Workflow Redesign Rate: доля задач, где процесс был перепроектирован, а не просто автоматизирован.
- Discovery Cycle Time: время от идеи до утвержденного SDD.
- Outcome Hypothesis Coverage: доля SDD с измеримой гипотезой результата.
- Agentic Fit Classification: доля задач, классифицированных до реализации.
- Human-in-the-loop Coverage Score: доля SDD с картой участия человека.

## Метрики реализации и валидации

| Метрика | Что показывает |
| --- | --- |
| Median Task Horizon | насколько длинные автономные сессии выдерживает система |
| Task Completion @ Horizon | доля задач, завершенных при заданном горизонте автономии |
| Self-Recovery Rate | способность сессий восстанавливаться без человека |
| Multi-Agent Adoption % | доля задач в режиме orchestrator-workers |
| Output Volume Lift | рост количества артефактов относительно baseline |
| Implementation/Validation Tempo Ratio | не отстает ли валидация от реализации |
| Evidence Bundle Completion Rate | полнота доказательств завершения |
| Hallucination Rate @ Horizon | деградация качества при росте длительности сессии |

## Метрики управления

Governance Effectiveness Metrics отвечают не на вопрос "правильно ли сделано", а на вопрос "правильно ли был устроен процесс".

| Метрика | Сигнал |
| --- | --- |
| Code compliance rate | соответствие внутренним и внешним нормам |
| Human override rate | доля AI-output, исправленного или отклоненного человеком |
| Runtime control activation rate | работают ли adaptive controls |
| Autoremediation success rate | способность системы исправлять низко- и среднерисковые проблемы |
| Platform coverage of AI tools and agents | доля AI-инструментов под едиными политиками |
| Policy Conflict Rate | частота конфликтов между базовыми и доменными политиками |

## Парные метрики

Отдельные метрики легко вводят в заблуждение. В концепции полезнее смотреть пары:

| Пара | Зачем нужна |
| --- | --- |
| Lead Time x Output Volume | скорость не должна достигаться уменьшением объема работ |
| Change Failure Rate x Agent-introduced Regression Rate | AI не должен покупать скорость ценой регрессий |
| Outcome Validation Rate x Change Failure Rate | бизнес-результат должен смотреться вместе со стабильностью |
| Spec Reuse Rate x Token Cost per Feature | переиспользование должно снижать стоимость |
| Median Task Horizon x Self-Recovery Rate | длинные сессии должны быть надежными |
| Reallocation Rate x Output Volume Lift | сэкономленное время должно превращаться в ценную работу |

## Лестница зрелости

| Уровень | Доля задач с AI | Медианный task horizon |
| --- | ---: | --- |
| L1 | <10% | до 5 минут |
| L2 | 10-30% | до 15 минут |
| L3 | 30-60% | до 1 часа |
| L4 | 60-80% | до 4 часов / до рабочего дня в зрелом режиме |
| L5+ | >80% | 4+ часа с автономным восстановлением |

## Advisory use

Для executive-оценки важно не начинать с "сколько разработчиков используют AI". Это метрика adoption, а не трансформации.

Лучший первый набор:

- baseline DORA;
- Outcome Hypothesis Coverage;
- Implementation/Validation Tempo Ratio;
- Evidence Bundle Completion Rate;
- Agent-introduced Regression Rate;
- Reallocation Rate;
- Platform coverage of AI tools and agents.

## Связанные заметки

- [[Frameworks/models/ai-native-pdlc|AI-native PDLC]]
- [[Frameworks/models/evidence-bundle|Evidence Bundle]]
- [[Frameworks/models/governance-mesh|Governance Mesh]]
- [[Frameworks/source-notes/dora-roi-of-ai-assisted-software-development-2026|DORA ROI of AI-assisted Software Development 2026]]
- [[Frameworks/models/quality-and-risks|quality and risks]]
