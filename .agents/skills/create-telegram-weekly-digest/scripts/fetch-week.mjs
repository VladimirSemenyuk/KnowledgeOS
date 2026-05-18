import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";
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
const configPath = path.join(repoRoot, "Posts", "research", "telegram", "channels.yaml");
const rawDir = path.join(repoRoot, "Posts", "research", "telegram", "raw");

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

function isSandboxNetworkError(error) {
  const message = String(error?.message || error || "");
  return (
    error?.code === "EPERM" ||
    message.includes("connect EPERM") ||
    message.includes("WebSocket connection failed")
  );
}

function isoWeek(date) {
  const working = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const day = working.getUTCDay() || 7;
  working.setUTCDate(working.getUTCDate() + 4 - day);
  const yearStart = new Date(Date.UTC(working.getUTCFullYear(), 0, 1));
  const week = Math.ceil(((working - yearStart) / 86400000 + 1) / 7);
  return `${working.getUTCFullYear()}-W${String(week).padStart(2, "0")}`;
}

function normalizeHandle(handle) {
  return String(handle || "")
    .trim()
    .replace(/^https?:\/\/t\.me\//, "")
    .replace(/^@/, "")
    .replace(/\/$/, "");
}

function messageDate(value) {
  if (!value) return null;
  if (value instanceof Date) return value;
  if (typeof value === "number") return new Date(value * 1000);
  return new Date(value);
}

function messageUrl(handle, messageId) {
  const cleanHandle = normalizeHandle(handle);
  if (!cleanHandle || !messageId) return "";
  return `https://t.me/${cleanHandle}/${messageId}`;
}

function serializeMessage(message, channel) {
  const date = messageDate(message.date);
  return {
    channel_title: channel.title || normalizeHandle(channel.handle),
    channel_handle: normalizeHandle(channel.handle),
    channel_weight: Number(channel.weight || 1),
    channel_language: channel.language || "",
    channel_themes: channel.themes || [],
    message_id: message.id,
    date: date ? date.toISOString() : null,
    text: message.message || message.text || "",
    views: message.views || 0,
    forwards: message.forwards || 0,
    replies: message.replies?.replies || 0,
    grouped_id: message.groupedId ? String(message.groupedId) : "",
    url: messageUrl(channel.handle, message.id)
  };
}

if (!fs.existsSync(configPath)) {
  throw new Error(`Missing ${configPath}. Create it from references/config.example.yaml first.`);
}

loadEnvFile(envPath);

const apiId = Number(requiredEnv("TELEGRAM_API_ID"));
const apiHash = requiredEnv("TELEGRAM_API_HASH");
if (!Number.isInteger(apiId)) throw new Error("TELEGRAM_API_ID must be an integer.");
if (!fs.existsSync(sessionPath)) throw new Error(`Missing ${sessionPath}. Run scripts/auth.mjs first.`);

const config = yaml.load(fs.readFileSync(configPath, "utf8")) || {};
const channels = Array.isArray(config.channels) ? config.channels : [];
if (channels.length === 0) throw new Error("channels.yaml has no channels.");

const periodDays = Number(config.period_days || 7);
const maxMessagesPerChannel = Number(config.max_messages_per_channel || 200);
const since = new Date(Date.now() - periodDays * 86400000);
const until = new Date();
const periodId = isoWeek(until);
const session = fs.readFileSync(sessionPath, "utf8").trim();
const client = new TelegramClient(new StringSession(session), apiId, apiHash, {
  connectionRetries: 5
});

console.log(`Using Telegram credentials from ${credentials.root}`);
try {
  await client.connect();
} catch (error) {
  if (isSandboxNetworkError(error)) {
    throw new Error(
      "Telegram connection was blocked by the Codex sandbox network policy. " +
        "Re-run this fetch command with sandbox_permissions=require_escalated to allow direct Telegram DC access."
    );
  }
  throw error;
}

const result = {
  period_id: periodId,
  period_start: since.toISOString(),
  period_end: until.toISOString(),
  captured_at: new Date().toISOString(),
  channels: [],
  messages: []
};

for (const channel of channels) {
  const handle = normalizeHandle(channel.handle);
  if (!handle) continue;
  console.log(`Fetching @${handle}`);
  try {
    const messages = await client.getMessages(handle, { limit: maxMessagesPerChannel });
    const serialized = messages
      .map((message) => serializeMessage(message, channel))
      .filter((message) => {
        if (!message.date) return false;
        const date = new Date(message.date);
        return date >= since && date <= until;
      });

    result.channels.push({
      title: channel.title || handle,
      handle,
      fetched: messages.length,
      in_period: serialized.length
    });
    result.messages.push(...serialized);
  } catch (error) {
    result.channels.push({
      title: channel.title || handle,
      handle,
      error: error.message
    });
  }
}

await client.disconnect();

fs.mkdirSync(rawDir, { recursive: true });
const outPath = path.join(rawDir, `${periodId}.json`);
fs.writeFileSync(outPath, `${JSON.stringify(result, null, 2)}\n`);
console.log(`Saved ${result.messages.length} messages to ${outPath}`);
