#!/bin/bash
# Публикует папку site/ в репозиторий semenyuk.pro (GitHub Pages).
# Источник правды — KnowledgeOS. Репозиторий semenyuk.pro только для публикации:
# правки, сделанные прямо на GitHub, будут перезаписаны.
# Перед запуском закоммитьте изменения в KnowledgeOS.
set -e
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
git remote get-url site >/dev/null 2>&1 || git remote add site git@github.com:VladimirSemenyuk/semenyuk.pro.git
SHA=$(git subtree split --prefix Personal/marketing/website/site HEAD)
git push --force site "$SHA:refs/heads/main"
echo "Готово: https://semenyuk.pro (обновится через 1–2 минуты)"
