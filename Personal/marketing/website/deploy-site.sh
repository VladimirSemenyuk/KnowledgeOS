#!/bin/bash
# Публикует папку site/ в репозиторий semenyuk.pro (GitHub Pages).
# Перед запуском закоммитьте изменения в KnowledgeOS.
set -e
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
git remote get-url site >/dev/null 2>&1 || git remote add site git@github.com:VladimirSemenyuk/semenyuk.pro.git
git subtree push --prefix Personal/marketing/website/site site main
echo "Готово: https://semenyuk.pro (обновится через 1–2 минуты)"
