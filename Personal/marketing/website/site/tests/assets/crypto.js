/* Закрытая часть ссылки на результат (k=…): имя, контакт, ответы и дата.
   pack — в байты, encrypt — открытым ключом Владимира из data.js (ECDH P-256 + AES-GCM), base64url.
   decrypt — закрытым ключом (страница /tests/key/ хранит его только в браузере Владимира), unpack — обратно.

   Формат байтов: [версия теста][дни с 2026-01-01, 2 байта][ответы: по 4 бита на вопрос — главный<<2 | второй]
   затем имя, Telegram, email: по байту длины (до 255) и UTF-8.
   Формат зашифрованного: [одноразовый открытый ключ, 65 байт][iv, 12 байт][шифротекст AES-GCM].

   Записано только здесь. В браузере — window.TestCrypto (tests.js), в Node — module.exports (тесты). */
(function(root){
'use strict';
var C=typeof crypto!=='undefined'&&crypto.subtle?crypto:require('node:crypto').webcrypto;
var EC={name:'ECDH',namedCurve:'P-256'};
var EPOCH=Date.UTC(2026,0,1),DAY=864e5;

function b64u(buf){var b=new Uint8Array(buf),s='';for(var i=0;i<b.length;i++)s+=String.fromCharCode(b[i]);return btoa(s).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'')}
function unb64u(str){str=str.replace(/-/g,'+').replace(/_/g,'/');while(str.length%4)str+='=';var s=atob(str),b=new Uint8Array(s.length);for(var i=0;i<s.length;i++)b[i]=s.charCodeAt(i);return b}

/* UTF-8 не длиннее max байт, обрезка по границе символа: половина буквы при расшифровке дала бы «�». */
function utf8(x,max){var b=new TextEncoder().encode(x||'');if(b.length<=max)return b;var e=max;while(e>0&&(b[e]&0xC0)===0x80)e--;return b.slice(0,e)}

/* p — {ans:[{m,s}], name, tg, mail}; now — для тестов, по умолчанию текущее время. */
function pack(T,p,now){
  var parts=[p.name,p.tg,p.mail].map(function(x){return utf8(x,255)});
  var n=Math.ceil(p.ans.length/2),head=new Uint8Array(3+n),days=Math.floor(((now==null?Date.now():now)-EPOCH)/DAY);
  head[0]=T.version;head[1]=days&255;head[2]=(days>>8)&255;
  p.ans.forEach(function(a,i){var nib=(a.m<<2)|a.s;head[3+(i>>1)]|=(i&1)?nib:(nib<<4)});
  var len=head.length+parts.reduce(function(a,b){return a+1+b.length},0),out=new Uint8Array(len),o=head.length;
  out.set(head,0);parts.forEach(function(b){out[o++]=b.length;out.set(b,o);o+=b.length});
  return out;
}
function unpack(T,b){
  var dec=new TextDecoder(),n=T.questions.length,ans=[],o=3+Math.ceil(n/2);
  for(var i=0;i<n;i++){var byte=b[3+(i>>1)],nib=(i&1)?byte&15:byte>>4;ans.push({m:nib>>2,s:nib&3})}
  var f=[];for(var k=0;k<3;k++){var l=b[o++];f.push(dec.decode(b.slice(o,o+l)));o+=l}
  return{version:b[0],date:new Date(EPOCH+((b[1]|(b[2]<<8))*DAY)),ans:ans,name:f[0],tg:f[1],mail:f[2]};
}
function encrypt(T,bytes){
  var S=C.subtle,pub,eph;
  return S.importKey('raw',unb64u(T.publicKey),EC,false,[]).then(function(k){pub=k;return S.generateKey(EC,true,['deriveKey'])})
  .then(function(kp){eph=kp;return S.deriveKey({name:'ECDH',public:pub},kp.privateKey,{name:'AES-GCM',length:256},false,['encrypt'])})
  .then(function(key){var iv=C.getRandomValues(new Uint8Array(12));
    return Promise.all([S.exportKey('raw',eph.publicKey),S.encrypt({name:'AES-GCM',iv:iv},key,bytes)]).then(function(r){
      var e=new Uint8Array(r[0]),c=new Uint8Array(r[1]),out=new Uint8Array(e.length+12+c.length);
      out.set(e,0);out.set(iv,e.length);out.set(c,e.length+12);return b64u(out)})});
}
/* Ошибки — только через отклонённый Promise: испорченная строка не должна ронять скрипт страницы. */
function importPrivate(priv){return Promise.resolve().then(function(){return C.subtle.importKey('pkcs8',unb64u(priv),EC,false,['deriveKey'])})}
function decrypt(T,k,priv){
  var S=C.subtle,ep,iv,ct,pk;
  return importPrivate(priv).then(function(x){pk=x;var b=unb64u(k);ep=b.slice(0,65);iv=b.slice(65,77);ct=b.slice(77);return S.importKey('raw',ep,EC,false,[])})
  .then(function(e){return S.deriveKey({name:'ECDH',public:e},pk,{name:'AES-GCM',length:256},false,['decrypt'])})
  .then(function(key){return S.decrypt({name:'AES-GCM',iv:iv},key,ct)}).then(function(p){return unpack(T,new Uint8Array(p))});
}

var api={EPOCH:EPOCH,b64u:b64u,unb64u:unb64u,pack:pack,unpack:unpack,encrypt:encrypt,decrypt:decrypt,importPrivate:importPrivate};
if(typeof module==='object'&&module.exports)module.exports=api;else root.TestCrypto=api;
})(this);
