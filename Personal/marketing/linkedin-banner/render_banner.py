#!/usr/bin/env python3
"""Баннер профиля LinkedIn (1584×396, рендер ×2) в визуальной системе Instagram.

Запуск из корня KnowledgeOS:
    python3 Personal/marketing/linkedin-banner/render_banner.py

Левая треть пустая: снизу слева её перекрывает фото профиля.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "Posts/render"))
import render as R  # noqa: E402

W, H = 1584, 396

# Обводка скопирована с первого экрана semenyuk.pro: тот же путь и пропорции,
# толщина 3,5 px при 72 px на сайте → 3,7 px при 76 px здесь.
RING = (
    '<style>.sm{{position:relative;display:inline-block;white-space:nowrap}}'
    '.sm svg{{position:absolute;overflow:visible;left:-6%;top:-14%;width:112%;height:128%}}'
    '.sm path{{fill:none;stroke:#D2302C;stroke-width:3.7px;stroke-linecap:round;stroke-linejoin:round}}</style>'
    '<span class="sm">Управляйте им<svg viewBox="0 0 200 64" preserveAspectRatio="none" aria-hidden="true">'
    '<path d="M30 12C70 3 150 2 184 14c18 7 16 28-4 38-38 15-122 14-160 3C2 49 2 31 18 21c22-13 76-17 112-13"/></svg></span>'
).replace("{{", "{").replace("}}", "}")

BODY = f"""
<div style="width:{W}px;height:{H}px;background:#F3F4F1;position:relative;overflow:hidden">
  <div style="position:absolute;left:600px;right:88px;top:64px;bottom:60px;display:flex;flex-direction:column;justify-content:space-between">
    <div class="top" style="font-size:20px;padding-top:16px">
      <span class="lab">Метод «Право управлять»</span>
      <span class="mut">для руководителей</span>
    </div>
    <h1 style="font-size:76px;line-height:1.02">Отвечаете за результат?<br>{RING}</h1>
    <div style="font-size:22px;color:#3A3E42">Ex-CTO Нетологии · ex-CIO mos.ru</div>
  </div>
</div>
"""

def main():
    html_path = os.path.join(HERE, "banner.html")
    with open(html_path, "w") as f:
        f.write(R.page(BODY))
    for scale, name in ((2, "linkedin-banner.png"),):
        png = os.path.join(HERE, name)
        subprocess.run([R.CHROME, "--headless=new", "--hide-scrollbars", f"--force-device-scale-factor={scale}",
                        f"--window-size={W},{H}", "--virtual-time-budget=6000", "--allow-file-access-from-files",
                        f"--screenshot={png}", "file://" + html_path],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(png)
    os.remove(html_path)

if __name__ == "__main__":
    main()
