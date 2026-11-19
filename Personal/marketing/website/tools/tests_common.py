"""Общие куски страниц тестов: голова, счётчик Метрики, подвал. Пути относительные: depth — глубина от site/."""

METRIKA = """<!-- Яндекс.Метрика: счётчик 114369053. Цели тестов: test_start, test_finish, tg_send, share, story_image, copy_link. -->
<script>
(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js?id=114369053","ym");
ym(114369053,"init",{ssr:true,webvisor:true,clickmap:true,accurateTrackBounce:true,trackLinks:true});
document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a[data-goal]");if(a)ym(114369053,"reachGoal",a.dataset.goal,{place:a.dataset.place});});
</script>"""

NOSCRIPT = '<noscript><div><img src="https://mc.yandex.ru/watch/114369053" style="position:absolute;left:-9999px" alt=""></div></noscript>'


def up(depth):
    return "../" * depth


def head(depth):
    u = up(depth)
    return f"""<link rel="icon" href="{u}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{u}assets/icons/favicon-32.png">
<link rel="apple-touch-icon" href="{u}assets/icons/apple-touch-icon.png">
<link rel="manifest" href="{u}site.webmanifest">
<meta name="theme-color" content="#F3F4F1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u}tests/assets/tests.css">
{METRIKA}"""


def footer(depth, place):
    u = up(depth)
    return f"""<footer class="site-foot">
  <div class="wrap site-foot__in">
    <ul class="site-foot__links">
      <li><a class="link" href="{u}">Главная</a></li>
      <li><a class="link" href="{u}tests/">Тесты</a></li>
      <li><a class="link" data-goal="tg_write" data-place="{place}-footer" href="https://t.me/vladimirsemenyuk">Telegram</a></li>
      <li><a class="link" data-goal="email_write" data-place="{place}-footer" href="mailto:vladimir@semenyuk.pro">vladimir@semenyuk.pro</a></li>
    </ul>
    <p>©&nbsp;2026 Владимир Семенюк</p>
  </div>
</footer>"""


def fill(html, depth, place):
    return html.replace("@@COMMON_HEAD@@", head(depth)).replace("@@METRIKA_NOSCRIPT@@", NOSCRIPT).replace("@@FOOTER@@", footer(depth, place))
