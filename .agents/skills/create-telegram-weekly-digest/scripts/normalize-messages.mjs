import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";

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
const baseDir = path.join(repoRoot, "Posts", "research", "telegram");
const configPath = path.join(baseDir, "channels.yaml");
const rawDir = path.join(baseDir, "raw");
const normalizedDir = path.join(baseDir, "normalized");

function latestJson(dir) {
  const files = fs
    .readdirSync(dir)
    .filter((file) => file.endsWith(".json"))
    .sort();
  if (files.length === 0) throw new Error(`No JSON files in ${dir}.`);
  return path.join(dir, files[files.length - 1]);
}

function normalizeText(text) {
  return String(text || "")
    .replace(/\r\n/g, "\n")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .replace(/[ \t]{2,}/g, " ")
    .trim();
}

function keywordMatch(text, keywords = []) {
  const lower = text.toLowerCase();
  return keywords.some((keyword) => lower.includes(String(keyword).toLowerCase()));
}

function signature(message) {
  const normalized = normalizeText(message.text).toLowerCase();
  return normalized.replace(/\s+/g, " ").slice(0, 500);
}

function preliminaryScore(message, channelConfig, globalPreferences) {
  const text = normalizeText(message.text);
  const priorityTopics = globalPreferences.priority_topics || [];
  let score = Number(message.channel_weight || 1);

  if (keywordMatch(text, channelConfig.include_keywords || [])) score += 2;
  if (keywordMatch(text, priorityTopics)) score += 2;
  if ((message.views || 0) > 0) score += Math.min(2, Math.log10(message.views + 1) / 2);
  if ((message.forwards || 0) > 0) score += 0.5;
  if ((message.replies || 0) > 0) score += 0.5;
  if (text.length > 700) score += 0.5;

  return Number(score.toFixed(2));
}

if (!fs.existsSync(configPath)) {
  throw new Error(`Missing ${configPath}.`);
}

const config = yaml.load(fs.readFileSync(configPath, "utf8")) || {};
const minViews = Number(config.min_views || 0);
const rawPath = process.argv[2] ? path.resolve(process.argv[2]) : latestJson(rawDir);
const raw = JSON.parse(fs.readFileSync(rawPath, "utf8"));
const channelsByHandle = new Map(
  (config.channels || []).map((channel) => [
    String(channel.handle || "").replace(/^@/, "").replace(/^https?:\/\/t\.me\//, ""),
    channel
  ])
);
const seen = new Set();
const messages = [];

for (const message of raw.messages || []) {
  const text = normalizeText(message.text);
  if (!text) continue;
  if (text.length < 80) continue;
  if ((message.views || 0) < minViews) continue;

  const channelConfig = channelsByHandle.get(message.channel_handle) || {};
  if (keywordMatch(text, channelConfig.exclude_keywords || [])) continue;
  if (keywordMatch(text, config.preferences?.avoid || [])) continue;

  const dedupeKey = message.grouped_id || signature(message);
  if (seen.has(dedupeKey)) continue;
  seen.add(dedupeKey);

  messages.push({
    ...message,
    text,
    preliminary_score: preliminaryScore(message, channelConfig, config.preferences || {})
  });
}

messages.sort((a, b) => {
  if (b.preliminary_score !== a.preliminary_score) return b.preliminary_score - a.preliminary_score;
  return new Date(b.date) - new Date(a.date);
});

const normalized = {
  period_id: raw.period_id,
  period_start: raw.period_start,
  period_end: raw.period_end,
  captured_at: new Date().toISOString(),
  source_raw_file: path.relative(repoRoot, rawPath),
  total_raw_messages: (raw.messages || []).length,
  total_normalized_messages: messages.length,
  messages
};

fs.mkdirSync(normalizedDir, { recursive: true });
const outPath = path.join(normalizedDir, `${raw.period_id}.json`);
fs.writeFileSync(outPath, `${JSON.stringify(normalized, null, 2)}\n`);
console.log(`Saved ${messages.length} normalized messages to ${outPath}`);
