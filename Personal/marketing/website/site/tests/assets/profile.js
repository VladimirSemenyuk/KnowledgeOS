/* Как показывается профиль теста: тексты, начертание кода, красная обводка и картинки.
   Записано только здесь. Пользуются страница результата и кнопка «Картинка для сторис» (tests.js)
   и сборка tools/tests-build.mjs: описание ссылки — через require, превью og.jpg — тем же drawOg в Chrome.
   Цвета берутся из переменных tests.css, поэтому для картинок tests.css должен быть подключён.
   Подсчёт — в scoring.js. В браузере — window.TestProfile, в Node — module.exports (только тексты). */
(function(root){
'use strict';
var S=typeof module==='object'&&module.exports?require('./scoring.js'):root.TestScoring;

var AUTHOR='Владимир Семенюк';
var FONT='Onest, system-ui, sans-serif';
/* Красная обводка от руки (viewBox 200×64) и подчёркивание шкалы (viewBox 100×14). */
var RING='M30 12C70 3 150 2 184 14c18 7 16 28-4 38-38 15-122 14-160 3C2 49 2 31 18 21c22-13 76-17 112-13';
var STROKE='M1 8c25-2 60-3 98-1';
var LEVEL={lead:'ведущая',mid:'рабочая',weak:'слабая'};

/* ---------- тексты ---------- */
function nb(s){return s.replace(/(\d) /g,'$1 ')}
function label(T){return 'Профиль склонностей '+T.letters}
function leadLetters(c){return c.split('').filter(function(ch){return S.levelOfChar(ch)==='lead'})}
function weakIndexes(c){var r=[];c.split('').forEach(function(ch,i){if(ch==='-')r.push(i)});return r}
function leadNames(T,c){return leadLetters(c).map(function(ch){return T.roles[ch].n})}
/* Символы кода для показа: прочерк — длинное тире, уровень задаёт начертание и цвет. */
function glyphs(c){return c.split('').map(function(ch){return{g:ch==='-'?'–':ch,level:S.levelOfChar(ch)}})}
/* Одна строка под кодом: превью ссылки и сторис. */
function caption(T,c){var nm=T.names[c],ln=leadNames(T,c);
  return nm?'По Адизесу — «'+nm+'»':(ln.length?'Ведущие роли: '+ln.join(', '):'Явной ведущей роли нет')}
/* Строка под кодом на странице результата: ведущие роли с буквами. */
function resultLine(T,c){var nm=T.names[c],ld=leadLetters(c);
  return nm?'По\u00a0Адизесу такой профиль называется «'+nm+'».':(ld.length?'Ведущие роли: '+ld.map(function(r){return r+'\u00a0·\u00a0'+T.roles[r].n}).join(', ')+'.':'Явной ведущей роли нет: все четыре роли рабочие.')}
/* Описание ссылки на страницу результата (meta description, og:description). */
function describe(T,c){var nm=T.names[c],lead=leadNames(T,c).join(', ');
  return (nm?'По Адизесу — «'+nm+'». Ведущие роли: '+lead+'.':(lead?'Ведущие роли: '+lead+'.':'Явной ведущей роли нет: все четыре роли рабочие.'))+
    ' Пройдите тест: '+T.pitch+', '+T.duration+'.'}
function ogTitle(T,c){var nm=T.names[c];return 'Профиль склонностей '+c+(nm?' — «'+nm+'»':'')}

/* ---------- рисование на canvas ---------- */
function palette(){
  var cs=getComputedStyle(document.documentElement),C={};
  ['board','paper','ink','ink-2','muted','line','line-2','red'].forEach(function(k){
    var v=cs.getPropertyValue('--'+k).trim();if(!v)throw new Error('нет цвета --'+k+': не подключён tests.css');C[k.replace('-','')]=v});
  return C;
}
/* Образец текста обязателен: без него браузер грузит только латинскую часть шрифта, и кириллица на canvas
   молча рисуется системным шрифтом. */
var FONT_SAMPLE='АаБбЯяЁё AaZz 0123456789 «»·–—';
function fontsReady(){
  if(!document.fonts)return Promise.resolve();
  return Promise.all(['400','500','600'].map(function(w){return document.fonts.load(w+' 40px Onest',FONT_SAMPLE)}));
}
function pen(x){
  function font(px,w,ls){x.font=w+' '+px+'px '+FONT;if('letterSpacing' in x)x.letterSpacing=(ls||0)+'px'}
  return{
    font:font,
    txt:function(str,px,w,col,X,Y,al,ls){font(px,w,ls);x.fillStyle=col;x.textAlign=al||'left';x.fillText(str,X,Y);return x.measureText(str).width},
    mark:function(d,vb,X,Y,w,h,col,lw){var p=new Path2D();p.addPath(new Path2D(d),new DOMMatrix([w/vb[0],0,0,h/vb[1],X,Y]));
      x.strokeStyle=col;x.lineWidth=lw;x.lineCap='round';x.lineJoin='round';x.stroke(p)},
    rrect:function(X,Y,w,h,r){x.beginPath();if(x.roundRect)x.roundRect(X,Y,w,h,r);else x.rect(X,Y,w,h)},
    arrow:function(X,Y,k,col,lw){x.save();x.translate(X,Y);x.scale(k,k);x.strokeStyle=col;x.lineWidth=lw/k;x.lineCap='round';x.lineJoin='round';
      x.beginPath();x.moveTo(2,10);x.lineTo(38,10);x.moveTo(30,3);x.lineTo(40,10);x.lineTo(30,17);x.stroke();x.restore()},
    wrap:function(str,px,w,ls,max){font(px,w,ls);var out=[],line='';str.split(' ').forEach(function(word){
      var t=line?line+' '+word:word;if(line&&x.measureText(t).width>max){out.push(line);line=word}else line=t});if(line)out.push(line);return out}
  };
}
/* Код профиля крупно: ведущая — жирная, рабочая — обычная, слабая — серое тире. Возвращает ширину. */
function drawCode(p,C,c,X,base,px,gap,ls){
  var cx=X;glyphs(c).forEach(function(g){
    cx+=p.txt(g.g,px,g.level==='lead'?600:500,g.level==='weak'?C.line2:(g.level==='lead'?C.ink:C.ink2),cx,base,'left',ls)+gap});
  return cx-gap-X;
}
/* Подпись внизу: имя и ник Instagram, по центру или от левого края. */
function drawByline(p,x,C,T,X,Y,px,center){
  p.font(px,600,0);var n1=AUTHOR,w1=x.measureText(n1).width;p.font(px,400,0);var n2=' · '+T.instagram,w2=x.measureText(n2).width;
  var sx=center?X-(w1+w2)/2:X;p.txt(n1,px,600,C.ink,sx,Y);p.txt(n2,px,400,C.muted,sx+w1,Y);
}
function canvas(W,H){var cv=document.createElement('canvas');cv.width=W;cv.height=H;return cv}

/* Превью ссылки 1200×630: профиль c или, без c, страница теста. */
function drawOg(T,c){
  var W=1200,H=630,cv=canvas(W,H),x=cv.getContext('2d'),p=pen(x),C=palette(),Lm=72,Rr=W-72;
  x.fillStyle=C.board;x.fillRect(0,0,W,H);
  x.fillStyle=C.ink;x.fillRect(Lm,64,Rr-Lm,3);
  p.txt(label(T).toUpperCase(),22,600,C.ink,Lm,107,'left',1.76);
  p.txt(T.short,22,400,C.muted,Rr,107,'right');
  if(c){
    var base=345,tw=drawCode(p,C,c,Lm,base,200,6,-6),bw=tw+60;
    p.mark(RING,[200,64],Lm-30-bw*.05,base-189,bw*1.1,245,C.red,6);
    p.txt(caption(T,c),34,500,C.ink2,Lm,427,'left',-0.68);
  }else{
    var lines=p.wrap(T.headline,76,600,-3.42,900),y0=307-(lines.length-1)*79/2;
    lines.forEach(function(l,i){p.txt(l,76,600,C.ink,Lm,y0+i*79,'left',-3.42)});
    p.txt(T.pitch+' · '+T.duration,34,500,C.ink2,Lm,y0+(lines.length-1)*79+70,'left',-0.68);
  }
  drawByline(p,x,C,T,Lm,568,22,false);
  p.arrow(Rr-36,552,36/44,C.ink,3);
  p.txt('Пройти тест',22,600,C.ink,Rr-36-12,568,'right');
  return cv;
}

/* Картинка для сторис 1080×1920, сетка как у сторис в Instagram. s — баллы, без них только код. */
function drawStory(T,c,s){
  var W=1080,H=1920,cv=canvas(W,H),x=cv.getContext('2d'),p=pen(x),C=palette(),L=T.letters,R=T.roles,Lm=88,Rr=W-88;
  x.fillStyle=C.board;x.fillRect(0,0,W,H);
  p.txt(('Мой '+label(T).toLowerCase()).toUpperCase(),28,600,C.muted,Lm,288,'left',2.2);
  var base=560,tw=drawCode(p,C,c,Lm,base,250,10,-6);
  p.mark(RING,[200,64],Lm-40,base-226,tw+104,284,C.red,7);
  p.txt(caption(T,c),40,500,C.ink2,Lm,684,'left',-0.8);
  if(s){
    var py=730,rh=130,ph=84+rh*4,top=Math.max.apply(null,s),dm=Math.max(30,top);
    x.save();x.shadowColor='rgba(22,24,26,.14)';x.shadowBlur=70;x.shadowOffsetY=32;p.rrect(Lm,py,Rr-Lm,ph,6);x.fillStyle='#FFFFFF';x.fill();x.restore();
    p.rrect(Lm+.5,py+.5,Rr-Lm-1,ph-1,6);x.strokeStyle=C.line;x.lineWidth=1;x.stroke();
    var ix=Lm+52,ir=Rr-52,vx=ix+252,vw=ir-vx,x1=vx+vw*T.lo/dm,x2=vx+vw*T.hi/dm;
    s.forEach(function(v,i){var y=py+64+i*rh,st=S.levelOf(T,v),ty=y+74,th=30;
      p.txt(L[i]+' · '+R[L[i]].n.toUpperCase(),24,st==='lead'?700:600,st==='lead'?C.ink:C.muted,ix,y+56,'left',1.9);
      p.txt(LEVEL[st],32,st==='lead'?700:500,st==='lead'?C.ink:(st==='weak'?C.muted:C.ink2),vx,y+56,'left',-0.6);
      var sw=p.txt(String(v),52,600,st==='weak'?C.muted:C.ink,ir,y+62,'right',-1.5);
      if(v===top&&st==='lead')p.mark(RING,[200,64],ir-sw-26,y+4,sw+52,76,C.red,4);
      // зоны: штриховка слабой, тон ведущей
      x.save();x.beginPath();x.rect(vx,ty,x1-vx,th);x.clip();x.strokeStyle='rgba(22,24,26,.14)';x.lineWidth=2;
      for(var hx=vx-th;hx<x1;hx+=9){x.beginPath();x.moveTo(hx,ty+th);x.lineTo(hx+th,ty);x.stroke()}x.restore();
      x.fillStyle='rgba(22,24,26,.04)';x.fillRect(x2,ty,ir-x2,th);
      x.save();x.strokeStyle=C.line2;x.lineWidth=2;x.setLineDash([6,5]);[x1,x2].forEach(function(t){x.beginPath();x.moveTo(t,ty-8);x.lineTo(t,ty+th+8);x.stroke()});x.restore();
      p.mark(STROKE,[100,14],vx,ty+12,Math.max(vw*v/dm,14),14,st==='weak'?C.ink2:C.ink,st==='lead'?11:(st==='weak'?6:8));
      x.fillStyle=C.line;x.fillRect(ix,y+rh-1,ir-ix,1)});
    ['weak','mid','lead'].forEach(function(l,i){p.txt(LEVEL[l].toUpperCase(),20,600,C.muted,[vx,x1+8,x2+8][i],py+56,'left',1.6)});
    x.fillStyle=C.ink;x.fillRect(ix,py+74,ir-ix,2);
  }
  var by=1384,bh=120;p.rrect(Lm,by,Rr-Lm,bh,60);x.fillStyle=C.ink;x.fill();
  p.font(40,600,-0.4);var lw=x.measureText(T.short).width,ax=W/2-(lw+64)/2;
  p.txt(T.short,40,600,C.paper,ax,by+bh/2+14,'left',-0.4);
  p.arrow(ax+lw+20,by+bh/2-10,1,C.paper,3);
  drawByline(p,x,C,T,W/2,by+bh+54,26,true);
  return cv;
}

var api={AUTHOR:AUTHOR,RING:RING,STROKE:STROKE,LEVEL:LEVEL,nb:nb,label:label,leadLetters:leadLetters,weakIndexes:weakIndexes,leadNames:leadNames,
  glyphs:glyphs,caption:caption,resultLine:resultLine,describe:describe,ogTitle:ogTitle,
  fontsReady:fontsReady,drawOg:drawOg,drawStory:drawStory};
if(typeof module==='object'&&module.exports)module.exports=api;else root.TestProfile=api;
})(this);
