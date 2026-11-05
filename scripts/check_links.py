#!/usr/bin/env python3
"""Check every link in data/projects.yml.

Exit code 1 only for hard failures (404 / 410). Anything else — rate limits,
403s from bot filtering, timeouts — is reported as a warning, because those are
the usual false positives in CI.

Usage:
    python3 scripts/check_links.py [--jobs 8] [--timeout 15]
"""

from __future__ import annotations

import argparse
import concurrent.futures
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "projects.yml"
UA = "awesome-esp32-s3-nano link checker (+https://github.com/)"

def ssl_context() -> "ssl.SSLContext":
    """Prefer certifi: stock macOS/Windows Pythons often ship without a CA bundle."""
    try:
        import certifi
    except ImportError:
        return ssl.create_default_context()
    return ssl.create_default_context(cafile=certifi.where())


CTX = ssl_context()


def load_repos() -> list[str]:
    import yaml

    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    return [p["repo"] for p in data["projects"]]


def check(url: str, timeout: int) -> tuple[str, str, str]:
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
            return url, "ok", str(resp.status)
    except urllib.error.HTTPError as exc:
        return url, "http", str(exc.code)
    except Exception as exc:  # noqa: BLE001 - network errors are all "warn"
        return url, "error", type(exc).__name__


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=15)
    args = ap.parse_args()

    urls = [f"https://github.com/{r}" for r in load_repos()]
    hard: list[str] = []
    warn: list[str] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for url, kind, detail in pool.map(lambda u: check(u, args.timeout), urls):
            if kind == "ok":
                continue
            if kind == "http" and detail in ("404", "410"):
                hard.append(f"{url} -> {detail}")
            else:
                warn.append(f"{url} -> {kind}:{detail}")

    for line in hard:
        print(f"FAIL {line}")
    for line in warn:
        print(f"WARN {line}")

    print(f"\nchecked {len(urls)} links: {len(hard)} failed, {len(warn)} warnings")
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
