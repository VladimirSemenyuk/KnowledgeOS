#!/usr/bin/env node
/* Сборка страниц результатов теста и картинок-превью.

   Запуск из папки website/:
       node tools/tests-build.mjs paei            # страницы и картинки
       node tools/tests-build.mjs paei --no-img   # только страницы

   Ничего не считает и не рисует сама: профили берёт у site/tests/assets/scoring.js,
   тексты — у profile.js, превью рисует profile.js (drawOg) в Chrome без окна —
   тот же код, что считает результат и рисует сторис на сайте. Пишет:
       site/tests/<id>/r/<имя>/index.html — страница результата (noindex, своё превью);
       site/tests/<id>/r/<имя>/og.jpg     — превью 1200×630;
       site/tests/<id>/og.jpg             — превью страницы теста.
   Старые папки профилей, которые стали недостижимы, удаляются. В конце проставляет версии
   скриптов и стилей во всех страницах сайта (stamp-assets.mjs). */
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";
import { stampSite } from "./stamp-assets.mjs";

const require = createRequire(import.meta.url);
const HERE = path.dirname(fileURLToPath(import.meta.url));
const SITE = path.join(HERE, "..", "site");
const ASSETS = path.join(SITE, "tests", "assets");
const S = require(path.join(ASSETS, "scoring.js"));
const P = require(path.join(ASSETS, "profile.js"));
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const FONTS = '<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600&display=swap" rel="stylesheet">';

const e = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#x27;" })[c]);
const up = (depth) => "../".repeat(depth);

/* ---------- общие куски страниц: голова, счётчик Метрики, подвал. depth — глубина от site/ ---------- */
const METRIKA = `<!-- Яндекс.Метрика: счётчик 114369053. Цели тестов: test_start, test_finish, test_tg_send, test_share, test_story, test_copy. -->
<script>
(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js?id=114369053","ym");
ym(114369053,"init",{ssr:true,webvisor:true,clickmap:true,accurateTrackBounce:true,trackLinks:true});
document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a[data-goal]");if(a)ym(114369053,"reachGoal",a.dataset.goal,{place:a.dataset.place});});
</script>`;
const NOSCRIPT = '<noscript><div><img src="https://mc.yandex.ru/watch/114369053" style="position:absolute;left:-9999px" alt=""></div></noscript>';

function head(depth) {
  const u = up(depth);
  return `<link rel="icon" href="${u}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="${u}assets/icons/favicon-32.png">
<link rel="apple-touch-icon" href="${u}assets/icons/apple-touch-icon.png">
<link rel="manifest" href="${u}site.webmanifest">
<meta name="theme-color" content="#F3F4F1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
${FONTS}
<link rel="stylesheet" href="${u}tests/assets/tests.css">
${METRIKA}`;
}

function footer(depth, place) {
  const u = up(depth);
  return `<footer class="site-foot">
  <div class="wrap site-foot__in">
    <ul class="site-foot__links">
      <li><a class="link" href="${u}">Главная</a></li>
      <li><a class="link" href="${u}tests/">Тесты</a></li>
      <li><a class="link" data-goal="tg_write" data-place="${place}-footer" href="https://t.me/vladimirsemenyuk">Telegram</a></li>
      <li><a class="link" data-goal="email_write" data-place="${place}-footer" href="mailto:vladimir@semenyuk.pro">vladimir@semenyuk.pro</a></li>
    </ul>
    <p>©&nbsp;2026 Владимир Семенюк</p>
  </div>
</footer>`;
}

/* ---------- страница результата ---------- */
function resultPage(T, c, slug) {
  const url = `${T.url}r/${slug}/`;
  const name = T.names[c];
  const desc = P.describe(T, c);
  return `<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${e(`Профиль ${c} · ${T.title}`)} · Владимир Семенюк</title>
<meta name="description" content="${e(desc)}">
<meta name="robots" content="noindex">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:title" content="${e(P.ogTitle(T, c))}">
<meta property="og:description" content="${e(desc)}">
<meta property="og:image" content="${url}og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="${url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="${url}">
${head(4)}
</head>
<body data-page="result" data-code="${e(c)}" data-root="../../">
${NOSCRIPT}
<header class="nav">
  <div class="wrap nav__in">
    <a class="skip" href="#res">К&nbsp;содержанию</a>
    <a class="who" href="../../../../"><b>Владимир Семенюк</b></a>
    <a class="btn btn--sm" data-goal="tg_write" data-place="result-nav" href="https://t.me/${T.telegram}">Написать<span class="btn-tail">&nbsp;в&nbsp;Telegram</span></a>
  </div>
</header>
<main class="screen">
  <div class="wrap res" id="res">
    <noscript><p>Профиль <b>${e(c)}</b>${name ? e(" — «" + name + "»") : ""}. Результат показывается с&nbsp;включённым JavaScript.</p></noscript>
  </div>
</main>
<div class="toast" id="toast" role="status"></div>
${footer(4, "result")}
<script src="../../data.js"></script>
<script src="../../../assets/scoring.js"></script>
<script src="../../../assets/profile.js"></script>
<script src="../../../assets/crypto.js"></script>
<script src="../../../assets/tests.js"></script>
</body>
</html>
`;
}

/* ---------- превью: одна страница в Chrome рисует все картинки через profile.js и отдаёт их в DOM ---------- */
function renderImages(testId, codes) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "tests-og-"));
  const src = (f) => pathToFileURL(f).href;
  const page = `<!doctype html><html lang="ru"><head><meta charset="utf-8">${FONTS}
<link rel="stylesheet" href="${src(path.join(ASSETS, "tests.css"))}">
<script src="${src(path.join(SITE, "tests", testId, "data.js"))}"></script>
<script src="${src(path.join(ASSETS, "scoring.js"))}"></script>
<script src="${src(path.join(ASSETS, "profile.js"))}"></script>
</head><body><pre id="out"></pre><script>
var P=window.TestProfile,T=window.TEST,codes=${JSON.stringify(codes)},out={};
P.fontsReady().then(function(){
  out[""]=P.drawOg(T).toDataURL("image/jpeg",0.86);
  codes.forEach(function(c){out[c]=P.drawOg(T,c).toDataURL("image/jpeg",0.86)});
  document.getElementById("out").textContent=JSON.stringify(out);
}).catch(function(err){document.getElementById("out").textContent=JSON.stringify({error:String(err)})});
</script></body></html>`;
  const file = path.join(tmp, "og.html");
  fs.writeFileSync(file, page);
  try {
    const dom = execFileSync(CHROME, ["--headless=new", "--allow-file-access-from-files", "--virtual-time-budget=20000", "--dump-dom", src(file)],
      { encoding: "utf8", maxBuffer: 256 * 1024 * 1024, stdio: ["ignore", "pipe", "ignore"] });
    const m = dom.match(/<pre id="out">([\s\S]*?)<\/pre>/);
    const json = m && m[1].replace(/&quot;/g, '"').replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
    if (!json) throw new Error("Chrome не вернул картинки: страница не дорисовала (шрифты не загрузились?)");
    const out = JSON.parse(json);
    if (out.error) throw new Error("profile.js: " + out.error);
    return Object.fromEntries(Object.entries(out).map(([c, url]) => [c, Buffer.from(url.split(",")[1], "base64")]));
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

function main() {
  const args = process.argv.slice(2);
  const testId = args.find((a) => !a.startsWith("--")) || "paei";
  const images = !args.includes("--no-img");
  const base = path.join(SITE, "tests", testId);
  const T = S.parseData(fs.readFileSync(path.join(base, "data.js"), "utf8"));
  const codes = S.reachable(T);
  const slugs = Object.fromEntries(codes.map((c) => [c, S.slugOf(c)]));
  const rdir = path.join(base, "r");
  const keep = new Set(Object.values(slugs));
  if (fs.existsSync(rdir))
    for (const d of fs.readdirSync(rdir))
      if (!keep.has(d) && fs.statSync(path.join(rdir, d)).isDirectory()) fs.rmSync(path.join(rdir, d), { recursive: true });
  const jpg = images ? renderImages(testId, codes) : null;
  for (const c of codes) {
    const d = path.join(rdir, slugs[c]);
    fs.mkdirSync(d, { recursive: true });
    fs.writeFileSync(path.join(d, "index.html"), resultPage(T, c, slugs[c]));
    if (jpg) fs.writeFileSync(path.join(d, "og.jpg"), jpg[c]);
  }
  if (jpg) fs.writeFileSync(path.join(base, "og.jpg"), jpg[""]);
  const { missing } = stampSite();
  if (missing.length) throw new Error("Ссылки на несуществующие файлы: " + missing.join(", "));
  console.log(`Готово: ${codes.length} страниц профилей` + (images ? " и превью" : ""));
}

main();
