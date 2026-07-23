#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const root = process.cwd();
const excludedEverywhere = new Set([
  ".git",
  ".obsidian",
  "node_modules",
  "tmp",
  ".agents",
]);
const excludedFromLinkScan = new Set([
  "raw",
  "normalized",
  "agentic-engineering-book-main",
  "oper8-v0-8-book",
]);

function walk(directory, exclusions) {
  const result = [];

  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    if (entry.isDirectory() && exclusions.has(entry.name)) {
      continue;
    }

    const absolutePath = path.join(directory, entry.name);

    if (entry.isDirectory()) {
      result.push(...walk(absolutePath, exclusions));
    } else {
      result.push(absolutePath);
    }
  }

  return result;
}

function vaultPath(absolutePath) {
  return path.relative(root, absolutePath).split(path.sep).join("/");
}

const allFiles = walk(root, excludedEverywhere);
const allPaths = allFiles.map(vaultPath);
const allPathSet = new Set(allPaths);
const markdownFiles = allFiles.filter((file) => {
  if (!file.endsWith(".md")) {
    return false;
  }

  return !vaultPath(file)
    .split("/")
    .some((segment) => excludedFromLinkScan.has(segment));
});

function existsAsVaultTarget(target, sourcePath) {
  const normalizedTarget = target.replace(/^\.\//, "");
  const sourceDirectory = path.posix.dirname(sourcePath);
  const candidates = [
    normalizedTarget,
    `${normalizedTarget}.md`,
    path.posix.normalize(path.posix.join(sourceDirectory, normalizedTarget)),
    path.posix.normalize(path.posix.join(sourceDirectory, `${normalizedTarget}.md`)),
  ];

  if (candidates.some((candidate) => allPathSet.has(candidate))) {
    return true;
  }

  return allPaths.some(
    (candidate) =>
      candidate.endsWith(`/${normalizedTarget}`) ||
      candidate.endsWith(`/${normalizedTarget}.md`),
  );
}

const brokenLinks = [];
const wikilinkPattern = /\[\[([^\]]+)\]\]/g;

for (const absolutePath of markdownFiles) {
  const sourcePath = vaultPath(absolutePath);
  const contents = fs.readFileSync(absolutePath, "utf8");
  let match;

  while ((match = wikilinkPattern.exec(contents)) !== null) {
    const rawTarget = match[1];
    const aliasPosition = rawTarget.search(/\\?\|/);
    const withoutAlias =
      aliasPosition === -1 ? rawTarget : rawTarget.slice(0, aliasPosition);
    const target = withoutAlias.split("#")[0].trim();

    if (!target || existsAsVaultTarget(target, sourcePath)) {
      continue;
    }

    brokenLinks.push({ sourcePath, target });
  }
}

const duplicateNames = new Map();

for (const absolutePath of markdownFiles) {
  const name = path.basename(absolutePath);
  const paths = duplicateNames.get(name) ?? [];
  paths.push(vaultPath(absolutePath));
  duplicateNames.set(name, paths);
}

const ambiguousNames = [...duplicateNames.entries()].filter(
  ([name, paths]) =>
    paths.length > 1 &&
    !["AGENTS.md", "Context.md", "_index.md", "summary.md", "transcript.md"].includes(
      name,
    ) &&
    !/^\d{4}-\d{2}-essay\.md$/.test(name),
);

console.log(`Markdown-файлов проверено: ${markdownFiles.length}`);
console.log(`Неразрешённых wikilinks: ${brokenLinks.length}`);

for (const link of brokenLinks) {
  console.log(`BROKEN ${link.sourcePath} -> ${link.target}`);
}

console.log(`Неоднозначных имен заметок: ${ambiguousNames.length}`);

for (const [name, paths] of ambiguousNames) {
  console.log(`AMBIGUOUS ${name}`);
  for (const candidate of paths) {
    console.log(`  ${candidate}`);
  }
}

if (brokenLinks.length > 0) {
  process.exitCode = 1;
}
