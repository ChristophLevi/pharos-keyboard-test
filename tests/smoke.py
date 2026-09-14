#!/usr/bin/env python3
"""Dependency-free static smoke checks for pharos-keyboard-test."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "dist" / "index.html"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


html = HTML_PATH.read_text(encoding="utf-8")

required = [
    '<html lang="zh-CN">',
    "<title>pharos-keyboard-test</title>",
    'id="keyboard"',
    'id="focusButton"',
    'id="resetButton"',
    'data-mode="win"',
    'data-mode="mac"',
    "navigator.keyboard.lock",
    "requestFullscreen",
    "event.code",
]

for marker in required:
    if marker not in html:
        fail(f"missing required marker: {marker}")

if re.search(r'<(?:script|link|img)[^>]+(?:src|href)="https?://', html):
    fail("unexpected external asset reference")

for code in ("Numpad0", "Numpad9", "NumpadEnter", "Insert", "PageDown", "AudioVolumeMute"):
    if f"code: '{code}'" not in html:
        fail(f"missing full-layout key: {code}")

legend_values = re.findall(r"(?:win|mac): '([^']*)'", html)
if any(re.search(r"[\u4e00-\u9fff]", legend) for legend in legend_values):
    fail("Chinese characters found in keyboard legends")

if html.count("{ code: '") < 80:
    fail("key definition count is unexpectedly low")

if "event.repeat" not in html and "pressed.has(code)" not in html:
    fail("repeat-event guard is missing")

if "window.addEventListener('blur'" not in html:
    fail("blur cleanup is missing")

print("PASS: pharos-keyboard-test static smoke checks")
print(f"PASS: {HTML_PATH.relative_to(ROOT)} ({len(html.encode('utf-8'))} bytes)")
