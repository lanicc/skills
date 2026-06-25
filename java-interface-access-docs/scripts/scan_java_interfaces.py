#!/usr/bin/env python3
"""Index Spring HTTP and Dubbo interface entry points in a Java project."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HTTP_ANNOTATIONS = (
    "RequestMapping",
    "GetMapping",
    "PostMapping",
    "PutMapping",
    "DeleteMapping",
    "PatchMapping",
)
DUBBO_MARKERS = ("DubboService", "DubboReference", "@Reference")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def annotation_value(line: str) -> str:
    match = re.search(r'@(?:\w+\.)?(\w+Mapping)\s*\((.*)\)', line)
    if not match:
        return ""
    inside = match.group(2)
    strings = re.findall(r'"([^"]+)"', inside)
    return ", ".join(strings) if strings else inside.strip()


def java_name(text: str, kind: str) -> str:
    if kind == "package":
        match = re.search(r"^\s*package\s+([\w.]+)\s*;", text, re.M)
    else:
        match = re.search(r"\b(?:class|interface|enum)\s+(\w+)", text)
    return match.group(1) if match else ""


def nearby_signature(lines: list[str], start: int) -> str:
    buf: list[str] = []
    seen_declaration = False
    paren_balance = 0
    for idx in range(start + 1, min(len(lines), start + 16)):
        stripped = lines[idx].strip()
        if not stripped:
            continue
        if stripped.startswith("@") and not seen_declaration:
            continue
        if re.match(r"^(public|protected|private|static|final|abstract|class|interface)\b", stripped):
            seen_declaration = True
        if not seen_declaration:
            continue
        buf.append(stripped)
        paren_balance += stripped.count("(") - stripped.count(")")
        if ("{" in stripped or ";" in stripped) and paren_balance <= 0:
            break
    return re.sub(r"\s+", " ", " ".join(buf)).replace(" {", "")


def scan_file(path: Path, keyword: str | None) -> dict | None:
    text = read_text(path)
    if keyword and keyword.lower() not in text.lower() and keyword.lower() not in str(path).lower():
        return None

    lines = text.splitlines()
    http: list[dict] = []
    dubbo_refs: list[dict] = []
    dubbo_services: list[dict] = []

    class_mapping = ""
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if any(f"@{ann}" in stripped for ann in HTTP_ANNOTATIONS):
            value = annotation_value(stripped)
            sig = nearby_signature(lines, idx)
            item = {"line": idx + 1, "annotation": stripped, "value": value, "signature": sig}
            if " class " in sig or sig.startswith("public class") or sig.startswith("class "):
                class_mapping = value
                item["scope"] = "class"
            else:
                item["scope"] = "method"
                item["class_mapping"] = class_mapping
            http.append(item)

        if stripped.startswith("import "):
            continue

        if any(marker in stripped for marker in DUBBO_MARKERS):
            sig = nearby_signature(lines, idx)
            target = {"line": idx + 1, "annotation": stripped, "signature": sig}
            if "DubboService" in stripped:
                dubbo_services.append(target)
            else:
                dubbo_refs.append(target)

    is_facade = bool(re.search(r"\binterface\s+\w*(Facade|Service)\b", text))
    if not (http or dubbo_refs or dubbo_services or is_facade):
        return None

    return {
        "path": str(path),
        "package": java_name(text, "package"),
        "type": java_name(text, "type"),
        "http": http,
        "dubbo_references": dubbo_refs,
        "dubbo_services": dubbo_services,
        "facade_or_service_interface": is_facade,
    }


def scan(root: Path, keyword: str | None) -> list[dict]:
    ignored = {".git", "target", "build", "node_modules", ".idea"}
    results: list[dict] = []
    for path in root.rglob("*.java"):
        if any(part in ignored for part in path.parts):
            continue
        item = scan_file(path, keyword)
        if item:
            results.append(item)
    return results


def render_markdown(items: list[dict]) -> str:
    lines = ["# Java Interface Inventory", ""]
    for item in items:
        lines.append(f"## {item['type'] or Path(item['path']).name}")
        lines.append("")
        if item["package"]:
            lines.append(f"- Package: `{item['package']}`")
        lines.append(f"- Source: `{item['path']}`")
        if item["facade_or_service_interface"]:
            lines.append("- Interface candidate: yes")
        if item["http"]:
            lines.append("")
            lines.append("### HTTP mappings")
            for entry in item["http"]:
                prefix = f" class `{entry.get('class_mapping')}` +" if entry.get("class_mapping") else ""
                lines.append(
                    f"- L{entry['line']}: `{entry['annotation']}`{prefix} signature `{entry['signature']}`"
                )
        if item["dubbo_services"]:
            lines.append("")
            lines.append("### Dubbo services")
            for entry in item["dubbo_services"]:
                lines.append(f"- L{entry['line']}: `{entry['annotation']}` -> `{entry['signature']}`")
        if item["dubbo_references"]:
            lines.append("")
            lines.append("### Dubbo references")
            for entry in item["dubbo_references"]:
                lines.append(f"- L{entry['line']}: `{entry['annotation']}` -> `{entry['signature']}`")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan Java project HTTP and Dubbo interface entry points.")
    parser.add_argument("--root", required=True, help="Project root to scan")
    parser.add_argument("--keyword", help="Optional keyword to narrow files")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    items = scan(root, args.keyword)
    if args.format == "json":
        print(json.dumps(items, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
