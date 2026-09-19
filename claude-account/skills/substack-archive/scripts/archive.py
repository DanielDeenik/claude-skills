#!/usr/bin/env python3
"""Maintain a local PDF archive of Substack publications you subscribe to.

Usage:
    python archive.py add <publication-url>
    python archive.py sync [publication-url]
    python archive.py status
"""

import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from playwright.sync_api import sync_playwright

CONFIG_PATH = Path.home() / ".substack-archive" / "config.json"


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())

    print("No config found. Paste the value of your 'substack.sid' cookie.")
    print("(Chrome DevTools > Application > Cookies > https://substack.com)")
    sid = input("substack.sid: ").strip()
    config = {
        "sid": sid,
        "output_dir": "~/Documents/SubstackArchive",
        "publications": [],
    }
    save_config(config)
    return config


def save_config(config):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2))
    CONFIG_PATH.chmod(0o600)


def outdir_for(config, base_url):
    host = urlparse(base_url).hostname
    d = Path(config["output_dir"]).expanduser() / host
    d.mkdir(parents=True, exist_ok=True)
    return d


def fetch_post_list(base_url):
    """Page through Substack's archive endpoint until it returns nothing."""
    posts = []
    offset = 0
    while True:
        r = requests.get(
            f"{base_url}/api/v1/archive",
            params={"sort": "new", "limit": 50, "offset": offset},
            timeout=30,
        )
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        for post in batch:
            posts.append({
                "date": post["post_date"][:10],
                "title": post["title"],
                "url": post["canonical_url"],
            })
        offset += len(batch)
        time.sleep(0.5)
    return posts


def filename_for(post):
    slug = re.sub(r"[^\w\s-]", "", post["title"]).strip()
    slug = re.sub(r"[\s_]+", "-", slug)[:80]
    return f"{post['date']}_{slug}.pdf"


def download(config, base_url):
    outdir = outdir_for(config, base_url)
    host = urlparse(base_url).hostname

    print(f"\n{host}: fetching post list...")
    posts = fetch_post_list(base_url)
    pending = [p for p in posts if not (outdir / filename_for(p)).exists()]
    print(f"{len(posts)} posts, {len(pending)} to download")

    if not pending:
        return 0, []

    failures = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        context.add_cookies([
            {"name": "substack.sid", "value": config["sid"], "domain": d, "path": "/"}
            for d in {".substack.com", f".{host}"}
        ])
        page = context.new_page()

        for i, post in enumerate(pending, 1):
            try:
                page.goto(post["url"], wait_until="networkidle", timeout=60000)
                page.pdf(
                    path=str(outdir / filename_for(post)),
                    format="A4",
                    margin={"top": "15mm", "bottom": "15mm",
                            "left": "12mm", "right": "12mm"},
                    print_background=True,
                )
                print(f"  [{i}/{len(pending)}] {post['title']}")
            except Exception as e:
                failures.append(post["title"])
                print(f"  [{i}/{len(pending)}] FAILED {post['title']}: {e}")
            time.sleep(1)

        browser.close()

    return len(pending) - len(failures), failures


def cmd_add(config, url):
    url = url.rstrip("/")
    if url not in config["publications"]:
        config["publications"].append(url)
        save_config(config)
    saved, failures = download(config, url)
    report([(url, saved, failures)], config)


def cmd_sync(config, url=None):
    targets = [url.rstrip("/")] if url else config["publications"]
    if not targets:
        print("No publications tracked. Use: archive.py add <url>")
        return
    results = [(t, *download(config, t)) for t in targets]
    report(results, config)


def cmd_status(config):
    root = Path(config["output_dir"]).expanduser()
    print(f"Archive: {root}\n")
    if not config["publications"]:
        print("No publications tracked.")
        return
    for url in config["publications"]:
        host = urlparse(url).hostname
        count = len(list((root / host).glob("*.pdf"))) if (root / host).exists() else 0
        print(f"  {host}: {count} posts")


def report(results, config):
    total = sum(r[1] for r in results)
    all_failures = [f for r in results for f in r[2]]
    print(f"\nSaved {total} new posts to {Path(config['output_dir']).expanduser()}")
    if all_failures:
        print(f"{len(all_failures)} failed (re-run sync to retry):")
        for title in all_failures:
            print(f"  {title}")


def main():
    args = sys.argv[1:]
    if not args or args[0] not in {"add", "sync", "status"}:
        print(__doc__)
        sys.exit(1)

    config = load_config()
    cmd = args[0]

    if cmd == "add":
        if len(args) < 2:
            print("Usage: archive.py add <publication-url>")
            sys.exit(1)
        cmd_add(config, args[1])
    elif cmd == "sync":
        cmd_sync(config, args[1] if len(args) > 1 else None)
    else:
        cmd_status(config)


if __name__ == "__main__":
    main()
