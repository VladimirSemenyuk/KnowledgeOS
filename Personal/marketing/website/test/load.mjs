// Общие модули сайта для тестов: те же файлы, что подключает страница.
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
export const SITE = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "site");
const ASSETS = path.join(SITE, "tests", "assets");
export const S = require(path.join(ASSETS, "scoring.js"));
export const CR = require(path.join(ASSETS, "crypto.js"));
export const loadTest = (id) => S.parseData(fs.readFileSync(path.join(SITE, "tests", id, "data.js"), "utf8"));
export const T = loadTest("paei");
