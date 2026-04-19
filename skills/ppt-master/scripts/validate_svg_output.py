#!/usr/bin/env python3
"""
PPT Master - SVG Output Pre-Finalize Validator

Validates svg_output/*.svg before running finalize_svg.py. Catches the common
failure modes we've seen in real projects:

  1. UTF-8 decode errors caused by the Cursor `Write` tool encoding some CJK
     characters / `\u00b7` as Latin-1 single bytes. See
     docs/lessons/cursor-write-latin1-bug.md.
  2. XML well-formedness errors (unescaped `&`, mismatched tags such as
     `<text>...</tspan>`).
  3. Orphan Latin-1 bytes that WOULD decode but strongly suggest the Write-tool
     corruption pattern.
  4. Tag-mismatch heuristic (line-level `<text>...</tspan>` or `<tspan>...</text>`)
     that produces subtle rendering issues even when XML parses.

Usage:
    python3 scripts/validate_svg_output.py <project_path>
    python3 scripts/validate_svg_output.py <project_path> --dir svg_output
    python3 scripts/validate_svg_output.py <project_path> --strict
    python3 scripts/validate_svg_output.py <single_svg_file>

Exit codes:
    0  all files pass
    1  at least one file has ENCODING or XML failure (hard error)
    2  usage / path error
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

# Suspicious orphan Latin-1 bytes. These are valid Latin-1 single bytes that
# would decode OK under latin-1, but in UTF-8 context they're either invalid
# or indicate the Cursor Write-tool corruption pattern.
#
# - 0xB7 orphan  (middle dot when not preceded by 0xC2) -> Write bug signature
# - 0xC0 / 0xC1 start bytes -> always invalid UTF-8 start bytes
# - 0xF5-0xFF                -> never valid UTF-8 start bytes

RE_TEXT_TSPAN_MISMATCH = re.compile(
    r"<text\b[^>]*>(?:(?!</text>)[^<])*</tspan>", re.DOTALL
)
RE_TSPAN_TEXT_MISMATCH = re.compile(
    r"<tspan\b[^>]*>(?:(?!</tspan>)[^<])*</text>", re.DOTALL
)
RE_BARE_AMP = re.compile(r"&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9A-Fa-f]+;)")


# ---------------------------------------------------------------------------
# Report datatypes
# ---------------------------------------------------------------------------


@dataclass
class FileReport:
    path: pathlib.Path
    encoding_ok: bool = True
    xml_ok: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.encoding_ok and self.xml_ok and not self.errors


# ---------------------------------------------------------------------------
# Checkers
# ---------------------------------------------------------------------------


def check_utf8(raw: bytes, report: FileReport) -> str | None:
    """Return decoded text if OK, else None and annotate report."""
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        report.encoding_ok = False
        start = max(0, exc.start - 12)
        end = min(len(raw), exc.end + 12)
        snippet = raw[start:end]
        hex_ctx = snippet.hex(" ")
        report.errors.append(
            f"[ENCODING] UTF-8 decode failed at byte {exc.start}: "
            f"{exc.reason!s}. Context bytes (hex): {hex_ctx}. "
            f"Likely cause: Cursor `Write` tool wrote CJK / `\u00b7` as "
            f"Latin-1. Remedy: delete this file and regenerate via Python "
            f"heredoc (see references/shared-standards.md \u00a70)."
        )
        return None


def check_suspicious_bytes(raw: bytes, report: FileReport) -> None:
    """Even if UTF-8 decoding passes, flag bytes that SHOULD NOT appear."""
    for idx, byte in enumerate(raw):
        if byte in (0xC0, 0xC1):
            report.warnings.append(
                f"[SUSPECT] 0x{byte:02x} at byte {idx} — not a legal UTF-8 start byte. "
                "File may contain latent corruption."
            )
            break
    for idx in range(0xF5, 0x100):
        if bytes([idx]) in raw:
            pos = raw.index(bytes([idx]))
            report.warnings.append(
                f"[SUSPECT] 0x{idx:02x} at byte {pos} — never a legal UTF-8 start byte."
            )
            break


def check_xml(path: pathlib.Path, report: FileReport) -> None:
    try:
        ET.parse(str(path))
    except ET.ParseError as exc:
        report.xml_ok = False
        report.errors.append(
            f"[XML] not well-formed: {exc}. "
            "Common causes: bare `&` instead of `&amp;`, or `<text>...</tspan>` tag mismatch."
        )


def check_text_tspan(text: str, report: FileReport) -> None:
    mismatches: list[tuple[int, str]] = []
    for match in RE_TEXT_TSPAN_MISMATCH.finditer(text):
        line_no = text.count("\n", 0, match.start()) + 1
        mismatches.append(
            (line_no, match.group(0)[:80].replace("\n", " "))
        )
    for match in RE_TSPAN_TEXT_MISMATCH.finditer(text):
        line_no = text.count("\n", 0, match.start()) + 1
        mismatches.append(
            (line_no, match.group(0)[:80].replace("\n", " "))
        )
    if mismatches:
        formatted = "; ".join(f"line {line}: `{snippet}...`" for line, snippet in mismatches[:3])
        more = f" (+{len(mismatches) - 3} more)" if len(mismatches) > 3 else ""
        report.errors.append(
            f"[TAG_MISMATCH] `<text>...</tspan>` or `<tspan>...</text>` "
            f"pattern detected: {formatted}{more}. Likely a string-literal typo "
            f"when the SVG was generated; fix by replacing the mismatched "
            f"closing tag."
        )


def check_bare_amp(text: str, report: FileReport) -> None:
    findings: list[tuple[int, str]] = []
    for match in RE_BARE_AMP.finditer(text):
        line_no = text.count("\n", 0, match.start()) + 1
        snippet = text[max(0, match.start() - 10) : match.start() + 15].replace("\n", " ")
        findings.append((line_no, snippet))
    if findings:
        formatted = "; ".join(f"line {line}: `{snippet}`" for line, snippet in findings[:3])
        more = f" (+{len(findings) - 3} more)" if len(findings) > 3 else ""
        report.errors.append(
            f"[AMP] Unescaped `&` detected: {formatted}{more}. "
            "Replace with `&amp;` in SVG/XML content."
        )


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def validate_file(path: pathlib.Path, strict: bool = False) -> FileReport:
    report = FileReport(path=path)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        report.errors.append(f"[IO] cannot read: {exc}")
        report.encoding_ok = False
        return report

    text = check_utf8(raw, report)
    check_suspicious_bytes(raw, report)

    if text is not None:
        check_xml(path, report)
        check_text_tspan(text, report)
        check_bare_amp(text, report)

    if strict and report.warnings:
        report.errors.extend(f"[STRICT] {w}" for w in report.warnings)
        report.warnings = []
    return report


def collect_targets(arg: pathlib.Path, sub: str) -> list[pathlib.Path]:
    if arg.is_file():
        return [arg]
    svg_dir = arg / sub if (arg / sub).is_dir() else arg
    return sorted(svg_dir.glob("*.svg"))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate SVG output before finalize_svg.py (UTF-8 + XML + tag heuristics)."
    )
    parser.add_argument("path", help="Project directory or single SVG file")
    parser.add_argument(
        "--dir",
        default="svg_output",
        help="Subdirectory to scan when path is a project dir (default: svg_output)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat suspicious-byte warnings as errors",
    )
    args = parser.parse_args(argv)

    root = pathlib.Path(args.path).expanduser().resolve()
    if not root.exists():
        print(f"[ERROR] path not found: {root}", file=sys.stderr)
        return 2

    targets = collect_targets(root, args.dir)
    if not targets:
        print(f"[WARN] no SVG files found under {root}", file=sys.stderr)
        return 0

    reports: list[FileReport] = [validate_file(p, strict=args.strict) for p in targets]

    print(f"PPT Master :: SVG pre-finalize validator")
    print(f"target     : {root}")
    print(f"files      : {len(reports)}")
    print("-" * 72)

    passed = sum(1 for r in reports if r.passed)
    hard_fail = [r for r in reports if not r.passed]
    with_warn = [r for r in reports if r.passed and r.warnings]

    for report in reports:
        status = "PASS"
        if not report.encoding_ok:
            status = "FAIL (encoding)"
        elif not report.xml_ok:
            status = "FAIL (xml)"
        elif report.errors:
            status = "FAIL"
        elif report.warnings:
            status = "WARN"
        print(f"  [{status:14s}] {report.path.name}")
        for err in report.errors:
            print(f"     - {err}")
        for warn in report.warnings:
            print(f"     ~ {warn}")

    print("-" * 72)
    print(f"summary    : {passed}/{len(reports)} passed, "
          f"{len(hard_fail)} failed, {len(with_warn)} warn-only")

    if hard_fail:
        print()
        print("NEXT STEPS for encoding failures:")
        print("  1. DO NOT attempt `latin-1 -> utf-8` conversion to repair the files.")
        print("  2. `rm` the failing files.")
        print("  3. Regenerate via Python heredoc (see references/shared-standards.md \u00a70,")
        print("     or docs/lessons/cursor-write-latin1-bug.md).")
        print("  4. Re-run this validator; it must show 0 failures before finalize_svg.py.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
