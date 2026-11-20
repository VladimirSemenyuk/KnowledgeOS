#!/usr/bin/env node
/* Версии в адресах скриптов и стилей сайта: src="../assets/tests.js?v=3f9a1c2e".
   Версия — начало хеша содержимого файла: поменялся файл — поменялся адрес, и браузер
   не возьмёт старую копию из кеша. Не поменялся — адрес тот же, кеш работает.

   Запуск из папки website/:
       node tools/stamp-assets.mjs           # проставить версии во всех страницах site/
       node tools/stamp-assets.mjs --check   # только проверить; есть устаревшие — код выхода 1

   Проставляется для локальных .js и .css в атрибутах src и href. Внешние адреса не трогаются.
   Сборка тестов (tests-build.mjs) вызывает stampSite сама, deploy-site.sh запускает --check. */
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const SITE = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "site");
const REF = /\b(src|href)="((?!https?:|\/\/|data:|mailto:)[^"?#]+\.(?:js|css))(?:\?v=[0-9a-f]*)?"/g;

function htmlFiles(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) htmlFiles(p, out);
    else if (e.name.endsWith(".html")) out.push(p);
  }
  return out;
}

export function stampSite({ check = false, root = SITE } = {}) {
  const hashes = new Map();
  const version = (file) => {
    if (!hashes.has(file)) hashes.set(file, crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex").slice(0, 8));
    return hashes.get(file);
  };
  const changed = [], missing = [];
  for (const page of htmlFiles(root)) {
    const src = fs.readFileSync(page, "utf8");
    const out = src.replace(REF, (all, attr, ref) => {
      const file = ref.startsWith("/") ? path.join(SITE, ref) : path.resolve(path.dirname(page), ref);
      if (!fs.existsSync(file)) { missing.push(`${path.relative(SITE, page)}: ${ref}`); return all; }
      return `${attr}="${ref}?v=${version(file)}"`;
    });
    if (out !== src) {
      changed.push(path.relative(SITE, page));
      if (!check) fs.writeFileSync(page, out);
    }
  }
  return { changed, missing };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const check = process.argv.includes("--check");
  const { changed, missing } = stampSite({ check });
  if (missing.length) console.log("Ссылки на несуществующие файлы:\n  " + missing.join("\n  "));
  if (check) {
    if (changed.length) {
      console.log(`Версии файлов устарели на ${changed.length} страницах, например: ${changed.slice(0, 3).join(", ")}.\n` +
        "Запустите из папки website/: node tools/stamp-assets.mjs — и закоммитьте.");
      process.exit(1);
    }
    if (missing.length) process.exit(1);
    console.log("Версии файлов актуальны");
  } else {
    console.log(changed.length ? `Версии обновлены на ${changed.length} страницах` : "Версии уже актуальны");
    if (missing.length) process.exit(1);
  }
}
