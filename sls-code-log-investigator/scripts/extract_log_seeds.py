#!/usr/bin/env python3
"""Extract likely SLS search seeds from a source tree."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path


SOURCE_SUFFIXES = {
    ".java",
    ".kt",
    ".scala",
    ".go",
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".xml",
    ".yml",
    ".yaml",
    ".properties",
}

SKIP_DIRS = {
    ".git",
    ".idea",
    ".gradle",
    ".mvn",
    "build",
    "dist",
    "node_modules",
    "target",
    "out",
}

LOG_RE = re.compile(
    r"(logger|log|LOGGER)\s*\.\s*(trace|debug|info|warn|error)\s*\(|"
    r"System\.(out|err)\.println\s*\(|"
    r"throw\s+new\s+\w+|"
    r"@(?:Get|Post|Put|Delete|Patch|Request)Mapping\s*\(",
)

STRING_RE = re.compile(r'"((?:[^"\\]|\\.){4,200})"|\'((?:[^\'\\]|\\.){4,200})\'')
IDENTIFIER_RE = re.compile(
    r"\b(?:[A-Z][A-Za-z0-9_]*(?:Exception|Error|Service|Controller|Manager|Handler|Client|DTO|VO)|"
    r"[a-z][A-Za-z0-9_]*(?:Id|ID|Key|Code|Status|Topic|Type|Biz|Task))\b"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to scan")
    parser.add_argument(
        "--keyword",
        action="append",
        default=[],
        help="Symptom/domain keyword. May be passed multiple times.",
    )
    parser.add_argument("--limit", type=int, default=80, help="Maximum result rows")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix in SOURCE_SUFFIXES:
                yield path


def normalize_string(value: str) -> str:
    return value.encode("utf-8", "ignore").decode("unicode_escape", "ignore").strip()


def line_matches_keywords(line: str, keywords: list[str]) -> bool:
    if not keywords:
        return True
    lowered = line.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def extract_strings(line: str) -> list[str]:
    values = []
    for match in STRING_RE.finditer(line):
        value = normalize_string(match.group(1) or match.group(2) or "")
        if value and not value.isspace():
            values.append(value)
    return values


def scan(root: Path, keywords: list[str], limit: int) -> list[dict]:
    results = []
    for path in iter_files(root):
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for idx, line in enumerate(lines, start=1):
            if not LOG_RE.search(line) and not line_matches_keywords(line, keywords):
                continue
            if not line_matches_keywords(line, keywords) and not any(
                line_matches_keywords(seed, keywords) for seed in extract_strings(line)
            ):
                continue
            strings = extract_strings(line)
            identifiers = sorted(set(IDENTIFIER_RE.findall(line)))
            if not strings and not identifiers and not LOG_RE.search(line):
                continue
            results.append(
                {
                    "file": str(path.relative_to(root)),
                    "line": idx,
                    "kind": "log-or-route" if LOG_RE.search(line) else "keyword-context",
                    "strings": strings[:5],
                    "identifiers": identifiers[:10],
                    "source": line.strip()[:300],
                }
            )
            if len(results) >= limit:
                return results
    return results


def print_text(results: list[dict]) -> None:
    if not results:
        print("No candidate log seeds found.")
        return
    for item in results:
        print(f"{item['file']}:{item['line']} [{item['kind']}]")
        if item["strings"]:
            print("  strings: " + " | ".join(item["strings"]))
        if item["identifiers"]:
            print("  identifiers: " + ", ".join(item["identifiers"]))
        print(f"  source: {item['source']}")


def main() -> None:
    args = parse_args()
    root = Path(args.root).resolve()
    results = scan(root, args.keyword, args.limit)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_text(results)


if __name__ == "__main__":
    main()
