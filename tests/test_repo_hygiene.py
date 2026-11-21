"""Repository hygiene: ASCII-safe sources, no typographic dashes, no local paths."""

import re
import subprocess

from conftest import ROOT

TEXT_SUFFIXES = {".py", ".js", ".mjs", ".md", ".json", ".txt", ".toml", ".cfg", ".yml", ".yaml", ".example", ""}
SKIP_DIRS = {".git", "runs", "release-assets", ".pytest_cache", "__pycache__", ".venv", "venv"}
DASHES = ("\u2013", "\u2014")
LOCAL_PATH = re.compile(r"[A-Za-z]:[\\/]+(Users|Program Files)|/home/[a-z]+/|/Users/[A-Za-z]+/")


def repo_files():
    try:
        out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.split()
        return [ROOT / p for p in out]
    except (OSError, subprocess.CalledProcessError):
        return [p for p in ROOT.rglob("*") if p.is_file() and not SKIP_DIRS & set(p.relative_to(ROOT).parts)]


def text_files():
    for p in repo_files():
        if p.suffix in TEXT_SUFFIXES and p.exists() and not SKIP_DIRS & set(p.relative_to(ROOT).parts):
            yield p


def test_no_en_or_em_dashes_anywhere():
    bad = [str(p.relative_to(ROOT)) for p in text_files() if any(d in p.read_text(encoding="utf-8", errors="replace") for d in DASHES)]
    assert bad == []


def test_no_local_paths():
    bad = [str(p.relative_to(ROOT)) for p in text_files() if LOCAL_PATH.search(p.read_text(encoding="utf-8", errors="replace"))]
    assert bad == []


def test_python_and_js_sources_are_ascii():
    for p in text_files():
        if p.suffix in (".py", ".js", ".mjs"):
            assert p.read_text(encoding="utf-8").isascii(), p
