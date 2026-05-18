import fs from "node:fs";
import path from "node:path";
import input from "input";
import { TelegramClient } from "telegram";
import { StringSession } from "telegram/sessions/index.js";

function findRepoRoot(startDir) {
  let current = startDir;
  while (true) {
    if (
      fs.existsSync(path.join(current, "AGENTS.md")) &&
      fs.existsSync(path.join(current, "Posts"))
    ) {
      return current;
    }
    const parent = path.dirname(current);
    if (parent === current) {
      throw new Error("Cannot find vault root with AGENTS.md and Posts/.");
    }
    current = parent;
  }
}

const repoRoot = findRepoRoot(process.cwd());
const skillRoot = path.dirname(path.dirname(new URL(import.meta.url).pathname));

function credentialRoots() {
  return [
    process.env.TELEGRAM_WEEKLY_CREDENTIAL_ROOT,
    path.join(skillRoot, ".private"),
    repoRoot,
    "/Users/vladimir/Obsidian/KnowledgeOS"
  ].filter(Boolean);
}

function findCredentialPaths() {
  const candidates = credentialRoots().map((root) => ({
    root,
    envPath: path.join(root, ".telegram-weekly.env"),
    sessionPath: path.join(root, ".telegram-weekly.session.txt")
  }));
  const fullMatch = candidates.find(
    (candidate) => fs.existsSync(candidate.envPath) && fs.existsSync(candidate.sessionPath)
  );
  if (fullMatch) return fullMatch;
  return candidates.find((candidate) => fs.existsSync(candidate.envPath)) || candidates[0];
}

const credentials = findCredentialPaths();
const envPath = credentials.envPath;
const sessionPath = credentials.sessionPath;

function loadEnvFile(filePath) {
  if (!fs.existsSync(filePath)) return;
  const lines = fs.readFileSync(filePath, "utf8").split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const match = trimmed.match(/^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/);
    if (!match) continue;
    const [, key, rawValue] = match;
    const value = rawValue.replace(/^['"]|['"]$/g, "");
    if (!process.env[key]) process.env[key] = value;
  }
}

function requiredEnv(name) {
  const value = process.env[name];
  if (!value) {
    const checked = credentialRoots()
      .map((root) => path.join(root, ".telegram-weekly.env"))
      .join(", ");
    throw new Error(`Missing ${name}. Add it to ${envPath}. Checked: ${checked}.`);
  }
  return value;
}

loadEnvFile(envPath);

const apiId = Number(requiredEnv("TELEGRAM_API_ID"));
const apiHash = requiredEnv("TELEGRAM_API_HASH");
const phoneNumber = process.env.TELEGRAM_PHONE || "";

if (!Number.isInteger(apiId)) {
  throw new Error("TELEGRAM_API_ID must be an integer.");
}

const existingSession = fs.existsSync(sessionPath)
  ? fs.readFileSync(sessionPath, "utf8").trim()
  : "";

const client = new TelegramClient(new StringSession(existingSession), apiId, apiHash, {
  connectionRetries: 5
});

console.log(`Using Telegram credentials from ${credentials.root}`);
await client.start({
  phoneNumber: async () => phoneNumber || input.text("Telegram phone: "),
  password: async () => input.password("Telegram 2FA password: "),
  phoneCode: async () => input.text("Telegram login code: "),
  onError: (error) => {
    console.error(error.message);
  }
});

const session = client.session.save();
fs.writeFileSync(sessionPath, session, { mode: 0o600 });
console.log(`Saved Telegram session to ${sessionPath}`);
await client.disconnect();
