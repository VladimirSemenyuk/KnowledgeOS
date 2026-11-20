#!/usr/bin/env python3
"""Рендер слайдов Instagram в PNG по визуальной системе «Доска после разбора».

Запуск из корня KnowledgeOS:
    python3 Posts/render/render.py Posts/render/slides/instagram.py [префикс имени]

Файл данных объявляет CHANNEL и список SLIDES: каждый элемент — dict с ключами
`name` (имя PNG без расширения), `kind` (шаблон), `week` (папка недели) и полями шаблона.
PNG пишутся в Posts/weeks/<week>/<CHANNEL>/img/. Сводный лист для проверки —
во временной папке, путь печатается в конце.

Разметка в тексте:
    [[o:текст]] — красный обвод, [[u:текст]] — красное подчёркивание (переносится по строкам),
    [[s:текст]] — зачёркивание чёрным, [[b:текст]] — полужирный.
На поверхность — одна красная пометка.
"""
import html
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
IMG = os.path.join(ROOT, "Personal/marketing/website/site/assets/img")

FONT = '<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600&display=swap" rel="stylesheet">'

CSS = """
*{box-sizing:border-box}
body{margin:0;font-family:Onest,system-ui,sans-serif;color:#16181A;-webkit-font-smoothing:antialiased}
.f{display:flex;flex-direction:column;justify-content:space-between;padding:96px 96px 88px;background:#F3F4F1}
.paper{background:#FAFAF8}
.dark{background:#16181A;color:#F3F4F1}
.top{display:flex;justify-content:space-between;align-items:baseline;border-top:3px solid currentColor;padding-top:22px;font-size:26px}
.lab{font-weight:600;letter-spacing:.08em;text-transform:uppercase}
.mut{color:#5E6469}
.dark .mut{color:#A9AFB3}
.bot{display:flex;justify-content:space-between;align-items:center;font-size:26px}
.bot.rule{border-top:1px solid #BFC4C6;padding-top:22px}
h1{margin:0;font-weight:600;letter-spacing:-.045em;line-height:1.02}
.sub{margin:0;font-size:44px;font-weight:500;line-height:1.3;letter-spacing:-.02em;color:#3A3E42}
.dark .sub{color:#D8DBD8}
.body p{margin:0 0 28px;font-size:54px;font-weight:500;line-height:1.24;letter-spacing:-.03em}
.rows{display:flex;flex-direction:column;border-top:3px solid currentColor}
.row{display:grid;gap:32px;padding:28px 0;border-bottom:1px solid #D8DBD8}
.row .k{font-size:24px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#5E6469;padding-top:8px}
.row .v{font-size:36px;line-height:1.3;letter-spacing:-.02em}
.row.big .k{font-size:40px;letter-spacing:-.02em;text-transform:none;color:#16181A;padding-top:0}
.pill{height:120px;width:100%;border-radius:999px;background:#16181A;color:#F3F4F1;font-size:40px;font-weight:600;display:flex;align-items:center;justify-content:center;gap:20px}
.dark .pill{background:#F3F4F1;color:#16181A}
.m{position:relative;white-space:nowrap}
.m svg{position:absolute;overflow:visible}
.u{padding:0 .01em .07em;margin:0 -.01em;background-repeat:no-repeat;background-position:0 100%;background-size:100% .14em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.s{text-decoration:line-through;text-decoration-thickness:3px;color:#5E6469}
.panel{background:#F3F4F1;border-radius:6px;box-shadow:0 0 0 1px #D8DBD8,0 36px 80px -56px rgba(22,24,26,.35)}
.st{display:flex;flex-direction:column;justify-content:space-between;gap:56px;padding:260px 88px 360px;background:#FAFAF8}
.ava{border-radius:50%;object-fit:cover;filter:grayscale(1)}
"""

ARROW = '<svg width="44" height="20" viewBox="0 0 44 20" aria-hidden="true"><path d="M2 10 H38 M30 3 L40 10 L30 17" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
# Подчёркивание — фон строки, а не SVG поверх: фраза переносится, каждая строка получает свою линию.
UNDER = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 24" preserveAspectRatio="none"><path d="M6 14 C 140 6, 320 20, 594 8" fill="none" stroke="#D2302C" stroke-width="{w}" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>'


def under_bg(w):
    return "url(&quot;data:image/svg+xml," + urllib.parse.quote(UNDER.format(w=w)) + "&quot;)"
CHECK = '<svg width="{s}" height="{h}" viewBox="0 0 14 10" aria-hidden="true"><path d="M1.5 6.5 L5 9 L12.5 1.5" fill="none" stroke="#D2302C" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

SHORT = r"(?:в|и|с|к|о|у|а|я|не|на|по|за|из|до|от|без|для|при|что|как|но|во|со|об|их|его|её|мы|вы|он|это|или|ли|же|бы|ни|раз)"


def typo(t):
    t = re.sub(r"(?i)(^|[\s(«:])(" + SHORT + r") ", lambda m: m.group(1) + m.group(2) + "\u00a0", t)
    t = re.sub(r"(?i)(^|[\s(«:])(" + SHORT + r") ", lambda m: m.group(1) + m.group(2) + "\u00a0", t)
    t = t.replace(" —", "\u00a0—")
    t = re.sub(r"(\d) (?=\S)", "\\1\u00a0", t)
    return t


def md(t, w=5):
    """Текст с разметкой пометок → HTML."""
    t = html.escape(typo(t), quote=False)

    def rep(m):
        kind, inner = m.group(1), m.group(2)
        if kind == "o":
            return f'<span class="m o" data-w="{w}">{inner}</span>'  # контур рисует OVAL_JS
        if kind == "u":
            return f'<span class="u" style="background-image:{under_bg(w + 2)}">{inner}</span>'
        if kind == "s":
            return f'<span class="s">{inner}</span>'
        if kind == "b":
            return f"<b style=\"font-weight:600\">{inner}</b>"
        return inner

    inner_re = re.compile(r"\[\[([ousb]):((?:(?!\[\[).)+?)\]\]")
    while True:  # раскрываем изнутри наружу: допускается [[b:… [[o:…]] …]]
        t2 = inner_re.sub(rep, t)
        if t2 == t:
            break
        t = t2
    return t.replace("\n", "<br>")


def img(name):
    return "file://" + os.path.join(IMG, name)


HANDLE = "@vladimir.semenyuk"
SIGN = '<span style="font-weight:600">Владимир Семенюк</span>'
SIGN_HANDLE = f'<span style="font-weight:600">Владимир Семенюк <span class="mut" style="font-weight:400">· {HANDLE}</span></span>'


def top(label, right):
    return f'<div class="top"><span class="lab">{md(label)}</span><span class="mut">{md(right)}</span></div>'


def bottom(right="", rule=False, arrow=False, handle=False):
    """Подпись внизу: имя и ник в Instagram — на всех слайдах (решение 2026-11-15)."""
    r = f'<span style="display:flex;align-items:center;gap:14px;font-weight:600">{md(right)}{ARROW}</span>' if arrow else f'<span class="mut">{md(right)}</span>'
    return f'<div class="bot{" rule" if rule else ""}">{SIGN_HANDLE}{r}</div>'


def rows_html(rows, kw=280, big=False, vsize=None):
    out = ['<div class="rows">']
    for k, v in rows:
        vs = f' style="font-size:{vsize}px"' if vsize else ""
        out.append(f'<div class="row{" big" if big else ""}" style="grid-template-columns:{kw}px 1fr"><span class="k">{md(k)}</span><span class="v"{vs}>{md(v)}</span></div>')
    out.append("</div>")
    return "".join(out)


# ---------- шаблоны ленты 1080×1350 ----------

def t_cover(s):
    """Обложка карусели или пост-заявление: крупный заголовок."""
    cls = "f dark" if s.get("dark") else "f"
    sub = f'<p class="sub" style="margin-top:44px">{md(s["sub"])}</p>' if s.get("sub") else ""
    table = ""
    if s.get("table"):
        table = '<div class="rows">' + "".join(
            f'<div class="row" style="grid-template-columns:90px 1fr auto;padding:20px 0;align-items:baseline"><span class="k" style="padding:0">{n}</span><span style="font-size:42px;font-weight:600;letter-spacing:-.03em">{md(a)}</span><span style="font-size:26px;color:#3A3E42">{md(b)}</span></div>'
            for n, a, b in s["table"]) + "</div>"
    return (f'<div class="{cls}" style="width:1080px;height:1350px">{top(s["label"], s["counter"])}'
            f'<div><h1 style="font-size:{s.get("size", 112)}px">{md(s["title"], 7)}</h1>{sub}</div>{table}'
            f'{bottom(s.get("foot", "Листайте"), arrow=s.get("arrow", True), handle=s.get("handle"))}</div>')


def t_text(s):
    """Слайд: заголовок, абзацы, опционально строки и кнопка."""
    paras = "".join(f"<p>{md(p)}</p>" for p in s.get("body", []))
    rows = rows_html(s["rows"], s.get("kw", 280), vsize=s.get("vsize")) if s.get("rows") else ""
    pill = f'<div class="pill">{md(s["pill"])}{ARROW}</div>' if s.get("pill") else ""
    after = f'<p class="sub" style="margin-top:36px;color:#16181A;font-weight:600">{md(s["after"])}</p>' if s.get("after") else ""
    return (f'<div class="f" style="width:1080px;height:1350px">{top(s["label"], s["counter"])}'
            f'<div style="display:flex;flex-direction:column;gap:44px"><h1 style="font-size:{s.get("size", 92)}px">{md(s["title"], 7)}</h1>'
            f'<div class="body">{paras}</div></div>'
            f'<div style="display:flex;flex-direction:column;gap:40px">{rows}{after}{pill}</div>'
            f'{bottom(s.get("foot", ""), handle=s.get("handle"))}</div>')


def t_position(s):
    rows = rows_html([("Как видно", s["see"]), ("Цена", s["cost"]), ("Шаг", "[[b:" + s["step"] + "]]" if "[[" not in s["step"] else s["step"])])
    return (f'<div class="f" style="width:1080px;height:1350px">{top(s["label"], s["counter"])}'
            f'<div style="display:flex;flex-direction:column;gap:28px"><h1 style="font-size:{s.get("size", 140)}px;letter-spacing:-.05em;line-height:1">{md(s["title"])}</h1>'
            f'<p class="sub">{md(s["quote"])}</p></div>{rows}{bottom(s["foot"], handle=s.get("handle"))}</div>')


def t_thesis(s):
    return (f'<div class="f" style="width:1080px;height:1350px">{top(s["label"], s["counter"])}'
            f'<div style="display:flex;flex-direction:column;gap:56px"><h1 style="font-size:{s.get("size", 116)}px">{md(s["title"], 7)}</h1>'
            f'<p class="sub" style="max-width:820px;font-size:38px;line-height:1.32">{md(s["sub"])}</p></div>'
            f'{bottom(rule=True, handle=True)}</div>')


def t_review(s, story=False):
    w, h = (1080, 1920) if story else (1080, 1350)
    cls = "st" if story else "f"
    head = (f'<div style="display:flex;flex-direction:column;gap:24px"><span class="lab mut" style="font-size:28px">Голос клиента</span></div>'
            if story else top("Голос клиента", "с согласия автора"))
    foot = f'<div style="font-size:26px">{SIGN_HANDLE}</div>' if story else bottom(handle=True)
    return (f'<div class="{cls}" style="width:{w}px;height:{h}px">{head}'
            f'<blockquote style="margin:0;font-size:{s.get("size", 64)}px;font-weight:500;line-height:1.22;letter-spacing:-.03em">{md(s["quote"], 7)}</blockquote>'
            f'<div style="display:flex;flex-direction:column;gap:40px"><div style="display:flex;align-items:center;gap:28px;border-top:1px solid #BFC4C6;padding-top:32px">'
            + (f'<img class="ava" src="{img("reviews/" + s["photo"])}" style="width:120px;height:120px">' if s.get("photo") else '') +
            f'<div style="display:flex;flex-direction:column;gap:6px"><span style="font-size:36px;font-weight:600;letter-spacing:-.02em">{md(s["who"])}</span>'
            f'<span style="font-size:28px;color:#3A3E42">{md(s["role"])}</span></div></div>{foot}</div></div>')


def case_panel(s, fs=34):
    was = "".join(f'<span style="font-size:{fs}px;line-height:1.3" class="s">{md(x)}</span>' for x in s["was"])
    now = "".join(f'<span style="font-size:{fs}px;font-weight:600;line-height:1.3">{md(x)}</span>' for x in s["now"])
    arrow = '<svg width="72" height="40" viewBox="0 0 72 40" style="margin-top:120px" aria-hidden="true"><path d="M4 21 C 24 18, 44 22, 62 20 M50 9 L64 20 L50 31" fill="none" stroke="#16181A" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    lab = '<span style="font-size:24px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#5E6469">{}</span>'
    return (f'<div class="panel" style="padding:56px;display:grid;grid-template-columns:1fr 72px 1fr;gap:24px;align-items:start">'
            f'<div style="display:flex;flex-direction:column;gap:26px">{lab.format("Было")}{was}</div>{arrow}'
            f'<div style="display:flex;flex-direction:column;gap:26px">{lab.format("Стало")}{now}</div></div>')


def t_case(s):
    return (f'<div class="f paper" style="width:1080px;height:1350px;padding:96px 80px 88px;gap:56px;justify-content:flex-start">'
            f'<div style="margin:0 16px">{top(s["label"], s["counter"])}</div>'
            f'<h1 style="margin:0 16px;font-size:80px;line-height:1.04;letter-spacing:-.04em">{md(s["title"])}</h1>'
            f'<div style="flex-grow:1;display:flex;flex-direction:column;justify-content:center">{case_panel(s)}</div>'
            f'<div style="margin:0 16px">{bottom(s.get("foot", ""), handle=True)}</div></div>')


# ---------- сторис 1080×1920 ----------

def t_story(s):
    head = [f'<span class="lab mut" style="font-size:28px">{md(s["label"])}</span>'] if s.get("label") else []
    if s.get("photo"):
        head.insert(0, f'<img class="ava" src="{img(s["photo"])}" style="width:300px;height:300px;object-position:50% 22%">')
    head.append(f'<h1 style="font-size:{s.get("size", 120)}px;letter-spacing:-.05em;line-height:1">{md(s["title"], 7)}</h1>')
    if s.get("sub"):
        head.append(f'<p class="sub" style="font-size:40px">{md(s["sub"])}</p>')
    mid = ""
    if s.get("lines"):  # регалии одна под другой
        mid = '<div class="rows">' + "".join(
            f'<div style="font-size:38px;font-weight:500;letter-spacing:-.02em;line-height:1.2;padding:20px 0;border-bottom:1px solid #D8DBD8">{md(x)}</div>'
            for x in s["lines"]) + "</div>"
    if s.get("stats"):  # крупные цифры
        mid = '<div style="display:flex;flex-direction:column;gap:36px">' + "".join(
            f'<div style="display:flex;flex-direction:column;gap:4px;border-top:3px solid #16181A;padding-top:18px">'
            f'<span style="font-size:{st.get("size", 120)}px;font-weight:600;letter-spacing:-.05em;line-height:.95">{md(st["n"])}</span>'
            f'<span style="font-size:34px;font-weight:500;letter-spacing:-.02em;color:#3A3E42">{md(st["t"])}</span></div>'
            for st in s["stats"]) + (f'<p class="sub" style="font-size:34px;margin-top:8px">{md(s["note"])}</p>' if s.get("note") else "") + "</div>"
    if s.get("rows"):
        mid = f'<div class="panel" style="padding:20px 52px">{rows_html(s["rows"], s.get("kw", 220), vsize=s.get("vsize", 38)).replace("border-top:3px", "border-top:0px")}</div>'
        mid = mid.replace('class="rows"', 'class="rows" style="border-top:0"')
    if s.get("case"):
        mid = case_panel(s["case"], 32)
    foot = (f'<div style="display:flex;flex-direction:column;align-items:center;gap:24px"><div class="pill">{md(s["pill"])}{ARROW}</div>'
            f'<span style="font-size:26px;color:#5E6469">Владимир Семенюк · {HANDLE}</span></div>'
            if s.get("pill") else f'<div style="font-size:26px">{SIGN_HANDLE}</div>')
    return (f'<div class="st" style="width:1080px;height:1920px"><div style="display:flex;flex-direction:column;gap:32px">{"".join(head)}</div>'
            f'{mid}{foot}</div>')


def t_story_review(s):
    return t_review(s, story=True)


def t_highlight(s):
    """Обложка Актуального: Instagram вырезает круг по центру."""
    check = CHECK.format(s=160, h=114).replace('stroke-width="1.6"', 'stroke-width="2"')  # в кружке 64 px мелкая галочка теряется
    return (f'<div style="width:1080px;height:1920px;background:#F3F4F1;display:flex;align-items:center;justify-content:center">'
            f'<div style="position:relative;width:1080px;height:1080px;display:flex;align-items:center;justify-content:center">'
            f'<span style="white-space:nowrap;font-size:{s.get("size", 120)}px;font-weight:600;letter-spacing:-.04em;line-height:1">{html.escape(s["word"])}</span>'
            # галочка в одном месте на всех обложках: над правым краем слова, не задевая букв
            f'<span style="position:absolute;top:300px;left:740px">{check}</span></div></div>')


def t_reel_cover(s):
    """Обложка Reels: смысловая зона — центр 1080×1350, сетка режет края."""
    return (f'<div style="width:1080px;height:1920px;background:#F3F4F1;padding:285px 96px">'
            f'<div style="height:1350px;display:flex;flex-direction:column;justify-content:space-between;padding:60px 0 50px">'
            f'{top(s["label"], "Reels")}'
            f'<h1 style="font-size:{s.get("size", 118)}px">{md(s["title"], 7)}</h1>'
            f'{bottom(handle=True)}</div></div>')


def photo_src(p):
    return "file://" + (p if os.path.isabs(p) else os.path.join(ROOT, p))


def t_photo(s, h=1350, safe_top=0):
    """Кадр с заголовком. Фото всегда ч/б.

    layout="split" (по умолчанию) — фото сверху, заголовок на доске снизу: работает с любым кадром.
    layout="dark" — белый заголовок прямо на тёмной части кадра (пиджак, тёмный фон). Без градиентов:
    берём только кадры, где низ и так тёмный.
    Поля: photo (путь от корня KnowledgeOS), pos (object-position), title, label, size, zoom.
    color=True — кадр в цвете: для обложек Reels из самого ролика, где видео идёт в цвете.
    """
    pos, zoom = s.get("pos", "50% 30%"), s.get("zoom", 1)
    flt = "none" if s.get("color") else "grayscale(1) contrast(1.05)"
    im = (f'<img src="{photo_src(s["photo"])}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;'
          f'object-position:{pos};filter:{flt};transform:scale({zoom});transform-origin:{pos}">')
    lab = f'<span class="lab" style="font-size:26px">{md(s["label"])}</span>' if s.get("label") else ""
    safe = 1350  # смысловая зона 4:5 — её видно в сетке
    pad_b = h - safe_top - safe  # что ниже смысловой зоны
    if s.get("layout") == "dark":
        sign = f'<div style="font-size:26px;opacity:.85">{SIGN_HANDLE}</div>' if s.get("sign", True) else ""
        title = md(s["title"], 7)
        if s.get("plate"):  # тёмная плашка под каждой строкой, как у субтитров в ролике
            pl = "background-color:rgba(22,24,26,.88);box-decoration-break:clone;-webkit-box-decoration-break:clone"
            title = f'<span style="{pl};padding:2px 22px 10px;border-radius:14px;line-height:1.32">{title}</span>'
            if lab:
                lab = f'<span class="lab" style="font-size:26px;{pl};padding:10px 16px;border-radius:10px;align-self:flex-start">{md(s["label"])}</span>'
        return (f'<div class="dark" style="position:relative;width:1080px;height:{h}px;overflow:hidden">{im}'
                f'<div style="position:absolute;left:{74 if s.get("plate") else 96}px;right:74px;bottom:{pad_b + 88}px;display:flex;flex-direction:column;gap:{20 if s.get("plate") else 36}px">'
                f'{lab}<h1 style="font-size:{s.get("size", 112)}px;color:#F3F4F1">{title}</h1>'
                f'{sign}</div></div>')
    board = s.get("board", 560)  # высота доски с заголовком внутри смысловой зоны
    return (f'<div style="position:relative;width:1080px;height:{h}px;overflow:hidden;background:#F3F4F1">'
            f'<div style="position:absolute;left:0;right:0;top:0;height:{h - pad_b - board}px;overflow:hidden">{im}</div>'
            f'<div style="position:absolute;left:96px;right:96px;bottom:{pad_b + 80}px;height:{board - 80}px;display:flex;flex-direction:column;justify-content:space-between;padding-top:56px">'
            f'<div style="display:flex;flex-direction:column;gap:28px">{lab}<h1 style="font-size:{s.get("size", 104)}px">{md(s["title"], 7)}</h1></div>'
            f'{bottom(handle=True)}</div></div>')


def t_reel_photo(s):
    """Обложка Reels с кадром: 9:16, смысловая зона — центр 1080×1350."""
    return t_photo(s, h=1920, safe_top=285)


KINDS = {
    "photo": (t_photo, 1080, 1350), "reel_photo": (t_reel_photo, 1080, 1920),
    "cover": (t_cover, 1080, 1350), "text": (t_text, 1080, 1350), "position": (t_position, 1080, 1350),
    "thesis": (t_thesis, 1080, 1350), "review": (t_review, 1080, 1350), "case": (t_case, 1080, 1350),
    "story": (t_story, 1080, 1920), "story_review": (t_story_review, 1080, 1920),
    "highlight": (t_highlight, 1080, 1920), "reel_cover": (t_reel_cover, 1080, 1920),
}


# Красный обвод — рукописный овал трёх форм по длине обводимого:
#   короткое слово (ширина < 2,5 высоты) — почти круглый эллипс;
#   среднее (до 6 высот) — овал чуть полнее эллипса;
#   длинная фраза — «мягкий» овал (суперэллипс), чтобы не уходить далеко в стороны.
# Размер считается так, чтобы буквы целиком оставались внутри. Конец линии заходит за начало, как от руки.
OVAL_JS = """
<script>
document.fonts.ready.then(function () {
  document.querySelectorAll('.m.o').forEach(function (el, idx) {
    var fs = parseFloat(getComputedStyle(el).fontSize), sw = +el.dataset.w * 0.9;
    var probe = document.createElement('span');
    probe.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline';
    el.insertBefore(probe, el.firstChild);
    var r = el.getBoundingClientRect(), bl = probe.getBoundingClientRect().top;
    probe.remove();
    var ns0 = 'http://www.w3.org/2000/svg';
    // Обвод выделяет понятие — одно-два слова. Мысль из трёх и больше слов — подчёркивание:
    // овал вокруг длинной фразы становится плоским и задевает соседние строки.
    var words = el.textContent.trim().split(/\s+/).length;
    if (words >= 3) {
      var uy = bl - r.top + 0.17 * fs, uw = r.width, sv = document.createElementNS(ns0, 'svg'), up = document.createElementNS(ns0, 'path');
      var ud = 'M' + (-0.02 * uw) + ',' + (uy + 0.04 * fs) + ' C' + (0.3 * uw) + ',' + (uy - 0.05 * fs) + ' ' + (0.6 * uw) + ',' + (uy + 0.07 * fs) + ' ' + (1.02 * uw) + ',' + (uy - 0.02 * fs);
      sv.setAttribute('width', uw); sv.setAttribute('height', r.height); sv.setAttribute('aria-hidden', 'true');
      sv.style.cssText = 'position:absolute;overflow:visible;left:0;top:0';
      up.setAttribute('d', ud); up.setAttribute('fill', 'none'); up.setAttribute('stroke', '#D2302C');
      up.setAttribute('stroke-width', Math.max(5, 0.12 * fs)); up.setAttribute('stroke-linecap', 'round');
      sv.appendChild(up); el.appendChild(sv); return;
    }
    var tw = r.width, th = 0.88 * fs, cy = bl - 0.74 * fs + th / 2 - r.top, cx = tw / 2;
    var ratio = tw / th, n, k;
    var tilt = 0;
    if (ratio < 2.5) { n = 2; k = 1.7; tilt = -0.03; }  // короткое слово: эллипс с лёгким наклоном
    else if (ratio < 6) { n = 2.6; k = 1.6; }  // среднее: овал полнее эллипса
    else { n = 3.2; k = 1.5; }                  // длинная фраза: мягкий овал без наклона
    var b = k * th / 2;
    var a = (tw / 2) / Math.pow(1 - Math.pow(th / 2 / b, n), 1 / n) + 0.06 * fs;
    var ph = idx * 1.7, pts = [], N = 90, t0 = Math.PI * 0.82, span = Math.PI * 2 + 0.45;
    for (var i = 0; i <= N; i++) {
      var t = t0 + span * i / N, c = Math.cos(t), s = Math.sin(t);
      var rr = 1 + 0.018 * Math.sin(3 * t + ph) + (i / N - 0.5) * 0.035;
      var x = a * rr * Math.sign(c) * Math.pow(Math.abs(c), 2 / n);
      var y = b * rr * Math.sign(s) * Math.pow(Math.abs(s), 2 / n);
      pts.push([cx + x * Math.cos(tilt) - y * Math.sin(tilt), cy + x * Math.sin(tilt) + y * Math.cos(tilt)]);
    }
    var d = 'M' + pts[0][0].toFixed(1) + ',' + pts[0][1].toFixed(1);
    for (var j = 0; j < pts.length - 1; j++) {
      var p0 = pts[Math.max(j - 1, 0)], p1 = pts[j], p2 = pts[j + 1], p3 = pts[Math.min(j + 2, pts.length - 1)];
      d += ' C' + (p1[0] + (p2[0] - p0[0]) / 6).toFixed(1) + ',' + (p1[1] + (p2[1] - p0[1]) / 6).toFixed(1) + ' ' +
           (p2[0] - (p3[0] - p1[0]) / 6).toFixed(1) + ',' + (p2[1] - (p3[1] - p1[1]) / 6).toFixed(1) + ' ' +
           p2[0].toFixed(1) + ',' + p2[1].toFixed(1);
    }
    var ns = 'http://www.w3.org/2000/svg', svg = document.createElementNS(ns, 'svg'), path = document.createElementNS(ns, 'path');
    svg.setAttribute('width', tw); svg.setAttribute('height', r.height); svg.setAttribute('aria-hidden', 'true');
    svg.style.cssText = 'position:absolute;overflow:visible;left:0;top:0';
    path.setAttribute('d', d); path.setAttribute('fill', 'none'); path.setAttribute('stroke', '#D2302C');
    path.setAttribute('stroke-width', sw); path.setAttribute('stroke-linecap', 'round'); path.setAttribute('stroke-linejoin', 'round');
    svg.appendChild(path); el.appendChild(svg);
  });
});
</script>
"""


def page(body):
    return f'<!doctype html><html lang="ru"><head><meta charset="utf-8">{FONT}<style>{CSS}</style></head><body>{body}{OVAL_JS}</body></html>'


def shot(html_path, png, w, h, tries=3):
    for i in range(tries):  # Chrome изредка падает на старте — повторяем
        try:
            return _shot(html_path, png, w, h)
        except subprocess.CalledProcessError:
            if i == tries - 1:
                raise


def _shot(html_path, png, w, h):
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={w},{h}", "--virtual-time-budget=6000", "--allow-file-access-from-files",
                    f"--screenshot={png}", "file://" + html_path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main(data_path, only=None):
    spec = importlib.util.spec_from_file_location("slides", data_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # Подпись под другой канал: HANDLE в файле данных, "" — только имя (LinkedIn).
    global SIGN_HANDLE
    if hasattr(mod, "HANDLE"):
        SIGN_HANDLE = (f'<span style="font-weight:600">Владимир Семенюк <span class="mut" style="font-weight:400">· {mod.HANDLE}</span></span>'
                       if mod.HANDLE else SIGN)
    def out_dir(s):
        if "week" not in s:
            return os.path.join(os.path.dirname(os.path.abspath(data_path)), "img")
        return os.path.join(ROOT, "Posts", "weeks", s["week"], mod.CHANNEL, "img")
    tmp = tempfile.mkdtemp(prefix="ig-render-")
    names = []
    for s in mod.SLIDES:
        if only and not s["name"].startswith(only):
            continue
        fn, w, h = KINDS[s["kind"]]
        hp = os.path.join(tmp, s["name"] + ".html")
        with open(hp, "w") as f:
            f.write(page(fn(s)))
        out = out_dir(s)
        os.makedirs(out, exist_ok=True)
        shot(hp, os.path.join(out, s["name"] + ".png"), w, h)
        names.append((os.path.join(out, s["name"] + ".png"), h))
        print("ok", s["name"])
    # сводный лист для проверки
    cells = "".join(f'<figure style="margin:0"><img src="file://{p}" style="width:270px;height:{h // 4}px;display:block;box-shadow:0 0 0 1px #ccc"><figcaption style="font:12px system-ui">{os.path.basename(p)[:-4]}</figcaption></figure>' for p, h in names)
    hp = os.path.join(tmp, "_contact.html")
    with open(hp, "w") as f:
        f.write(f'<!doctype html><body style="margin:0;padding:16px;background:#fff;display:flex;flex-wrap:wrap;gap:16px;width:1800px">{cells}</body>')
    rows = (len(names) + 5) // 6
    shot(hp, os.path.join(tmp, "_contact.png"), 1832, rows * 520 + 40)
    print("сводный лист:", os.path.join(tmp, "_contact.png"))
    # PDF-карусели для LinkedIn: PDFS = {"имя.pdf": "префикс слайдов"}, PDF кладётся в папку канала недели.
    for pdf, prefix in getattr(mod, "PDFS", {}).items():
        try:
            from PIL import Image
        except ImportError:
            print("PDF пропущен: нет Pillow, запустите через Posts/render/.venv/bin/python")
            break
        part = [s for s in mod.SLIDES if s["name"].startswith(prefix)]
        pages = [Image.open(os.path.join(out_dir(s), s["name"] + ".png")).convert("RGB") for s in part]
        dst = os.path.join(os.path.dirname(out_dir(part[0])), pdf)
        pages[0].save(dst, save_all=True, append_images=pages[1:], resolution=144)
        print("pdf", pdf, len(pages))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
