#!/bin/bash
# Публикует папку site/ в репозиторий semenyuk.pro (GitHub Pages).
# Источник правды — KnowledgeOS. Репозиторий semenyuk.pro только для публикации.
# Пуш без --force: если в semenyuk.pro есть правки, которых нет в KnowledgeOS
# (например, сделанные прямо на GitHub), скрипт остановится и ничего не перезапишет.
# Перед запуском закоммитьте изменения в KnowledgeOS.
set -e
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
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
