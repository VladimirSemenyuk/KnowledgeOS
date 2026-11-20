// Тесты scoring.js: любой результат теста ведёт на существующую страницу профиля.
// Запуск из папки website/: node --test 'test/*.test.mjs'
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { S, T, SITE } from "./load.mjs";

const REACHABLE = S.reachable(T); // перебор долгий: считаем один раз

// Детерминированный генератор случайных ответов, чтобы падение воспроизводилось.
function rng(seed) {
  return () => ((seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648);
}
function randomAnswers(r, n) {
  return Array.from({ length: n }, () => {
    const m = Math.floor(r() * 4);
    let s = Math.floor(r() * 3);
    if (s >= m) s++;
    return { m, s };
  });
}

test("баллы: главный выбор 2, второй 1, пропуски не считаются", () => {
  assert.deepEqual(S.scoresOf([{ m: 0, s: 1 }, { m: 3, s: 0 }, null, { m: 2, s: -1 }]), [3, 1, 2, 2]);
});

test("пороги: ведущая от hi, рабочая от lo", () => {
  assert.equal(S.levelOf(T, T.hi), "lead");
  assert.equal(S.levelOf(T, T.hi - 1), "mid");
  assert.equal(S.levelOf(T, T.lo), "mid");
  assert.equal(S.levelOf(T, T.lo - 1), "weak");
  assert.equal(S.codeOf(T, [T.hi, T.hi - 1, T.lo, T.lo - 1]), "Pae-");
});

test("код и уровень по символу согласованы", () => {
  for (const s of [[40, 20, 0, 0], [13, 15, 14, 18], [7, 8, 16, 29]]) {
    const c = S.codeOf(T, s);
    assert.deepEqual(c.split("").map(S.levelOfChar), s.map((v) => S.levelOf(T, v)));
  }
});

test("любые ответы дают допустимые баллы и достижимый код", () => {
  const reachable = new Set(REACHABLE);
  const r = rng(42);
  for (let i = 0; i < 5000; i++) {
    const s = S.scoresOf(randomAnswers(r, T.questions.length));
    assert.ok(S.validScores(T, s), `баллы ${s}`);
    assert.ok(reachable.has(S.codeOf(T, s)), `код ${S.codeOf(T, s)} для ${s} не среди собранных страниц`);
  }
});

test("крайние ответы: всё в одну роль, поровну, по кругу", () => {
  const reachable = new Set(REACHABLE);
  const n = T.questions.length;
  const cases = [
    Array.from({ length: n }, () => ({ m: 0, s: 1 })),
    Array.from({ length: n }, () => ({ m: 3, s: 2 })),
    Array.from({ length: n }, (_, i) => ({ m: i % 4, s: (i + 1) % 4 })),
    Array.from({ length: n }, (_, i) => ({ m: i % 2, s: 2 + (i % 2) })),
  ];
  for (const ans of cases) assert.ok(reachable.has(S.codeOf(T, S.scoresOf(ans))));
});

test("каждый достижимый код получается настоящими ответами", () => {
  // обратная проверка: reachable не перечисляет лишних профилей.
  // Для каждого кода берём раскладку «сколько раз буква была главным / вторым выбором»
  // и строим из неё ответы, где в каждом вопросе главный и второй выбор разные.
  const n = T.questions.length;
  const comps = [];
  (function walk(left, k, acc) {
    if (k === 1) { comps.push([...acc, left]); return; }
    for (let i = 0; i <= left; i++) walk(left - i, k - 1, [...acc, i]);
  })(n, 4, []);
  const witness = new Map();
  for (const m of comps) for (const s of comps) {
    if (m.some((v, i) => v + s[i] > n)) continue; // правило reachable: его и проверяем построением ответов
    const c = S.codeOf(T, m.map((v, i) => S.MAIN * v + S.SECOND * s[i]));
    if (!witness.has(c)) witness.set(c, [m, s]);
  }
  // ответы по раскладке: перебор с отсечением, когда букве не хватает вопросов
  function build(m, s) {
    const ans = [];
    (function go(m, s, q) {
      if (q === 0) return true;
      if ([0, 1, 2, 3].some((k) => m[k] + s[k] > q)) return false;
      for (let i = 0; i < 4; i++) if (m[i]) for (let j = 0; j < 4; j++) if (j !== i && s[j]) {
        m[i]--; s[j]--; ans.push({ m: i, s: j });
        if (go(m, s, q - 1)) return true;
        m[i]++; s[j]++; ans.pop();
      }
      return false;
    })([...m], [...s], n);
    return ans.length === n ? ans : null;
  }
  for (const c of REACHABLE) {
    const ans = build(...witness.get(c));
    assert.ok(ans, `для кода ${c} нет настоящих ответов`);
    assert.ok(ans.every((a) => a.m !== a.s));
    assert.equal(S.codeOf(T, S.scoresOf(ans)), c);
  }
});

test("имена папок: разные коды — разные папки, без лишних символов", () => {
  const codes = REACHABLE;
  const slugs = codes.map(S.slugOf);
  assert.equal(new Set(slugs).size, codes.length);
  for (const s of slugs) assert.match(s, /^[a-z0]+$/);
  assert.equal(S.slugOf("Pa-i"), "ppa0i");
});

test("собранные страницы совпадают с достижимыми кодами", () => {
  const dir = path.join(SITE, "tests", "paei", "r");
  const built = fs.readdirSync(dir).filter((d) => fs.statSync(path.join(dir, d)).isDirectory()).sort();
  assert.deepEqual(built, REACHABLE.map(S.slugOf).sort(),
    "страницы устарели: пересоберите node tools/tests-build.mjs paei");
});

test("баллы из ссылки: проверка отсекает подделку и обрезку", () => {
  const n3 = T.questions.length * 3;
  assert.ok(S.validScores(T, [20, 20, 10, n3 - 50]));
  assert.ok(!S.validScores(T, [20, 20, 10]));
  assert.ok(!S.validScores(T, [20, 20, 10, n3 - 49]));
  assert.ok(!S.validScores(T, [-1, 21, 10, n3 - 30]));
  assert.ok(!S.validScores(T, [T.max + 1, 0, 0, n3 - T.max - 1]));
});

test("data.js читается, пороги согласованы", () => {
  assert.equal(T.letters.length, 4);
  assert.ok(T.lo < T.hi && T.hi <= T.max);
  assert.equal(T.max, T.questions.length * S.MAIN);
  for (const q of T.questions) assert.equal(q.o.length, 4);
  assert.throws(() => S.parseData("var x = 1;"));
});
