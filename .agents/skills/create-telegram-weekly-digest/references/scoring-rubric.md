# Scoring Rubric

Оценивать только после нормализации сообщений.

## Dimensions

- `strategic_relevance`: связь с AI transformation, operating model, CTO/CEO agenda.
- `novelty`: новый сигнал, а не повтор уже известной новости.
- `management_implication`: есть вывод для управления системой, ownership, decision-making, quality или risk.
- `evidence_quality`: есть конкретика, пример, данные, первоисточник или наблюдаемый паттерн.
- `content_potential`: можно развить в LinkedIn post, framework, advisory memo или клиентский вопрос.

## Scale

- 1: шум.
- 2: слабый сигнал, можно пропустить.
- 3: потенциально полезно, но нужен контекст.
- 4: сильный сигнал для digest.
- 5: стратегически важный сигнал, заслуживает отдельной заметки или поста.

## Include

Включать в digest сообщения, где:
- `management_implication >= 4`; или
- `strategic_relevance + content_potential >= 8`; или
- сообщение указывает на повторяющийся паттерн недели.

## Exclude

Исключать даже при высоких views:
- рекламные интеграции;
- вакансии;
- списки инструментов без управленческого смысла;
- generic AI optimism / fear;
- пересказы новостей без нового вывода.
