---
name: import-linkedin-posts
description: Импорт опубликованных LinkedIn-постов из открытой страницы LinkedIn/Analytics в Posts/published, обновление vault без дублей и сбор аналитики только за последний год.
---

# LinkedIn Posts Import

## Purpose

Забрать из открытой страницы LinkedIn:
- опубликованные посты;
- ссылки и activity id;
- аналитику постов за последний год;
- сохранить или обновить заметки в `Posts/published`;
- обновить агрегированную таблицу в `Posts/metrics.md`.

## When To Use

Использовать, когда пользователь просит:
- забрать посты из LinkedIn через браузер;
- импортировать LinkedIn-посты в vault;
- собрать статистику, аналитику, impressions, reactions, comments по LinkedIn-постам;
- обновить `Posts/published` без дублей.

## Required Context

Перед изменениями прочитать:
- `Posts/AGENTS.md`;
- `Posts/Context.md`;
- `Posts/metrics.md`, если файл существует;
- существующие файлы в `Posts/published`.

Соблюдать правила vault:
- русский язык;
- concise executive style;
- не добавлять случайные английские слова в русские заметки;
- сохранять английский только если он был в исходном посте, относится к метрикам, продуктам, компаниям, названиям ролей или точным терминам;
- не создавать новые top-level folders;
- не удалять и не переименовывать существующие папки;
- не создавать дубли постов;
- не перезаписывать вручную доработанные секции без необходимости.

## Analytics Period

По умолчанию собирать аналитику только за последний месяц.

В LinkedIn Analytics использовать:
- `Последние 365 дней`, если это ближайший доступный preset;
- custom range за последний календарный месяц только если пользователь явно просит календарный месяц.

Не использовать годовой диапазон, если пользователь не попросил отдельно.

## Browser Workflow

1. Использовать браузер пользователя, если он уже открыт или пользователь просит "через мой браузер".
2. Открыть страницу LinkedIn Creator Analytics / Top posts:

```text
https://www.linkedin.com/analytics/creator/top-posts/?metricType=IMPRESSIONS&timeRange=past_365_days
```

3. Если LinkedIn не применил query parameters, вручную выбрать:
   - метрика: `Показы` / `Impressions`;
   - период: `Последние 365 дней`.
4. Проверить, что выбран период последнего месяца:
   - обычно `Последние 365 дней`;
   - проверить, что страница действительно обновилась.
5. Прокрутить список до конца, чтобы все посты периода загрузились.
6. Скопировать страницу:
   - сфокусировать страницу;
   - `Cmd+A`;
   - `Cmd+C`;
   - сохранить clipboard во временный файл, например `/private/tmp/linkedin_analytics_page.txt`.
7. Если нужны ссылки/activity id, брать их из DOM, accessibility tree или видимых ссылок вида:
   - `https://www.linkedin.com/feed/update/urn:li:activity:{id}/`

Если LinkedIn просит login, captcha или 2FA, остановиться и попросить пользователя пройти шаг вручную.

## Parsing Rules

Для каждого поста извлечь:
- full post text;
- publish date, если доступна;
- `linkedin_activity_id`;
- `linkedin_url`;
- impressions;
- reactions;
- comments.

Правила очистки:
- удалить сервисные строки LinkedIn: `Показать еще`, `См. аналитику`, `Показы`, reaction labels, navigation labels;
- `Хэштег#tag` нормализовать в `#tag`;
- не импортировать пустые media-only блоки вроде `Альтернативный текст...`, если пользователь явно не просил;
- сохранять смысл и формулировки поста, не переписывать его как новый текст.

Activity id можно использовать для даты публикации, если дата не видна:

```js
new Date(Number(BigInt(activityId) >> 22n))
```

Метрики парсить осторожно:
- `impressions` брать только из числа перед `Показы` / `Impressions`;
- `comments` брать из числа перед `комментар` / `comments`;
- `reactions` брать из отдельной числовой строки перед comments или impressions;
- не путать impressions с reactions.

## Deduplication

Перед созданием файла проверить `Posts/published` по:
1. `linkedin_activity_id`;
2. `linkedin_url`;
3. нормализованному тексту поста;
4. близкому title + publish date.

Если пост уже есть:
- обновить `linkedin_url`, `linkedin_activity_id` и `## Analytics`;
- сохранить существующие editorial sections, если они были доработаны вручную;
- не создавать новый файл.

Если поста нет:
- создать новый kebab-case файл в `Posts/published`;
- filename строить из даты и короткого slug по hook, например:
  `2026-05-14-ai-native-organization.md`.

## Note Format

Использовать Markdown с frontmatter:

```markdown
---
title: "Короткий title"
status: published
publish_date: YYYY-MM-DD
source: linkedin
linkedin_url: "https://www.linkedin.com/feed/update/urn:li:activity:..."
linkedin_activity_id: "..."
---

# Короткий title

## Post

Текст поста.

## Analytics

- Период: последние 365 дней
- Дата сбора: YYYY-MM-DD
- Показы: 0
- Реакции: 0
- Комментарии: 0
- Источник: LinkedIn Creator Analytics
```

Если точная дата неизвестна, использовать дату из activity id и сообщить об этом в финальном ответе.

## Metrics File

Обновить `Posts/metrics.md`:
- добавить или заменить блок `## Imported Monthly Post Analytics`;
- указать capture date и source;
- таблицу отсортировать по impressions descending;
- включить wikilink на note, дату, impressions, reactions, comments, url.

Не удалять другие секции `Posts/metrics.md`.

## Verification

Перед финальным ответом проверить:
- количество импортированных и обновленных постов;
- отсутствие дублей по `linkedin_activity_id`;
- что новые файлы лежат только в `Posts/published`;
- что `Posts/metrics.md` обновлен;
- что нет явных сервисных артефактов LinkedIn в текстах постов.

В финальном ответе кратко указать:
- сколько постов создано;
- сколько обновлено;
- сколько пропущено как дубли или пустые блоки;
- период аналитики;
- путь к обновленному metrics-файлу.
