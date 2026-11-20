// Тесты crypto.js: закрытая часть ссылки на результат (имя, контакт, ответы) переживает упаковку и шифрование.
// Запуск из папки website/: node --test test/
import test from "node:test";
import assert from "node:assert/strict";
import { webcrypto } from "node:crypto";
import { T, CR } from "./load.mjs";

const answers = (n, f = (i) => ({ m: i % 4, s: (i + 1) % 4 })) => Array.from({ length: n }, (_, i) => f(i));
const person = { name: "Анна Петрова", tg: "anna_p", mail: "anna@example.com" };

async function keyPair() {
  const kp = await webcrypto.subtle.generateKey({ name: "ECDH", namedCurve: "P-256" }, true, ["deriveKey"]);
  return {
    pub: CR.b64u(await webcrypto.subtle.exportKey("raw", kp.publicKey)),
    priv: CR.b64u(await webcrypto.subtle.exportKey("pkcs8", kp.privateKey)),
  };
}

test("base64url туда и обратно, без +, / и =", () => {
  for (let len = 0; len < 70; len++) {
    const b = Uint8Array.from({ length: len }, (_, i) => (i * 37 + len * 11) & 255);
    const s = CR.b64u(b);
    assert.doesNotMatch(s, /[+/=]/);
    assert.deepEqual(CR.unb64u(s), b);
  }
});

test("упаковка: все сочетания главного и второго выбора восстанавливаются", () => {
  const all = [];
  for (let m = 0; m < 4; m++) for (let s = 0; s < 4; s++) if (m !== s) all.push({ m, s });
  const ans = answers(T.questions.length, (i) => all[i % all.length]);
  const now = Date.UTC(2026, 10, 21, 15, 30);
  const d = CR.unpack(T, CR.pack(T, { ans, ...person }, now));
  assert.deepEqual(d.ans, ans);
  assert.equal(d.version, T.version);
  assert.equal(d.date.toISOString(), "2026-11-21T00:00:00.000Z");
  assert.deepEqual([d.name, d.tg, d.mail], [person.name, person.tg, person.mail]);
});

test("упаковка: нечётное число вопросов и пустые контакты", () => {
  const T21 = { ...T, questions: answers(21) };
  const ans = answers(21);
  const d = CR.unpack(T21, CR.pack(T21, { ans, name: "Ян" }));
  assert.deepEqual(d.ans, ans);
  assert.deepEqual([d.name, d.tg, d.mail], ["Ян", "", ""]);
});

test("упаковка: длинное имя обрезается до 255 байт, остальные поля не съезжают", () => {
  const d = CR.unpack(T, CR.pack(T, { ans: answers(T.questions.length), name: "я".repeat(300), tg: "anna_p", mail: "a@b.c" }));
  assert.ok(new TextEncoder().encode(d.name).length <= 255);
  assert.ok(d.name.startsWith("я".repeat(127)));
  assert.deepEqual([d.tg, d.mail], ["anna_p", "a@b.c"]);
});

test("дата: годы вперёд не переполняют два байта", () => {
  const now = Date.UTC(2040, 5, 1);
  const d = CR.unpack(T, CR.pack(T, { ans: answers(T.questions.length) }, now));
  assert.equal(d.date.toISOString(), "2040-06-01T00:00:00.000Z");
});

test("шифрование и расшифровка своей парой ключей", async () => {
  const { pub, priv } = await keyPair();
  const TK = { ...T, publicKey: pub };
  const ans = answers(T.questions.length);
  const k = await CR.encrypt(TK, CR.pack(TK, { ans, ...person }));
  assert.match(k, /^[A-Za-z0-9_-]+$/);
  const d = await CR.decrypt(TK, k, priv);
  assert.deepEqual(d.ans, ans);
  assert.deepEqual([d.name, d.tg, d.mail], [person.name, person.tg, person.mail]);
});

test("каждое шифрование своё: одинаковые данные дают разные ссылки", async () => {
  const { pub } = await keyPair();
  const TK = { ...T, publicKey: pub };
  const bytes = CR.pack(TK, { ans: answers(T.questions.length), ...person });
  assert.notEqual(await CR.encrypt(TK, bytes), await CR.encrypt(TK, bytes));
});

test("чужой ключ и испорченная ссылка не расшифровываются", async () => {
  const a = await keyPair(), b = await keyPair();
  const TK = { ...T, publicKey: a.pub };
  const k = await CR.encrypt(TK, CR.pack(TK, { ans: answers(T.questions.length), ...person }));
  await assert.rejects(CR.decrypt(TK, k, b.priv));
  const broken = k.slice(0, -4) + (k.slice(-4) === "AAAA" ? "BBBB" : "AAAA");
  await assert.rejects(CR.decrypt(TK, broken, a.priv));
});

test("ссылка с недопустимыми символами — отклонённый Promise, а не исключение", async () => {
  const { priv } = await keyPair();
  const p = CR.decrypt(T, "обрезано при копировании!", priv);
  assert.ok(p instanceof Promise);
  await assert.rejects(p);
});

test("открытый ключ из data.js рабочий: им можно зашифровать", async () => {
  const k = await CR.encrypt(T, CR.pack(T, { ans: answers(T.questions.length), ...person }));
  assert.ok(k.length > 100);
});

test("закрытый ключ проверяется при сохранении на странице ключа", async () => {
  const { priv } = await keyPair();
  await CR.importPrivate(priv);
  await assert.rejects(CR.importPrivate("не ключ"));
});
