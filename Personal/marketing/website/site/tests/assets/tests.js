/* Движок тестов semenyuk.pro/tests/. Данные теста — window.TEST (файл data.js в папке теста).
   Страница выбирает режим через <body data-page="test|result|key">.
   Ссылка на результат: <тест>/r/<код>/#s=<версия>.<баллы>&k=<зашифрованное>.
   k — имя, контакт, ответы и дата, зашифрованы открытым ключом Владимира (ECDH P-256 + AES-GCM).
   Закрытый ключ хранится только в браузере Владимира (страница /tests/key/). */
(function(){
'use strict';
var T=window.TEST, page=document.body.dataset.page;
var $=function(id){return document.getElementById(id)};
var KEY_STORE='tests-owner-key';
var UL='M3 6c30-2.5 64-3.5 94 .5';
var ARROW='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';

function goal(name){try{if(window.ym)ym(114369053,'reachGoal',name,{test:T&&T.id})}catch(e){}}
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);if(v===null)localStorage.removeItem(k);else localStorage.setItem(k,v)}catch(e){return null}}
var tt;function toast(m,ms){var el=$('toast');if(!el)return;el.textContent=m;el.classList.add('is-on');clearTimeout(tt);tt=setTimeout(function(){el.classList.remove('is-on')},ms||2600)}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}

/* ---------- подсчёт и показ профиля: scoring.js и profile.js, их же использует сборка страниц ---------- */
var SC=window.TestScoring,P=window.TestProfile,L=T?T.letters:'',RING=P.RING;
var scoresOf=SC.scoresOf,slugOf=SC.slugOf;
function codeOf(s){return SC.codeOf(T,s)}
function validScores(s){return SC.validScores(T,s)}
function status(v){return P.LEVEL[SC.levelOf(T,v)]}

/* ---------- закрытая часть ссылки: crypto.js ---------- */
var CR=window.TestCrypto;
function pack(p){return CR.pack(T,p)}
function unpack(b){return CR.unpack(T,b)}
function encrypt(bytes){return CR.encrypt(T,bytes)}
function decrypt(k,priv){return CR.decrypt(T,k,priv)}

/* ---------- ссылки ---------- */
function rootURL(){return new URL(document.body.dataset.root||'./',location.href)}
function resultURL(c,s,k){var u=new URL('r/'+slugOf(c)+'/',rootURL());u.hash='s='+T.version+'.'+s.join('.')+(k?'&k='+k:'');return u.href}

/* ---------- экран теста ---------- */
function testPage(){
  var N=T.questions.length,KEY='tests-'+T.id+'-progress';
  var S=null;try{S=JSON.parse(store(KEY))}catch(e){}
  if(!S||!S.a||S.v!==T.version)S=fresh();
  function fresh(){return{v:T.version,i:0,a:[],seed:Math.floor(Math.random()*1e9)}}
  function save(){store(KEY,JSON.stringify(S))}
  function rng(seed){return function(){seed|=0;seed=seed+0x6D2B79F5|0;var t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
  function order(qi){var r=rng(S.seed+qi*7919),o=[0,1,2,3];for(var k=3;k>0;k--){var j=Math.floor(r()*(k+1));var t=o[k];o[k]=o[j];o[j]=t}return o}
  var screens={intro:$('s-intro'),q:$('s-q'),contact:$('s-contact')};
  function show(name){
    for(var k in screens)screens[k].hidden=(k!==name);
    var flow=name!=='intro';
    $('nav-tg').hidden=flow;$('nav-step').hidden=!flow;
    window.scrollTo(0,0);
    if(name==='q')renderQ();
    if(name==='contact')$('f-name').focus();
  }
  // вступление: продолжить незаконченное
  var started=S.a.some(function(a){return a&&(a.m>=0||a.s>=0)});
  if(started){$('start-t').textContent='Продолжить с вопроса '+(S.i+1);$('restart').hidden=false}
  $('start').addEventListener('click',function(){if(!started)goal('test_start');show('q')});
  $('restart').addEventListener('click',function(){S=fresh();save();started=false;$('start-t').textContent='Начать тест';$('restart').hidden=true;goal('test_start');show('q')});
  $('quit').addEventListener('click',function(e){e.preventDefault();location.reload()});

  var prog=$('progress');for(var p=0;p<N;p++)prog.appendChild(document.createElement('span'));
  function cur(){return S.a[S.i]||(S.a[S.i]={m:-1,s:-1})}
  function renderQ(){
    var q=T.questions[S.i];
    $('q-h').textContent=q.q;$('step-n').textContent=S.i+1;
    [].forEach.call(prog.children,function(el,k){el.className=k<S.i?'is-done':(k===S.i?'is-now':'')});
    var box=$('opts');box.innerHTML='';
    order(S.i).forEach(function(role){
      var b=document.createElement('button');b.type='button';b.className='opt';b.dataset.role=role;
      b.innerHTML='<span class="opt__t">'+esc(q.o[role])+
        '<svg class="mk mk--ring mk--red" viewBox="0 0 200 64" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="'+RING+'"/></svg>'+
        '<svg class="mk mk--ul" viewBox="0 0 100 10" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="'+UL+'"/></svg>'+
        '</span><span class="sr st"></span>';
      b.addEventListener('click',function(){pick(role)});box.appendChild(b);
    });
    paint();$('back').disabled=(S.i===0);
  }
  function paint(){
    var a=cur();
    [].forEach.call($('opts').children,function(b){var r=+b.dataset.role;
      b.classList.toggle('is-main',a.m===r);b.classList.toggle('is-second',a.s===r);
      b.setAttribute('aria-pressed',a.m===r||a.s===r?'true':'false');
      b.querySelector('.st').textContent=a.m===r?' — больше всего про меня':(a.s===r?' — второй выбор':'')});
    var h=$('q-hint');
    if(a.m<0)h.innerHTML='Обведите, что <b>больше всего</b> про&nbsp;вас';
    else if(a.s<0)h.innerHTML='Теперь подчеркните <b>второе</b> по&nbsp;близости';
    else h.textContent='Принято';
  }
  var timer=null;
  function pick(r){var a=cur();clearTimeout(timer);
    if(a.m===r)a.m=-1;else if(a.s===r)a.s=-1;else if(a.m<0)a.m=r;else a.s=r;
    paint();save();if(a.m>=0&&a.s>=0)timer=setTimeout(next,650)}
  function next(){var body=$('q-body');
    if(S.i<N-1){body.classList.add('is-leaving');setTimeout(function(){S.i++;save();renderQ();body.classList.remove('is-leaving')},180)}
    else show('contact')}
  $('back').addEventListener('click',function(){clearTimeout(timer);if(S.i>0){S.i--;save();renderQ()}});
  document.addEventListener('keydown',function(e){
    if(screens.q.hidden||e.target.tagName==='INPUT'||e.metaKey||e.ctrlKey||e.altKey)return;
    var n=parseInt(e.key,10);if(n>=1&&n<=4){var b=$('opts').children[n-1];if(b)b.click()}
    if(e.key==='Backspace'){e.preventDefault();$('back').click()}
  });

  // контакт
  var nm=$('f-name'),tg=$('f-tg'),ml=$('f-mail');
  if(S.name)nm.value=S.name;if(S.tg)tg.value=S.tg;if(S.mail)ml.value=S.mail;
  $('form').addEventListener('submit',function(e){
    e.preventDefault();
    var name=nm.value.trim(),t=tg.value.trim().replace(/^@/,'').replace(/^https?:\/\/t\.me\//,''),mail=ml.value.trim(),ok=true;
    function err(f,id,bad){$(id).hidden=!bad;if(f)f.setAttribute('aria-invalid',bad?'true':'false');if(bad)ok=false}
    err(nm,'e-name',!name);
    err(tg,'e-tg',!!t&&!/^[A-Za-z0-9_]{5,32}$/.test(t));
    err(ml,'e-mail',!!mail&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(mail));
    err(null,'e-contact',!t&&!mail);
    if(!ok){(document.querySelector('.form [aria-invalid="true"]')||tg).focus();return}
    if(!S.a.length||S.a.length<N||!S.a.every(function(a){return a&&a.m>=0&&a.s>=0})){S.i=S.a.findIndex(function(a){return!a||a.m<0||a.s<0});if(S.i<0)S.i=0;save();show('q');return}
    S.name=name;S.tg=t;S.mail=mail;save();
    var btn=$('form').querySelector('button');btn.disabled=true;
    var s=scoresOf(S.a),c=codeOf(s);
    var go=function(k){
      goal('test_finish');
      try{sessionStorage.setItem('tests-own',slugOf(c))}catch(e){}
      store(KEY,null);
      location.href=resultURL(c,s,k);
    };
    if(window.crypto&&crypto.subtle&&window.TextEncoder){encrypt(pack({ans:S.a,name:name,tg:t,mail:mail})).then(go,function(){go('')})}
    else go('');
  });

  show('intro');
}

/* ---------- страница результата ---------- */
function resultPage(){
  var main=$('res'),pageCode=document.body.dataset.code;
  var h=new URLSearchParams(location.hash.slice(1)),sRaw=h.get('s'),k=h.get('k')||'';
  var s=null;
  if(sRaw){var parts=sRaw.split('.').map(Number);if(parts[0]===T.version&&validScores(parts.slice(1)))s=parts.slice(1)}
  if(sRaw&&!s){renderError();return}
  if(s&&codeOf(s)!==pageCode){renderError();return}
  var c=pageCode,owner=store(KEY_STORE);
  var mode=owner&&k?'owner':(k?'own':'visitor');
  render(c,s,mode);
  if(mode==='owner')decrypt(k,owner).then(function(d){renderOwner(d,s)},function(){renderOwnerFail()});
  // уходим со страницы с закрытой частью в адресе только через кнопки, адрес не меняем

  function renderError(){
    main.innerHTML='<div class="res__err"><h1>Ссылку не удалось прочитать</h1><p>Возможно, она обрезалась при копировании. Пройдите тест заново&nbsp;— это 5&nbsp;минут.</p><a class="btn" href="'+rootURL().href+'">Пройти тест '+ARROW+'</a></div>';
  }
}
function render(c,s,mode){
  var main=$('res'),R=T.roles,nm=T.names[c];
  var lead=P.leadLetters(c),weak=P.weakIndexes(c).map(function(i){return L[i]});
  var top=s?s.indexOf(Math.max.apply(null,s)):L.indexOf(lead[0]||c[0].toUpperCase());
  var CLS={lead:'hi',mid:'lo',weak:'no'};
  var letters=P.glyphs(c).map(function(g){return '<span class="'+CLS[g.level]+'">'+g.g+'</span>'}).join('');
  var who=mode==='visitor'?'Профиль склонностей по&nbsp;модели PAEI':'Ваш профиль склонностей';
  var html='<div class="res__top">'+
    (mode==='visitor'?'<p class="res__flag">Это профиль другого человека. Пройдите тест, чтобы узнать свой.</p>':'')+
    '<h1 class="res__who" id="r-h">'+who+'</h1>'+
    '<p class="code" aria-hidden="true"><span class="m code__m">'+letters+'<svg class="mk mk--ring mk--red mk--draw" viewBox="0 0 200 64" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" style="--d:.35s" d="'+RING+'"/></svg></span></p>'+
    '<p class="sr">Профиль '+c.split('').join(' ').replace(/-/g,'прочерк')+'</p>'+
    '<p class="res__name">'+esc(P.resultLine(T,c))+'</p>'+
    '<p class="res__note">Профиль показывает, к&nbsp;каким ролям вы&nbsp;тянетесь, а&nbsp;не&nbsp;насколько хорошо их&nbsp;исполняете.</p></div>';
  if(s){
    var top2=Math.max.apply(null,s),dm=Math.max(30,top2),z1=T.lo/dm*100,z2=T.hi/dm*100;
    var bars='<div class="bar bar--head" aria-hidden="true"><span class="bar__n"></span><div class="bar__z"><span style="left:0">Слабая</span><span style="left:'+z1+'%">Рабочая</span><span style="left:'+z2+'%">Ведущая</span></div><span class="bar__st"></span><span class="bar__s"></span></div>';
    s.forEach(function(v,i){
      var w=Math.max(v/dm*100,2),st=SC.levelOf(T,v),key=v===top2&&v>=T.hi;
      bars+='<div class="bar bar--'+st+'"><p class="bar__n">'+L[i]+' · '+R[L[i]].n+'</p>'+
        '<div class="bar__track"><i class="bar__weak" style="width:'+z1+'%"></i><i class="bar__lead" style="left:'+z2+'%"></i><i class="bar__tick" style="left:'+z1+'%"></i><i class="bar__tick" style="left:'+z2+'%"></i>'+
        '<span class="bar__line" style="width:'+w+'%"><svg viewBox="0 0 100 14" preserveAspectRatio="none" aria-hidden="true" class="mk mk--draw"><path pathLength="1" style="--d:'+(0.5+i*0.15)+'s" d="'+P.STROKE+'"/></svg></span></div>'+
        '<p class="bar__st">'+status(v)+'</p><p class="bar__s"><span class="m">'+v+(key?'<svg class="mk mk--ring mk--red mk--draw" viewBox="0 0 200 64" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" style="--d:1.3s" d="'+RING+'"/></svg>':'')+'</span></p></div>';
    });
    html+='<div class="boardp"><div class="bars">'+bars+'</div><p class="legend">Всего 60&nbsp;баллов на&nbsp;четыре роли. Слабая зона&nbsp;— до&nbsp;'+(T.lo-1)+'&nbsp;баллов, ведущая роль&nbsp;— от&nbsp;'+T.hi+'.</p></div>';
  }
  var side='';
  if(mode==='own'){
    side='<h2>Разберём профиль на&nbsp;ваших рабочих кейсах</h2><p>Отправьте ссылку&nbsp;— на&nbsp;15&nbsp;минутах знакомства сверим профиль с&nbsp;тем, что происходит у&nbsp;вас в&nbsp;карьере.</p>'+
      '<a class="btn" id="send" target="_blank" rel="noopener" href="#">Отправить результат в&nbsp;Telegram '+ARROW+'</a>'+
      '<div class="share"><button class="btn btn--line btn--sm" id="share">Поделиться</button><button class="btn btn--line btn--sm" id="story">Картинка для&nbsp;сторис</button><button class="btn btn--line btn--sm" id="copy">Скопировать ссылку</button></div>';
  } else if(mode==='visitor'){
    side='<h2>Узнайте свой профиль</h2><p>'+esc(P.nb(T.pitch+', '+T.duration))+', результат сразу.</p><a class="btn" href="'+rootURL().href+'">Пройти тест '+ARROW+'</a>';
  }
  if(side)html+='<div class="side">'+side+'</div>';
  var rows=(lead.length?'<div class="read__row"><h2 class="read__k">Ведущие роли</h2><div class="read__v">'+lead.map(function(r){return '<p><b>'+r+' · '+R[r].n+'.</b> '+esc(R[r].lead)+' '+esc(R[r].over)+'</p>'}).join('')+'</div></div>':'')+
    '<div class="read__row"><h2 class="read__k">Слабые зоны</h2><div class="read__v">'+(weak.length?weak.map(function(r){return '<p><b>'+r+' · '+R[r].n+'.</b> '+esc(R[r].weak)+'</p>'}).join(''):'<p>Слабых зон нет: ни&nbsp;одну роль вы&nbsp;не&nbsp;обходили стороной.</p>')+'</div></div>'+
    '<div class="read__row"><h2 class="read__k">Вопрос к&nbsp;знакомству</h2><div class="read__v"><p class="read__q">'+esc(R[L[top]].q)+'</p></div></div>';
  html+='<div class="read">'+rows+'</div>';
  if(mode==='owner')html+='<div class="own" id="own"><h2>Ответы</h2><p class="own__who">Расшифровываю…</p></div>';
  main.innerHTML=html;
  var drawn=function(){main.querySelectorAll('.code,.bars').forEach(function(el){el.classList.add('is-drawn')})};
  requestAnimationFrame(function(){requestAnimationFrame(drawn)});setTimeout(drawn,120);

  if(mode==='own'){
    var full=location.href, pub=full.split('#')[0]+(s?'#s='+T.version+'.'+s.join('.'):'');
    $('send').href='https://t.me/'+T.telegram+'?text='+encodeURIComponent('Мой профиль PAEI — '+c+': '+full);
    $('send').addEventListener('click',function(){goal('test_tg_send')});
    $('copy').onclick=function(){goal('test_copy');copy(pub)};
    $('share').onclick=function(){goal('test_share');
      if(navigator.share)navigator.share({title:T.title,text:'Мой профиль — '+c+(nm?', «'+nm+'»':''),url:pub}).catch(function(){});
      else copy(pub)};
    $('story').onclick=function(){goal('test_story');storyShare(c,s,nm)};
  }
}
function renderOwner(d,s){
  var el=$('own'),R=T.roles,n=T.questions.length;
  var ss=scoresOf(d.ans),bad=s&&ss.join()!==s.join();
  var who='<p class="own__who"><span><b>'+esc(d.name||'—')+'</b></span>'+
    (d.tg?'<span>Telegram: <a class="link" href="https://t.me/'+encodeURIComponent(d.tg)+'" target="_blank" rel="noopener">@'+esc(d.tg)+'</a></span>':'')+
    (d.mail?'<span>Email: <a class="link" href="mailto:'+esc(d.mail)+'">'+esc(d.mail)+'</a></span>':'')+
    '<span>'+d.date.toLocaleDateString('ru-RU',{day:'numeric',month:'long',year:'numeric'})+'</span></p>';
  var warn=bad?'<p class="own__warn">Баллы в&nbsp;ссылке не&nbsp;совпадают с&nbsp;ответами. По&nbsp;ответам: '+ss.map(function(v,i){return L[i]+' '+v}).join(', ')+' ('+codeOf(ss)+').</p>':'';
  var rows='';
  for(var i=0;i<n;i++){var a=d.ans[i],q=T.questions[i];
    rows+='<tr><td>'+(i+1)+'</td><td>'+esc(q.q)+'</td><td><b>'+L[a.m]+'</b> '+esc(q.o[a.m])+'</td><td><b>'+L[a.s]+'</b> '+esc(q.o[a.s])+'</td></tr>'}
  el.innerHTML='<h2>Ответы</h2>'+who+warn+'<table class="ans"><thead><tr><th>№</th><th>Вопрос</th><th>Главный выбор</th><th>Второй</th></tr></thead><tbody>'+rows+'</tbody></table>';
}
function renderOwnerFail(){var el=$('own');if(el)el.innerHTML='<h2>Ответы</h2><p class="own__warn">Не&nbsp;удалось расшифровать: ссылка повреждена или ключ на&nbsp;этом устройстве не&nbsp;тот.</p>'}
function copy(t){(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){toast('Ссылка скопирована')},function(){window.prompt('Скопируйте ссылку',t)})}

/* ---------- картинка для сторис: рисует profile.js (drawStory) ---------- */
function storyShare(c,s,nm){
  var hint='Добавьте в сторис стикер «Ссылка» с адресом '+T.short+' и отметьте '+T.instagram;
  P.fontsReady().then(function(){P.drawStory(T,c,s).toBlob(function(blob){
    var file=new File([blob],'profil-paei-'+slugOf(c)+'.png',{type:'image/png'});
    if(navigator.canShare&&navigator.canShare({files:[file]})){navigator.share({files:[file]}).then(function(){toast(hint,7000)}).catch(function(){})}
    else{var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=file.name;document.body.appendChild(a);a.click();a.remove();
      setTimeout(function(){URL.revokeObjectURL(a.href)},4000);toast('Картинка сохранена. '+hint,7000)}
  },'image/png')});
}

/* ---------- страница ключа ---------- */
function keyPage(){
  var ta=$('key'),st=$('key-state');
  function upd(){var has=!!store(KEY_STORE);st.textContent=has?'Ключ сохранён в этом браузере. Ссылки на результаты будут показывать имя, контакт и ответы.':'Ключа в этом браузере нет.';$('key-del').hidden=!has}
  $('key-save').addEventListener('click',function(){
    var v=ta.value.trim();if(!v){ta.focus();return}
    CR.importPrivate(v).then(function(){store(KEY_STORE,v);ta.value='';upd();toast('Ключ сохранён')},function(){toast('Это не похоже на ключ: проверьте, что скопирован целиком')});
  });
  $('key-del').addEventListener('click',function(){store(KEY_STORE,null);upd();toast('Ключ удалён из этого браузера')});
  upd();
}

window.__tests={storyDraw:function(c,s){return P.drawStory(T,c,s)},encrypt:encrypt,decrypt:decrypt,pack:pack,unpack:unpack,codeOf:codeOf,slugOf:slugOf,scoresOf:scoresOf};
if(page==='result')window.addEventListener('hashchange',function(){location.reload()});
if(page==='test')testPage();else if(page==='result')resultPage();else if(page==='key')keyPage();
})();
