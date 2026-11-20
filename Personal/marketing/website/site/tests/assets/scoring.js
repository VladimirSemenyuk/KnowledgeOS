/* Правило подсчёта тестов semenyuk.pro/tests/: ответы → баллы → уровень роли → код профиля → адрес страницы результата.
   Записано только здесь. Им пользуются страница (tests.js, profile.js — через window.TestScoring)
   и сборка tools/tests-build.mjs (через require) — поэтому браузер не может выдать код,
   для которого сборка не сделала страницу. */
(function(root){
'use strict';

/* Балл за ответ: главный выбор и второй выбор в одной ситуации. */
var MAIN=2,SECOND=1;

/* ans — [{m: индекс буквы главного выбора, s: индекс второго}]; пропуск — null или -1. */
function scoresOf(ans){var s=[0,0,0,0];ans.forEach(function(a){if(!a)return;if(a.m>=0)s[a.m]+=MAIN;if(a.s>=0)s[a.s]+=SECOND});return s}

/* Уровень роли по баллам: ведущая (≥ hi), рабочая (≥ lo), слабая. */
function levelOf(T,v){return v>=T.hi?'lead':(v>=T.lo?'mid':'weak')}

/* Код: ведущая роль — большая буква, рабочая — маленькая, слабая — прочерк. */
function codeOf(T,s){var L=T.letters;return s.map(function(v,i){var l=levelOf(T,v);return l==='lead'?L[i]:(l==='mid'?L[i].toLowerCase():'-')}).join('')}

/* Уровень роли по символу кода — обратное к codeOf. */
function levelOfChar(ch){return ch==='-'?'weak':(ch===ch.toUpperCase()?'lead':'mid')}

/* Код в имя папки: большая буква удваивается, маленькая остаётся, прочерк — 0. «Pa-i» → «ppa0i». */
function slugOf(c){return c.split('').map(function(ch){var l=levelOfChar(ch);return l==='weak'?'0':(l==='lead'?ch.toLowerCase()+ch.toLowerCase():ch)}).join('')}

/* Баллы из ссылки правдоподобны: четыре числа в пределах шкалы, сумма — полный тест. */
function validScores(T,s){return s.length===4&&s.every(function(v){return v>=0&&v<=T.max})&&s.reduce(function(a,b){return a+b},0)===T.questions.length*(MAIN+SECOND)}

/* Все коды, которые можно получить ответами. m[i] и s[i] — сколько раз буква i была главным и вторым выбором.
   Главный и второй выбор в одной ситуации — разные буквы, такие ответы существуют, пока m[i]+s[i] ≤ числа ситуаций. */
function reachable(T){
  var n=T.questions.length,C=[],codes={};
  (function comps(total,k,acc){
    if(k===1){C.push(acc.concat(total));return}
    for(var i=0;i<=total;i++)comps(total-i,k-1,acc.concat(i));
  })(n,4,[]);
  C.forEach(function(m){C.forEach(function(s){
    for(var i=0;i<4;i++)if(m[i]+s[i]>n)return;
    codes[codeOf(T,[0,1,2,3].map(function(i){return MAIN*m[i]+SECOND*s[i]}))]=1;
  })});
  return Object.keys(codes).sort();
}

/* Текст data.js → объект теста. Формат: JSON после строки «window.TEST=». */
function parseData(src){
  var at=src.indexOf('\nwindow.TEST=');
  if(at<0)throw new Error('в data.js нет строки «window.TEST=»');
  return JSON.parse(src.slice(at+13).trim().replace(/;$/,''));
}

var api={MAIN:MAIN,SECOND:SECOND,scoresOf:scoresOf,levelOf:levelOf,levelOfChar:levelOfChar,codeOf:codeOf,slugOf:slugOf,
  validScores:validScores,reachable:reachable,parseData:parseData};
if(typeof module==='object'&&module.exports)module.exports=api;else root.TestScoring=api;
})(this);
