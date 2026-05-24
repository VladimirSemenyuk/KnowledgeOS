#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";

const DEFAULT_EXTENSIONS = [".md", ".markdown", ".txt"];
const DEFAULT_LOCALES = ["ru", "en-US"];
const SKIP_DIRS = new Set([".git", ".obsidian", "node_modules"]);

function printUsage() {
  console.log(`Usage:
  npm --prefix .agents/skills/apply-typograf run typograf -- <file-or-folder> [options]

Options:
  --write                 Write changes. Without this flag the script runs dry-run.
  --dry-run               Show what would change without writing files.
  --locale ru,en-US       Typograf locales. Default: ru,en-US.
  --extensions .md,.txt   Extensions to process in folders. Default: .md,.markdown,.txt.
  --force                 Process an explicitly selected file even with a non-default extension.
  --help                  Show this help.
`);
}

function parseArgs(argv) {
  const args = {
    target: null,
    write: false,
    dryRun: true,
    force: false,
    locales: DEFAULT_LOCALES,
    extensions: DEFAULT_EXTENSIONS,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];

    if (arg === "--help" || arg === "-h") {
      args.help = true;
    } else if (arg === "--write") {
      args.write = true;
      args.dryRun = false;
    } else if (arg === "--dry-run") {
      args.dryRun = true;
      args.write = false;
    } else if (arg === "--force") {
      args.force = true;
    } else if (arg === "--locale") {
      i += 1;
      args.locales = parseCsvArg(argv[i], "--locale");
    } else if (arg.startsWith("--locale=")) {
      args.locales = parseCsvArg(arg.slice("--locale=".length), "--locale");
    } else if (arg === "--extensions") {
      i += 1;
      args.extensions = normalizeExtensions(parseCsvArg(argv[i], "--extensions"));
    } else if (arg.startsWith("--extensions=")) {
      args.extensions = normalizeExtensions(parseCsvArg(arg.slice("--extensions=".length), "--extensions"));
    } else if (arg.startsWith("-")) {
      throw new Error(`Unknown option: ${arg}`);
    } else if (!args.target) {
      args.target = arg;
    } else {
      throw new Error(`Unexpected extra argument: ${arg}`);
    }
  }

  return args;
}

function parseCsvArg(value, optionName) {
  if (!value) {
    throw new Error(`${optionName} requires a comma-separated value.`);
  }

  const parsed = value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);

  if (parsed.length === 0) {
    throw new Error(`${optionName} requires at least one value.`);
  }

  return parsed;
}

function normalizeExtensions(extensions) {
  return extensions.map((extension) => (
    extension.startsWith(".") ? extension.toLowerCase() : `.${extension.toLowerCase()}`
  ));
}

async function collectFiles(targetPath, extensions, force) {
  const stat = await fs.stat(targetPath);

  if (stat.isFile()) {
    const extension = path.extname(targetPath).toLowerCase();
    if (!force && !extensions.includes(extension)) {
      throw new Error(`Unsupported file extension: ${extension || "(none)"}. Use --force for an explicitly selected file.`);
    }
    return [targetPath];
  }

  if (!stat.isDirectory()) {
    throw new Error(`Target is neither a file nor a directory: ${targetPath}`);
  }

  const files = [];
  await walkDirectory(targetPath, extensions, files);
  files.sort((a, b) => a.localeCompare(b));
  return files;
}

async function walkDirectory(directoryPath, extensions, files) {
  const entries = await fs.readdir(directoryPath, { withFileTypes: true });

  for (const entry of entries) {
    const entryPath = path.join(directoryPath, entry.name);

    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name)) {
        continue;
      }
      await walkDirectory(entryPath, extensions, files);
    } else if (entry.isFile()) {
      const extension = path.extname(entry.name).toLowerCase();
      if (extensions.includes(extension)) {
        files.push(entryPath);
      }
    }
  }
}

function splitLineEnding(chunk) {
  if (chunk.endsWith("\r\n")) {
    return [chunk.slice(0, -2), "\r\n"];
  }
  if (chunk.endsWith("\n")) {
    return [chunk.slice(0, -1), "\n"];
  }
  return [chunk, ""];
}

function typografMarkdown(text, typograf) {
  const chunks = text.match(/.*(?:\r?\n|$)/g) ?? [];
  if (chunks.at(-1) === "") {
    chunks.pop();
  }

  let inFrontmatter = false;
  let inFence = false;
  let fenceMarker = null;

  return chunks.map((chunk, index) => {
    const [line, ending] = splitLineEnding(chunk);
    const trimmed = line.trim();

    if (index === 0 && trimmed === "---") {
      inFrontmatter = true;
      return chunk;
    }

    if (inFrontmatter) {
      if (index > 0 && (trimmed === "---" || trimmed === "...")) {
        inFrontmatter = false;
      }
      return chunk;
    }

    const fenceMatch = line.match(/^\s*(```|~~~)/);
    if (fenceMatch) {
      const marker = fenceMatch[1];
      if (!inFence) {
        inFence = true;
        fenceMarker = marker;
      } else if (marker === fenceMarker) {
        inFence = false;
        fenceMarker = null;
      }
      return chunk;
    }

    if (inFence || /^( {4}|\t)/.test(line)) {
      return chunk;
    }

    return `${typografLine(line, typograf)}${ending}`;
  }).join("");
}

function typografLine(line, typograf) {
  if (!line.trim()) {
    return line;
  }

  const protectedSpans = [];
  let protectedLine = line;

  const protect = (regex) => {
    protectedLine = protectedLine.replace(regex, (match) => {
      const token = `\uE000TYPOGRAF_${protectedSpans.length}\uE001`;
      protectedSpans.push(match);
      return token;
    });
  };

  protect(/`[^`]*`/g);
  protect(/!\[\[[^\]]+\]\]/g);
  protect(/\[\[[^\]]+\]\]/g);
  protect(/!\[[^\]]*\]\([^)]+\)/g);
  protect(/\[[^\]]+\]\([^)]+\)/g);
  protect(/<https?:\/\/[^>]+>/g);
  protect(/https?:\/\/[^\s)\]]+/g);
  protect(/#[\p{L}\p{N}_/-]+/gu);
  protect(/\$[^$\n]+\$/g);
  protect(/<\/?[A-Za-z][^>]*>/g);

  const result = typograf.execute(protectedLine);
  return protectedSpans.reduce(
    (restored, span, index) => restored.replaceAll(`\uE000TYPOGRAF_${index}\uE001`, span),
    result,
  );
}

async function loadTypograf() {
  try {
    const imported = await import("typograf");
    return imported.default ?? imported.Typograf ?? imported;
  } catch (error) {
    if (error?.code === "ERR_MODULE_NOT_FOUND" || error?.code === "MODULE_NOT_FOUND") {
      throw new Error("Package `typograf` is not installed. Run: npm --prefix .agents/skills/apply-typograf install");
    }
    throw error;
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    printUsage();
    return;
  }

  if (!args.target) {
    printUsage();
    throw new Error("Missing target file or folder.");
  }

  const baseCwd = process.env.INIT_CWD || process.cwd();
  const targetPath = path.resolve(baseCwd, args.target);
  const files = await collectFiles(targetPath, args.extensions, args.force);

  if (files.length === 0) {
    console.log("No matching files found.");
    return;
  }

  const Typograf = await loadTypograf();
  const typograf = new Typograf({ locale: args.locales });
  const changed = [];

  for (const filePath of files) {
    const original = await fs.readFile(filePath, "utf8");
    const updated = typografMarkdown(original, typograf);

    if (updated !== original) {
      changed.push(filePath);
      if (args.write) {
        await fs.writeFile(filePath, updated, "utf8");
      }
    }
  }

  const relativeChanged = changed.map((filePath) => path.relative(baseCwd, filePath));
  if (args.write) {
    console.log(`Changed files: ${changed.length}`);
  } else {
    console.log(`Files that would change: ${changed.length}`);
  }

  for (const filePath of relativeChanged) {
    console.log(`- ${filePath}`);
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
