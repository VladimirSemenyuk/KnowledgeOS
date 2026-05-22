#!/usr/bin/env python3
"""Convert an HTML or TXT meeting transcript into the vault transcript.md layout."""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path


MONTHS_RU = {
    "января": "01",
    "февраля": "02",
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": "10",
    "ноября": "11",
    "декабря": "12",
}


class TextExtractor(HTMLParser):
    BLOCK_TAGS = {
        "address",
        "article",
        "aside",
        "blockquote",
        "br",
        "caption",
        "div",
        "figcaption",
        "footer",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "hr",
        "li",
        "main",
        "p",
        "pre",
        "section",
        "table",
        "td",
        "th",
        "tr",
    }

    SKIP_TAGS = {"script", "style", "noscript", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        text = "".join(self.parts)
        text = html.unescape(text)
        text = text.replace("\xa0", " ")
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
        lines = [line for line in lines if line]
        return "\n".join(lines)


class StructuredTranscriptExtractor(HTMLParser):
    """Extract Fireflies-style transcript paragraph blocks from exported HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.turns: list[TranscriptTurn] = []
        self.paragraph_depth = 0
        self.in_name = False
        self.sentence_depth = 0
        self.speaker_parts: list[str] = []
        self.timestamp: str | None = None
        self.text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key: value or "" for key, value in attrs}
        classes = set(attrs_dict.get("class", "").split())
        elem_id = attrs_dict.get("id", "")

        if tag == "div" and elem_id.startswith("transcript-paragraph-"):
            self.paragraph_depth = 1
            self.speaker_parts = []
            self.timestamp = None
            self.text_parts = []
            return

        if self.paragraph_depth:
            if tag == "div":
                self.paragraph_depth += 1
            if tag == "span" and "name" in classes:
                self.in_name = True
            if self.sentence_depth:
                self.sentence_depth += 1
            elif "transcript-sentence" in classes:
                self.sentence_depth = 1

    def handle_endtag(self, tag: str) -> None:
        if self.in_name and tag == "span":
            self.in_name = False
        if self.sentence_depth:
            self.sentence_depth -= 1

        if self.paragraph_depth and tag == "div":
            self.paragraph_depth -= 1
            if self.paragraph_depth == 0:
                speaker = normalize_speaker(" ".join(self.speaker_parts))
                text = re.sub(r"\s+", " ", " ".join(self.text_parts)).strip()
                if speaker and text:
                    self.turns.append(TranscriptTurn(speaker, text, self.timestamp))

    def handle_data(self, data: str) -> None:
        if not self.paragraph_depth:
            return
        clean = data.replace("\xa0", " ").strip()
        if not clean:
            return
        if self.in_name:
            self.speaker_parts.append(clean)
        elif self.sentence_depth:
            self.text_parts.append(clean)
        elif self.timestamp is None and re.fullmatch(r"\d{1,2}:\d{2}(?::\d{2})?", clean):
            self.timestamp = clean


@dataclass
class TranscriptTurn:
    speaker: str
    text: str
    timestamp: str | None = None


def normalize_speaker(name: str) -> str:
    name = re.sub(r"\s+", " ", name).strip(" -:\t")
    if len(name) >= 3 and name[0].casefold() == name[1].casefold() and name[2].isalpha():
        name = name[1:]
    return name.strip()


def normalize_date(value: str) -> str | None:
    patterns = [
        r"\b(20\d{2})[-./](\d{1,2})[-./](\d{1,2})\b",
        r"\b(\d{1,2})[-./](\d{1,2})[-./](20\d{2})\b",
    ]
    match = re.search(patterns[0], value)
    if match:
        year, month, day = match.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    match = re.search(patterns[1], value)
    if match:
        day, month, year = match.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"

    ru_match = re.search(
        r"\b(\d{1,2})\s+("
        + "|".join(MONTHS_RU)
        + r")\s+(20\d{2})\b",
        value.casefold(),
    )
    if ru_match:
        day, month_name, year = ru_match.groups()
        return f"{int(year):04d}-{MONTHS_RU[month_name]}-{int(day):02d}"

    return None


def find_date(text: str, input_path: Path, explicit_date: str | None) -> tuple[str, str]:
    if explicit_date:
        date = normalize_date(explicit_date)
        if not date:
            raise SystemExit(f"Cannot parse --date: {explicit_date}")
        return date, "argument"

    for source, value in (("html", text), ("filename", input_path.name)):
        date = normalize_date(value)
        if date:
            return date, source

    stat = input_path.stat()
    return datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d"), "file-mtime"


def discover_mentee_dirs(vault_root: Path) -> list[Path]:
    clients = vault_root / "Clients"
    results: list[Path] = []
    if not clients.exists():
        return results
    for context in clients.rglob("Context.md"):
        if "Meetings" not in context.parts:
            results.append(context.parent)
    for context in clients.rglob("Contex.md"):
        if "Meetings" not in context.parts:
            results.append(context.parent)
    return sorted(set(results), key=lambda p: str(p).casefold())


def score_mentee_dir(path: Path, text: str, explicit_mentee: str | None) -> int:
    score = 0
    haystack = text.casefold()
    name = path.name
    if explicit_mentee:
        if explicit_mentee.casefold() == name.casefold():
            score += 100
        elif explicit_mentee.casefold() in str(path).casefold():
            score += 60
    if name.casefold() in haystack:
        score += 25
    context = path / "Context.md"
    if not context.exists():
        context = path / "Contex.md"
    if context.exists():
        try:
            context_text = context.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            context_text = ""
        for token in re.findall(r"[\wА-Яа-яЁё-]{3,}", name):
            if token.casefold() in haystack:
                score += 5
        for line in context_text.splitlines()[:80]:
            clean = re.sub(r"[*_`#>\-:]+", " ", line).strip()
            if len(clean) >= 3 and clean.casefold() in haystack:
                score += 2
    return score


def find_mentee_dir(
    vault_root: Path,
    text: str,
    explicit_mentee: str | None,
    output_dir: str | None,
) -> Path:
    if output_dir:
        path = (vault_root / output_dir).resolve()
        if not path.exists():
            raise SystemExit(f"Output directory does not exist: {path}")
        return path

    dirs = discover_mentee_dirs(vault_root)
    scored = [(score_mentee_dir(path, text, explicit_mentee), path) for path in dirs]
    scored = [(score, path) for score, path in scored if score > 0]
    scored.sort(key=lambda item: (-item[0], str(item[1]).casefold()))

    if not scored:
        raise SystemExit("Cannot determine mentee. Re-run with --mentee or --output-dir.")
    if len(scored) > 1 and scored[0][0] == scored[1][0]:
        options = "\n".join(f"- {path}" for _, path in scored[:5])
        raise SystemExit(f"Mentee is ambiguous. Re-run with --output-dir.\n{options}")
    return scored[0][1]


def parse_turns(text: str) -> list[TranscriptTurn]:
    lines = text.splitlines()
    turns: list[TranscriptTurn] = []
    current_speaker: str | None = None
    current_timestamp: str | None = None
    current_text: list[str] = []

    speaker_re = re.compile(
        r"^(?P<speaker>[A-Za-zА-Яа-яЁё][A-Za-zА-Яа-яЁё .'\-]{1,60})\s*[:\-–]\s*(?P<body>.*)$"
    )
    speaker_timestamp_re = re.compile(
        r"^(?P<speaker>[A-Za-zА-Яа-яЁё][A-Za-zА-Яа-яЁё .'\-]{1,60})\s+"
        r"(?P<timestamp>\d{1,2}:\d{2}(?::\d{2})?)\s+(?P<body>.*)$"
    )

    for line in lines:
        clean = line.strip()
        if not clean:
            continue
        timestamp_match = speaker_timestamp_re.match(clean)
        match = speaker_re.match(clean)
        if timestamp_match:
            if current_speaker and current_text:
                turns.append(
                    TranscriptTurn(
                        current_speaker,
                        " ".join(current_text).strip(),
                        current_timestamp,
                    )
                )
            current_speaker = normalize_speaker(timestamp_match.group("speaker"))
            current_timestamp = timestamp_match.group("timestamp")
            current_text = [timestamp_match.group("body").strip()]
        elif match:
            if current_speaker and current_text:
                turns.append(
                    TranscriptTurn(
                        current_speaker,
                        " ".join(current_text).strip(),
                        current_timestamp,
                    )
                )
            current_speaker = normalize_speaker(match.group("speaker"))
            current_timestamp = None
            body = match.group("body").strip()
            current_text = [body] if body else []
        elif current_speaker:
            current_text.append(clean)
        else:
            turns.append(TranscriptTurn("Transcript", clean))

    if current_speaker and current_text:
        turns.append(TranscriptTurn(current_speaker, " ".join(current_text).strip(), current_timestamp))

    return merge_turns(turns)


def merge_turns(turns: list[TranscriptTurn]) -> list[TranscriptTurn]:
    merged: list[TranscriptTurn] = []
    for turn in turns:
        text = re.sub(r"\s+", " ", turn.text).strip()
        if not text:
            continue
        if merged and merged[-1].speaker == turn.speaker and not merged[-1].timestamp and not turn.timestamp:
            merged[-1].text = f"{merged[-1].text} {text}"
        else:
            merged.append(TranscriptTurn(turn.speaker, text, turn.timestamp))
    return merged


def markdown_escape(text: str) -> str:
    return text.replace("\r", "").strip()


def render_markdown(mentee: str, date: str, turns: list[TranscriptTurn]) -> str:
    lines = [f"# Transcript встречи: {mentee} & Владимир {date}", ""]
    for turn in turns:
        speaker = markdown_escape(normalize_speaker(turn.speaker))
        body = markdown_escape(turn.text)
        if speaker == "Transcript":
            lines.extend([body, ""])
        else:
            timestamp = f" *[{markdown_escape(turn.timestamp)}]*" if turn.timestamp else ""
            lines.extend([f"**{speaker}**{timestamp}: {body}", ""])
    return "\n".join(lines).rstrip() + "\n"


def extract_input_text(input_path: Path) -> tuple[str, str]:
    raw = input_path.read_text(encoding="utf-8", errors="ignore")
    if input_path.suffix.casefold() in {".html", ".htm"}:
        extractor = TextExtractor()
        extractor.feed(raw)
        text = extractor.text()
        if not text:
            raise SystemExit("No transcript text found in HTML.")
        return text, raw

    text = raw.replace("\ufeff", "").replace("\xa0", " ")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    text = "\n".join(line for line in lines if line)
    if not text:
        raise SystemExit("No transcript text found in input file.")
    return text, raw


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="HTML or TXT transcript file")
    parser.add_argument("--mentee", help="Mentee name, if not obvious")
    parser.add_argument("--date", help="Meeting date, e.g. 2026-05-13")
    parser.add_argument("--output-dir", help="Existing mentee directory relative to vault root")
    parser.add_argument("--vault-root", default=".", help="Vault root; default is current directory")
    parser.add_argument("--force", action="store_true", help="Overwrite transcript.md if it exists")
    args = parser.parse_args()

    vault_root = Path(args.vault_root).resolve()
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = (vault_root / input_path).resolve()
    if not input_path.exists():
        raise SystemExit(f"Input file does not exist: {input_path}")

    text, raw_input = extract_input_text(input_path)

    date, date_source = find_date(text, input_path, args.date)
    mentee_dir = find_mentee_dir(vault_root, text, args.mentee, args.output_dir)
    meeting_dir = mentee_dir / "Meetings" / f"{date}-meeting"
    output_path = meeting_dir / "transcript.md"

    if output_path.exists() and not args.force:
        raise SystemExit(f"Output already exists: {output_path}\nRe-run with --force to overwrite.")

    structured_turns: list[TranscriptTurn] = []
    if input_path.suffix.casefold() in {".html", ".htm"}:
        structured_extractor = StructuredTranscriptExtractor()
        structured_extractor.feed(raw_input)
        structured_turns = structured_extractor.turns
    turns = merge_turns(structured_turns) or parse_turns(text)
    markdown = render_markdown(mentee_dir.name, date, turns)
    meeting_dir.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    rel = output_path.relative_to(vault_root)
    print(f"created: {rel}")
    print(f"date: {date} ({date_source})")
    print(f"mentee: {mentee_dir.relative_to(vault_root)}")
    if date_source == "file-mtime":
        print("warning: date came from file mtime; verify it is correct")
    return 0


if __name__ == "__main__":
    sys.exit(main())
