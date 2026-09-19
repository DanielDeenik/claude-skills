---
name: substack-archive
description: Download and maintain a local offline archive of Substack publications the user subscribes to, saving each post as a PDF. Handles paywalled posts using the user's own session cookie, tracks multiple publications, and syncs incrementally so re-runs only fetch new posts. Use this skill whenever the user mentions archiving, backing up, downloading, scraping, or saving Substack posts or newsletters, wants offline copies of a newsletter they pay for, asks to "grab everything from" a Substack, or wants to add a new publication to their archive or refresh an existing one. Also use when the user asks what is in their newsletter archive or which publications are being tracked.
---

# Substack Archive

Maintains a local PDF archive of Substack publications the user subscribes to.

Scope: personal offline archiving of content the user has legitimate access to. Do not use this to bulk-collect publications the user does not subscribe to, and do not help repackage or redistribute the output.

## Prerequisites

Check these before the first run:

```bash
pip install playwright requests
playwright install chromium
```

## Configuration

State lives in `~/.substack-archive/config.json`:

```json
{
  "sid": "session cookie value",
  "output_dir": "~/Documents/SubstackArchive",
  "publications": ["https://example.substack.com"]
}
```

If the file does not exist, `archive.py` creates it on first run and prompts for the session cookie.

### Getting the session cookie

The cookie authenticates paywalled posts. Walk the user through this if `sid` is missing or expired:

1. Open any Substack post in Chrome while logged in
2. DevTools (Cmd+Opt+I) then Application, Cookies, `https://substack.com`
3. Copy the value of the cookie named `substack.sid`

Cookies expire. If PDFs come back truncated at the paywall boundary, the cookie is stale and needs replacing.

## Commands

Add a publication and download its full archive:

```bash
python scripts/archive.py add https://example.substack.com
```

Sync every tracked publication, fetching only posts not already saved:

```bash
python scripts/archive.py sync
```

Sync one publication:

```bash
python scripts/archive.py sync https://example.substack.com
```

List tracked publications and post counts on disk:

```bash
python scripts/archive.py status
```

## How it works

Post URLs come from Substack's own archive endpoint (`/api/v1/archive`), paged 50 at a time, rather than HTML scraping. Each post is then rendered to PDF in headless Chromium with the session cookie attached, so paid content resolves.

Files land at `<output_dir>/<publication-host>/YYYY-MM-DD_post-title.pdf`. Existing files are skipped, which makes `sync` safe to re-run on a schedule.

## Handling problems

- **Truncated PDFs stopping at a subscribe prompt**: stale or wrong cookie. Re-copy `substack.sid`.
- **Empty post list**: publication uses a custom domain. Pass the custom domain, not the `*.substack.com` alias, since the archive endpoint lives on the canonical host.
- **Individual post failures**: the script logs and continues. Re-run `sync` to retry only the ones that failed, since successful files are skipped.
- **Rate limiting**: the script sleeps between requests. If the publication still throttles, raise the delay in `archive.py`.

## Reporting back

After a run, tell the user how many posts were newly saved, how many were skipped, and the output path. If any posts failed, list their titles rather than dumping stack traces.
