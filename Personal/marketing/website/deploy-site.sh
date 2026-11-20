#!/bin/bash
# Публикует папку site/ в репозиторий semenyuk.pro (GitHub Pages).
# Источник правды — KnowledgeOS. Репозиторий semenyuk.pro только для публикации.
# Пуш без --force: если в semenyuk.pro есть правки, которых нет в KnowledgeOS
# (например, сделанные прямо на GitHub), скрипт остановится и ничего не перезапишет.
# Перед запуском закоммитьте изменения в KnowledgeOS.
set -e
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
# Каждая страница сайта должна нести счётчик Яндекс.Метрики (код — в site/README.md, раздел «Аналитика»).
# Служебные файлы подтверждения (yandex_*.html, google*.html) не проверяются.
MISSING=$(find Personal/marketing/website/site -name '*.html' ! -name 'yandex_*.html' ! -name 'google*.html' \
  -exec grep -L 'mc.yandex.ru/metrika/tag.js?id=114369053' {} +)
if [ -n "$MISSING" ]; then
  echo "На этих страницах нет счётчика Метрики. Вставьте код из site/README.md («Аналитика») и закоммитьте:"
  echo "$MISSING"
  exit 1
fi
# Тесты сайта: подсчёт, шифрование ссылок, соответствие собранных страниц профилям.
(cd Personal/marketing/website && node --test 'test/*.test.mjs' >/dev/null 2>&1) || {
  echo "Тесты сайта не прошли. Подробности: cd Personal/marketing/website && node --test 'test/*.test.mjs'"; exit 1; }
# Скрипты и стили подключаются с версией по содержимому (?v=…), иначе браузеры держат старые копии.
node Personal/marketing/website/tools/stamp-assets.mjs --check || exit 1
git remote get-url site >/dev/null 2>&1 || git remote add site git@github.com:VladimirSemenyuk/semenyuk.pro.git
# subtree split пишет прогресс через \r в тот же поток: берём только строку с SHA.
SHA=$(git subtree split --prefix Personal/marketing/website/site HEAD 2>/dev/null | tr '\r' '\n' | grep -oE '^[0-9a-f]{40}$' | tail -1)
[ -n "$SHA" ] || { echo "Не удалось получить коммит папки site/"; exit 1; }
git fetch -q site
if ! git merge-base --is-ancestor site/main "$SHA"; then
  echo "В semenyuk.pro есть коммиты, которых нет в KnowledgeOS. Перенесите их в site/ и закоммитьте, затем запустите снова."
  git log --oneline "$SHA..site/main"
  exit 1
fi
git push site "$SHA:refs/heads/main"
echo "Готово: https://semenyuk.pro (обновится через 1–2 минуты)"
