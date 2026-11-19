#!/usr/bin/env python3
"""Сборка страниц результатов теста и картинок-превью.

Запуск из папки website/:
    python3 tools/tests-build.py paei            # страницы и картинки
    python3 tools/tests-build.py paei --no-img   # только страницы

Читает site/tests/<id>/data.js (JSON после «window.TEST=»), перебирает все достижимые профили
при текущих порогах и пишет:
    site/tests/<id>/r/<код>/index.html — страница результата (noindex, своё превью);
    site/tests/<id>/r/<код>/og.jpg     — превью 1200×630;
    site/tests/<id>/og.jpg             — превью страницы теста.
Старые папки профилей, которые стали недостижимы, удаляются.
"""
import html
import itertools
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(__file__))
import tests_common as common  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "site")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
RING = "M30 12C70 3 150 2 184 14c18 7 16 28-4 38-38 15-122 14-160 3C2 49 2 31 18 21c22-13 76-17 112-13"


def load(test_id):
    src = open(os.path.join(SITE, "tests", test_id, "data.js"), encoding="utf-8").read()
    return json.loads(src.split("\nwindow.TEST=", 1)[1].rstrip().rstrip(";"))


def reachable(T):
    """Все профили, которые дают реальные раскладки ответов: главный выбор — 2 балла, второй — 1."""
    n = len(T["questions"])

    def comps(total, k):
        if k == 1:
            yield (total,)
            return
        for i in range(total + 1):
            for r in comps(total - i, k - 1):
                yield (i,) + r

    C = list(comps(n, 4))
    codes = set()
    for m in C:
        for s in C:
            if all(m[i] + s[i] <= n for i in range(4)):
                sc = [2 * m[i] + s[i] for i in range(4)]
                codes.add(code_of(T, sc))
    return sorted(codes)


def code_of(T, s):
    L = T["letters"]
    return "".join(L[i] if v >= T["hi"] else (L[i].lower() if v >= T["lo"] else "-") for i, v in enumerate(s))


def slug_of(c):
    return "".join("0" if ch == "-" else (ch.lower() * 2 if ch.isupper() else ch) for ch in c)


def lead_names(T, c):
    return [T["roles"][ch]["n"] for ch in c if ch != "-" and ch.isupper()]


def describe(T, c):
    name = T["names"].get(c)
    lead = ", ".join(lead_names(T, c))
    first = f"По Адизесу — «{name}». Ведущие роли: {lead}." if name else (f"Ведущие роли: {lead}." if lead else "Явной ведущей роли нет: все четыре роли рабочие.")
    return first + " Пройдите тест: 20 рабочих ситуаций руководителя, 5 минут."


def result_page(T, c):
    e = html.escape
    slug = slug_of(c)
    url = f"{T['url']}r/{slug}/"
    title = f"Профиль {c} · {T['title']}"
    name = T["names"].get(c)
    og_title = f"Профиль склонностей {c}" + (f" — «{name}»" if name else "")
    page = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · Владимир Семенюк</title>
<meta name="description" content="{e(describe(T, c))}">
<meta name="robots" content="noindex">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:title" content="{e(og_title)}">
<meta property="og:description" content="{e(describe(T, c))}">
<meta property="og:image" content="{url}og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}">
@@COMMON_HEAD@@
</head>
<body data-page="result" data-code="{e(c)}" data-root="../../">
@@METRIKA_NOSCRIPT@@
<header class="nav">
  <div class="wrap nav__in">
    <a class="skip" href="#res">К&nbsp;содержанию</a>
    <a class="who" href="../../../../"><b>Владимир Семенюк</b></a>
    <a class="btn btn--sm" data-goal="tg_write" data-place="result-nav" href="https://t.me/{T['telegram']}">Написать<span class="btn-tail">&nbsp;в&nbsp;Telegram</span></a>
  </div>
</header>
<main class="screen">
  <div class="wrap res" id="res">
    <noscript><p>Профиль <b>{e(c)}</b>{e(' — «' + name + '»') if name else ''}. Результат показывается с&nbsp;включённым JavaScript.</p></noscript>
  </div>
</main>
<div class="toast" id="toast" role="status"></div>
@@FOOTER@@
<script src="../../data.js"></script>
<script src="../../../assets/tests.js"></script>
</body>
</html>
"""
    return common.fill(page, 4, "result")


OG_CSS = """*{box-sizing:border-box}html,body{margin:0}
body{width:1200px;height:630px;background:#F3F4F1;color:#16181A;font-family:Onest,system-ui,sans-serif;-webkit-font-smoothing:antialiased;
display:flex;flex-direction:column;justify-content:space-between;padding:64px 72px 56px}
.top{display:flex;justify-content:space-between;align-items:baseline;border-top:3px solid #16181A;padding-top:18px;font-size:22px}
.lab{font-weight:600;letter-spacing:.08em;text-transform:uppercase}.mut{color:#5E6469}
.code{position:relative;display:inline-flex;gap:6px;font-size:200px;line-height:.9;font-weight:600;letter-spacing:-.03em;padding:0 30px;margin-left:-30px}
.code .lo{color:#3A3E42;font-weight:500}.code .no{color:#BFC4C6;font-weight:500}
.code svg{position:absolute;left:-5%;top:-18%;width:110%;height:136%;overflow:visible}
.code path{fill:none;stroke:#D2302C;stroke-width:6;stroke-linecap:round;vector-effect:non-scaling-stroke}
.sub{font-size:34px;font-weight:500;letter-spacing:-.02em;color:#3A3E42;margin-top:26px}
h1{margin:0;font-size:76px;line-height:1.04;letter-spacing:-.045em;font-weight:600;max-width:900px}
.bot{display:flex;justify-content:space-between;align-items:center;font-size:22px}
.go{display:flex;align-items:center;gap:12px;font-weight:600}"""
ARROW = '<svg width="36" height="16" viewBox="0 0 44 20"><path d="M2 10 H38 M30 3 L40 10 L30 17" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def og_html(T, c=None):
    font = '<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600&display=swap" rel="stylesheet">'
    top = f'<div class="top"><span class="lab">Профиль склонностей PAEI</span><span class="mut">{T["short"]}</span></div>'
    bot = (f'<div class="bot"><span><b style="font-weight:600">Владимир Семенюк</b> <span class="mut">· {T["instagram"]}</span></span>'
           f'<span class="go">Пройти тест {ARROW}</span></div>')
    if c is None:
        mid = '<div><h1>Какую роль вы&nbsp;берёте на&nbsp;себя, когда приходится выбирать</h1><p class="sub">20 рабочих ситуаций руководителя · 5 минут</p></div>'
    else:
        letters = "".join(
            f'<span class="{"no" if ch == "-" else ("hi" if ch.isupper() else "lo")}">{"–" if ch == "-" else ch}</span>' for ch in c)
        name = T["names"].get(c)
        ln = lead_names(T, c)
        sub = f"По Адизесу — «{name}»" if name else ("Ведущие роли: " + ", ".join(ln) if ln else "Явной ведущей роли нет")
        mid = (f'<div><div class="code">{letters}<svg viewBox="0 0 200 64" preserveAspectRatio="none"><path d="{RING}"/></svg></div>'
               f'<p class="sub">{html.escape(sub)}</p></div>')
    return f'<!doctype html><html lang="ru"><head><meta charset="utf-8">{font}<style>{OG_CSS}</style></head><body>{top}{mid}{bot}</body></html>'


def shoot(markup, out_jpg):
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "og.html")
        png = os.path.join(tmp, "og.png")
        open(src, "w", encoding="utf-8").write(markup)
        subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--window-size=1200,630", "--virtual-time-budget=5000", f"--screenshot={png}", "file://" + src],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "86", png, "--out", out_jpg],
                       check=True, stdout=subprocess.DEVNULL)


def main():
    test_id = sys.argv[1] if len(sys.argv) > 1 else "paei"
    images = "--no-img" not in sys.argv
    T = load(test_id)
    base = os.path.join(SITE, "tests", test_id)
    rdir = os.path.join(base, "r")
    codes = reachable(T)
    keep = {slug_of(c) for c in codes}
    if os.path.isdir(rdir):
        for d in os.listdir(rdir):
            if d not in keep and os.path.isdir(os.path.join(rdir, d)):
                shutil.rmtree(os.path.join(rdir, d))
    for i, c in enumerate(codes, 1):
        d = os.path.join(rdir, slug_of(c))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(result_page(T, c))
        if images:
            shoot(og_html(T, c), os.path.join(d, "og.jpg"))
            print(f"\r{i}/{len(codes)} {c}  ", end="", flush=True)
    if images:
        shoot(og_html(T), os.path.join(base, "og.jpg"))
    print(f"\nГотово: {len(codes)} страниц профилей" + (" и превью" if images else ""))


if __name__ == "__main__":
    main()
