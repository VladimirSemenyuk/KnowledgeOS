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
var RING='M30 12C70 3 150 2 184 14c18 7 16 28-4 38-38 15-122 14-160 3C2 49 2 31 18 21c22-13 76-17 112-13';
var UL='M3 6c30-2.5 64-3.5 94 .5';
var ARROW='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';

function goal(name){try{if(window.ym)ym(114369053,'reachGoal',name,{test:T&&T.id})}catch(e){}}
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);if(v===null)localStorage.removeItem(k);else localStorage.setItem(k,v)}catch(e){return null}}
var tt;function toast(m,ms){var el=$('toast');if(!el)return;el.textContent=m;el.classList.add('is-on');clearTimeout(tt);tt=setTimeout(function(){el.classList.remove('is-on')},ms||2600)}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}

/* ---------- подсчёт ---------- */
var L=T?T.letters:'';
function scoresOf(ans){var s=[0,0,0,0];ans.forEach(function(a){if(!a)return;if(a.m>=0)s[a.m]+=2;if(a.s>=0)s[a.s]+=1});return s}
function codeOf(s){return s.map(function(v,i){return v>=T.hi?L[i]:(v>=T.lo?L[i].toLowerCase():'-')}).join('')}
function slugOf(c){return c.split('').map(function(ch){return ch==='-'?'0':(ch===ch.toUpperCase()?ch.toLowerCase()+ch.toLowerCase():ch)}).join('')}
function isHi(ch){return ch!=='-'&&ch===ch.toUpperCase()}
function status(v){return v>=T.hi?'ведущая':(v>=T.lo?'рабочая':'слабая')}
function validScores(s){return s.length===4&&s.every(function(v){return v>=0&&v<=T.max})&&s.reduce(function(a,b){return a+b},0)===T.questions.length*3}

/* ---------- кодирование и шифрование ---------- */
function b64u(buf){var b=new Uint8Array(buf),s='';for(var i=0;i<b.length;i++)s+=String.fromCharCode(b[i]);return btoa(s).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'')}
function unb64u(str){str=str.replace(/-/g,'+').replace(/_/g,'/');while(str.length%4)str+='=';var s=atob(str),b=new Uint8Array(s.length);for(var i=0;i<s.length;i++)b[i]=s.charCodeAt(i);return b}
var EPOCH=Date.UTC(2026,0,1);
function pack(p){
  var enc=new TextEncoder(),parts=[p.name,p.tg,p.mail].map(function(x){return enc.encode(x||'').slice(0,255)});
  var n=Math.ceil(p.ans.length/2),head=new Uint8Array(3+n),days=Math.floor((Date.now()-EPOCH)/864e5);
  head[0]=T.version;head[1]=days&255;head[2]=(days>>8)&255;
  p.ans.forEach(function(a,i){var nib=(a.m<<2)|a.s;head[3+(i>>1)]|=(i&1)?nib:(nib<<4)});
  var len=head.length+parts.reduce(function(a,b){return a+1+b.length},0),out=new Uint8Array(len),o=head.length;
  out.set(head,0);parts.forEach(function(b){out[o++]=b.length;out.set(b,o);o+=b.length});
  return out;
}
function unpack(b){
  var dec=new TextDecoder(),n=T.questions.length,ans=[],o=3+Math.ceil(n/2);
  for(var i=0;i<n;i++){var byte=b[3+(i>>1)],nib=(i&1)?byte&15:byte>>4;ans.push({m:nib>>2,s:nib&3})}
  var f=[];for(var k=0;k<3;k++){var l=b[o++];f.push(dec.decode(b.slice(o,o+l)));o+=l}
  return{version:b[0],date:new Date(EPOCH+((b[1]|(b[2]<<8))*864e5)),ans:ans,name:f[0],tg:f[1],mail:f[2]};
}
var EC={name:'ECDH',namedCurve:'P-256'};
function encrypt(bytes){
  var S=crypto.subtle,pub,eph;
  return S.importKey('raw',unb64u(T.publicKey),EC,false,[]).then(function(k){pub=k;return S.generateKey(EC,true,['deriveKey'])})
  .then(function(kp){eph=kp;return S.deriveKey({name:'ECDH',public:pub},kp.privateKey,{name:'AES-GCM',length:256},false,['encrypt'])})
  .then(function(key){var iv=crypto.getRandomValues(new Uint8Array(12));
    return Promise.all([S.exportKey('raw',eph.publicKey),S.encrypt({name:'AES-GCM',iv:iv},key,bytes)]).then(function(r){
      var e=new Uint8Array(r[0]),c=new Uint8Array(r[1]),out=new Uint8Array(e.length+12+c.length);
      out.set(e,0);out.set(iv,e.length);out.set(c,e.length+12);return b64u(out)})});
}
function decrypt(k,priv){
  var S=crypto.subtle,b=unb64u(k),ep=b.slice(0,65),iv=b.slice(65,77),ct=b.slice(77),pk;
  return S.importKey('pkcs8',unb64u(priv),EC,false,['deriveKey']).then(function(x){pk=x;return S.importKey('raw',ep,EC,false,[])})
  .then(function(e){return S.deriveKey({name:'ECDH',public:e},pk,{name:'AES-GCM',length:256},false,['decrypt'])})
  .then(function(key){return S.decrypt({name:'AES-GCM',iv:iv},key,ct)}).then(function(p){return unpack(new Uint8Array(p))});
}

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
  var top=s?s.indexOf(Math.max.apply(null,s)):L.indexOf(c.split('').find(isHi)||c[0].toUpperCase());
  var letters=c.split('').map(function(ch){var cls=ch==='-'?'no':(isHi(ch)?'hi':'lo');return '<span class="'+cls+'">'+(ch==='-'?'–':ch)+'</span>'}).join('');
  var lead=[],weak=[];c.split('').forEach(function(ch,i){if(isHi(ch))lead.push(L[i]);if(ch==='-')weak.push(L[i])});
  var who=mode==='visitor'?'Профиль склонностей по&nbsp;модели PAEI':'Ваш профиль склонностей';
  var html='<div class="res__top">'+
    (mode==='visitor'?'<p class="res__flag">Это профиль другого человека. Пройдите тест, чтобы узнать свой.</p>':'')+
    '<h1 class="res__who" id="r-h">'+who+'</h1>'+
    '<p class="code" aria-hidden="true"><span class="m code__m">'+letters+'<svg class="mk mk--ring mk--red mk--draw" viewBox="0 0 200 64" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" style="--d:.35s" d="'+RING+'"/></svg></span></p>'+
    '<p class="sr">Профиль '+c.split('').join(' ').replace(/-/g,'прочерк')+'</p>'+
    '<p class="res__name">'+(nm?'По&nbsp;Адизесу такой профиль называется «'+nm+'».':(lead.length?'Ведущие роли: '+lead.map(function(r){return r+'&nbsp;·&nbsp;'+R[r].n}).join(', ')+'.':'Явной ведущей роли нет: все четыре роли рабочие.'))+'</p>'+
    '<p class="res__note">Профиль показывает, к&nbsp;каким ролям вы&nbsp;тянетесь, а&nbsp;не&nbsp;насколько хорошо их&nbsp;исполняете.</p></div>';
  if(s){
    var z1=T.lo/T.max*100,z2=T.hi/T.max*100;
    var bars='<div class="bar bar--head" aria-hidden="true"><span class="bar__n"></span><div class="bar__z"><span style="left:0">Слабая</span><span style="left:'+z1+'%">Рабочая</span><span style="left:'+z2+'%">Ведущая</span></div><span class="bar__st"></span><span class="bar__s"></span></div>';
    s.forEach(function(v,i){
      var w=Math.max(v/T.max*100,1.5);
      bars+='<div class="bar"><p class="bar__n">'+L[i]+' · '+R[L[i]].n+'</p>'+
        '<div class="bar__track"><i class="bar__tick" style="left:'+z1+'%"></i><i class="bar__tick" style="left:'+z2+'%"></i>'+
        '<span class="bar__line" style="width:'+w+'%"><svg viewBox="0 0 100 14" preserveAspectRatio="none" aria-hidden="true" class="mk mk--draw"><path pathLength="1" style="--d:'+(0.5+i*0.15)+'s;--sw:3px" d="M1 8c25-2 60-3 98-1"/></svg></span></div>'+
        '<p class="bar__st'+(v>=T.hi?' is-lead':'')+'">'+status(v)+'</p><p class="bar__s">'+v+'</p></div>';
    });
    html+='<div class="boardp"><div class="bars">'+bars+'</div><p class="legend">Всего 60&nbsp;баллов на&nbsp;четыре роли. Слабая зона&nbsp;— до&nbsp;'+(T.lo-1)+'&nbsp;баллов, ведущая роль&nbsp;— от&nbsp;'+T.hi+'.</p></div>';
  }
  var side='';
  if(mode==='own'){
    side='<h2>Разберём профиль на&nbsp;ваших рабочих кейсах</h2><p>Отправьте ссылку&nbsp;— на&nbsp;15&nbsp;минутах знакомства сверим профиль с&nbsp;тем, что происходит у&nbsp;вас в&nbsp;карьере.</p>'+
      '<a class="btn" id="send" target="_blank" rel="noopener" href="#">Отправить результат в&nbsp;Telegram '+ARROW+'</a>'+
      '<div class="share"><button class="btn btn--line btn--sm" id="share">Поделиться</button><button class="btn btn--line btn--sm" id="story">Картинка для&nbsp;сторис</button><button class="btn btn--line btn--sm" id="copy">Скопировать ссылку</button></div>';
  } else if(mode==='visitor'){
    side='<h2>Узнайте свой профиль</h2><p>20&nbsp;рабочих ситуаций руководителя, 5&nbsp;минут, результат сразу.</p><a class="btn" href="'+rootURL().href+'">Пройти тест '+ARROW+'</a>';
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
    $('send').addEventListener('click',function(){goal('tg_send')});
    $('copy').onclick=function(){goal('copy_link');copy(pub)};
    $('share').onclick=function(){goal('share');
      if(navigator.share)navigator.share({title:T.title,text:'Мой профиль — '+c+(nm?', «'+nm+'»':''),url:pub}).catch(function(){});
      else copy(pub)};
    $('story').onclick=function(){goal('story_image');storyShare(c,s,nm)};
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

/* ---------- картинка для сторис: 1080×1920, сетка как у сторис в Instagram ---------- */
function storyDraw(c,s,nm){
  var W=1080,H=1920,cv=document.createElement('canvas');cv.width=W;cv.height=H;
  var x=cv.getContext('2d'),F='Onest, system-ui, sans-serif',R=T.roles;
  var C={paper:'#FAFAF8',board:'#F3F4F1',ink:'#16181A',ink2:'#3A3E42',muted:'#5E6469',line:'#D8DBD8',line2:'#BFC4C6',red:'#D2302C'};
  function font(px,w,ls){x.font=w+' '+px+'px '+F;if('letterSpacing' in x)x.letterSpacing=(ls||0)+'px'}
  function txt(str,px,w,col,X,Y,al,ls){font(px,w,ls);x.fillStyle=col;x.textAlign=al||'left';x.fillText(str,X,Y);return x.measureText(str).width}
  function mark(d,vb,X,Y,w,h,col,lw){var p=new Path2D();p.addPath(new Path2D(d),new DOMMatrix([w/vb[0],0,0,h/vb[1],X,Y]));x.strokeStyle=col;x.lineWidth=lw;x.lineCap='round';x.lineJoin='round';x.stroke(p)}
  function rrect(X,Y,w,h,r){x.beginPath();if(x.roundRect)x.roundRect(X,Y,w,h,r);else x.rect(X,Y,w,h)}
  var Lm=88,Rr=W-88;
  x.fillStyle=C.paper;x.fillRect(0,0,W,H);
  txt('МОЙ ПРОФИЛЬ СКЛОННОСТЕЙ PAEI',28,600,C.muted,Lm,288,'left',2.2);
  var px=250,base=560,gap=10,cx=Lm;
  c.split('').forEach(function(ch){var hi=isHi(ch),g=ch==='-'?'–':ch;
    cx+=txt(g,px,hi?600:500,ch==='-'?C.line2:(hi?C.ink:C.ink2),cx,base,'left',-6)+gap});
  var tw=cx-gap-Lm;
  mark(RING,[200,64],Lm-40,base-226,tw+104,284,C.red,7);
  var ln=c.split('').filter(isHi).map(function(ch){return R[ch].n});var sub=nm?'По Адизесу — «'+nm+'»':(ln.length?'Ведущие роли: '+ln.join(', '):'Явной ведущей роли нет');
  txt(sub,40,500,C.ink2,Lm,684,'left',-0.8);
  if(s){
    var py=740,rh=130,ph=40+rh*4;
    x.save();x.shadowColor='rgba(22,24,26,.14)';x.shadowBlur=70;x.shadowOffsetY=32;rrect(Lm,py,Rr-Lm,ph,6);x.fillStyle=C.board;x.fill();x.restore();
    rrect(Lm+.5,py+.5,Rr-Lm-1,ph-1,6);x.strokeStyle=C.line;x.lineWidth=1;x.stroke();
    var ix=Lm+52,ir=Rr-52,vx=ix+252,vw=ir-vx;
    s.forEach(function(v,i){var y=py+20+i*rh,lead=v>=T.hi;
      txt(L[i]+' · '+R[L[i]].n.toUpperCase(),24,600,C.muted,ix,y+56,'left',1.9);
      txt(status(v),34,lead?600:500,lead?C.ink:C.ink2,vx,y+56,'left',-0.6);
      txt(String(v),38,600,C.ink,ir,y+58,'right',-0.6);
      var ty=y+80;x.fillStyle=C.line2;[T.lo,T.hi].forEach(function(t){x.fillRect(vx+vw*t/T.max-1,ty-6,2,30)});
      mark('M1 8c25-2 60-3 98-1',[100,14],vx,ty,Math.max(vw*v/T.max,12),14,C.ink,7);
      x.fillStyle=C.line;x.fillRect(ix,y+rh-1,ir-ix,1)});
  }
  var by=1384,bh=120;rrect(Lm,by,Rr-Lm,bh,60);x.fillStyle=C.ink;x.fill();
  font(40,600,-0.4);var lw=x.measureText(T.short).width,ax=W/2-(lw+64)/2;
  txt(T.short,40,600,C.paper,ax,by+bh/2+14,'left',-0.4);
  x.save();x.translate(ax+lw+20,by+bh/2-10);x.strokeStyle=C.paper;x.lineWidth=3;x.lineCap='round';x.lineJoin='round';
  x.beginPath();x.moveTo(2,10);x.lineTo(38,10);x.moveTo(30,3);x.lineTo(40,10);x.lineTo(30,17);x.stroke();x.restore();
  font(26,600,0);var n1='Владимир Семенюк',w1=x.measureText(n1).width;font(26,400,0);var n2=' · '+T.instagram,w2=x.measureText(n2).width,sx=W/2-(w1+w2)/2;
  txt(n1,26,600,C.ink,sx,by+bh+54);txt(n2,26,400,C.muted,sx+w1,by+bh+54);
  return cv;
}
function storyShare(c,s,nm){
  var hint='Добавьте в сторис стикер «Ссылка» с адресом '+T.short+' и отметьте '+T.instagram;
  var fonts=document.fonts?Promise.all(['600 250px Onest','500 250px Onest','400 26px Onest'].map(function(f){return document.fonts.load(f)})):Promise.resolve();
  fonts.then(function(){storyDraw(c,s,nm).toBlob(function(blob){
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
    crypto.subtle.importKey('pkcs8',unb64u(v),EC,false,['deriveKey']).then(function(){store(KEY_STORE,v);ta.value='';upd();toast('Ключ сохранён')},function(){toast('Это не похоже на ключ: проверьте, что скопирован целиком')});
  });
  $('key-del').addEventListener('click',function(){store(KEY_STORE,null);upd();toast('Ключ удалён из этого браузера')});
  upd();
}

window.__tests={storyDraw:storyDraw,encrypt:encrypt,decrypt:decrypt,pack:pack,unpack:unpack,codeOf:codeOf,slugOf:slugOf,scoresOf:scoresOf};
if(page==='result')window.addEventListener('hashchange',function(){location.reload()});
if(page==='test')testPage();else if(page==='result')resultPage();else if(page==='key')keyPage();
})();
