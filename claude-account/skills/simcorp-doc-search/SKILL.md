---
name: simcorp-doc-search
description: "Search Dan's SimCorp consulting documentation corpus on his Mac: 5,982 indexed documents across vendor manuals, Nicola client files, config exports and his own output. Use whenever a SimCorp field, window, service, parameter or manual section needs grounding."
---

# SimCorp documentation search

A full text index over Dan's consulting corpus, so any claim about SimCorp Dimension can be traced to the document it came from instead of being reasoned from plausibility. A full rescan takes about 20 seconds once built. A search returns in about a second.

## Where everything lives

```
ROOT="$HOME/mnt/01 Work & Business/a. Consulting - SimCorp"      # inside device_bash
```

On the Mac itself that is `/Users/danieldeenik/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business/a. Consulting - SimCorp`. It is iCloud Drive, not Documents.

```
$ROOT/_corpus_index/bin/build_index.py    the indexer
$ROOT/_corpus_index/bin/search_corpus.py  the search helper
$ROOT/_corpus_index/text/<mirrored path>.txt   extracted text, mirrors the source tree
$ROOT/_corpus_index/manifest.tsv          path, mtime, bytes, status, tier
$ROOT/_corpus_index/build.log             extraction failures
```

## Getting access

The folder is not connected by default. Request it once per session:

```
device_request_folder_access
  paths:  ["/Users/danieldeenik/Library/Mobile Documents/com~apple~CloudDocs/01 Work & Business"]
```

Three access facts that will otherwise waste a lot of time:

1. Dan's local **Filesystem MCP server does not work in Cowork**. Its tools declare JSON Schema draft-07, which the client rejects. Use `device_bash` for everything.
2. **`device_commit_files` reports success but iCloud does not serve the new bytes back to the mount.** A script written that way stays stale. Write files with `device_bash` and a heredoc, or `cp` from `$HOME`, then verify with `stat -c%s` before trusting it.
3. **Nothing can be backgrounded.** Each `device_bash` call runs in its own PID namespace with die-with-parent, so `nohup` dies when the call returns. Use `BUDGET_SECONDS` and `SHARD` instead.

## Refresh the index before searching

Always do this first. It is cheap when nothing changed, and it is the difference between searching the corpus and searching a stale snapshot.

```bash
R="$HOME/mnt/01 Work & Business/a. Consulting - SimCorp"
for i in 0 1 2 3 4 5; do
  SHARD=$i/6 BUDGET_SECONDS=110 python3 "$R/_corpus_index/bin/build_index.py" "$R" 2>/dev/null &
done
wait
```

Six shards at a 110 second budget fits inside the call timeout. Repeat until every shard reports `pending 0`. A full cold build is roughly eight passes. Merge the shard manifests when done:

```bash
python3 - <<'PY'
import glob, os
R = os.path.expanduser("~/mnt/01 Work & Business/a. Consulting - SimCorp/_corpus_index")
rows = {}
for f in glob.glob(os.path.join(R, "manifest.*.tsv")):
    for line in open(f):
        if not line.startswith("path\t"): rows[line.split("\t")[0]] = line
with open(os.path.join(R, "manifest.tsv"), "w") as out:
    out.write("path\tmtime\tbytes\tstatus\ttier\n")
    for k in sorted(rows): out.write(rows[k])
print("rows", len(rows))
PY
```

## Search

```bash
R="$HOME/mnt/01 Work & Business/a. Consulting - SimCorp"
S="$R/_corpus_index/bin/search_corpus.py"

python3 "$S" "Restrict order types to Order Manager" --root "$R" --tier tier1
python3 "$S" "Data Store" --root "$R" --tier tier1 --path foconfig --context 3
python3 "$S" "MDV" --root "$R" --tier tier3 --files
python3 "$S" "omwsdatastorehostnames" --root "$R" --max 10
```

Flags: `--tier` filters by tier, `--path` filters on the source path, `--ext` on the source extension, `--context N` adds surrounding lines, `--files` lists matching documents only, `--max N` caps hits. Every hit prints its tier, the real source file and the line number in the extracted text.

## Tiers, and the rule that matters most

| Tier | What it is | Count | How to treat it |
|---|---|---|---|
| tier1-vendor-manual | SimCorp's own PDFs in `ii. Manuals & Documentation/PDFs` | 139 | Authoritative. Cite by section and page. |
| tier2-reference | Copies, extracts and staged text of the same manuals | 918 | Same content, uncertain vintage. Confirm against tier1 before quoting. |
| tier3-client | Nicola files under `i. Client - Nicola Wealth`, `vi. Config & Architecture`, `iv. SQL & Scripts` | 4,487 | How Nicola configured things. An assertion about this installation, never vendor truth. |
| tier4-derived | Training modules, presentations, `ix. SimCorp SuperAgent` | 438 | Dan's own prior output. Context only. Never a source. |

**Never cite tier3 or tier4 as if it were documentation.** Dan's house rule is that structure comes from manuals or verified client config, and anything else is marked open. A hit in his own earlier analysis is not evidence that the analysis was right.

**Deduplicate.** The same manual appears several times: in `PDFs/`, under `Reference/Db-Schema-.../`, inside `_stage/` folders, and as extracted markdown under the client tree. Five hits on one sentence usually means one source. Prefer the tier1 copy.

## Check the edition before quoting

Editions vary by nearly twenty years and the installation is 26.04. Always read the edition line near the top of the extracted text before citing.

| File | Manual | Edition |
|---|---|---|
| foconfig | Front Office Configuration | September 2025 |
| foops | Front Office Operations | September 2025 |
| srvicad | Service Administration | March 2026 |
| srvicconf | Service Configuration | March 2026 |
| sysmn | System Maintenance | March 2026 |
| cmmgr | Compliance Manager | March 2026 |
| cmrbg | Compliance Manager Rule Building Guide | September 2025 |
| dataextr | Data Extractor | March 2026 |
| ssam | System Administrator's Manual | September 2025 |
| copyscd | Copying SimCorp Dimension | September 2025 |
| privdebt | Private Debt, Loan facilities | March 2026 |
| amgsg, amcv, amfx, amacf, amscn | Asset Manager family | September 2025 |
| omgsg | Order Manager Getting Started | December 2023 |
| cashman | Cash Management | January 2012 |
| marktdat | Market Data | February 2009 |
| refdata | Reference Data | March 2009 |
| modlling | Modelling Structures | March 2008 |
| sysoptns | System Options | October 2006 |

The last five are old enough that a window or field described there may no longer exist. Say so rather than quoting them flat.

## Known extraction failures

Nineteen files do not extract. All of them are Office lock files beginning `~$`, plus a handful of large or malformed workbooks and decks. Nothing load bearing. `$ROOT/_corpus_index/build.log` names them. Do not treat a missing document as an absent fact without checking that log.

## What the index does not cover

Images, screenshots, zip archives, JavaScript and TypeScript sources, and anything under `node_modules`, `.git` or `_to_delete`. Screenshots are a real gap: much of Dan's PROD evidence is PNG, and no text search will find it.

## Regenerating the scripts

If `bin/` is missing, or `grep -c hashlib bin/build_index.py` returns 0 (the pre-sharding version), rewrite it. Write with a `device_bash` heredoc, never `device_commit_files`.

`build_index.py` contract: walk the root, skip `SKIP_DIRS`, take `.md .txt .csv .json .xml .xslt .xsl .cei .sql .yml .yaml .html .htm .log .ini .cfg .tsv .local .apl` directly and extract `.pdf .docx .pptx .xlsx`; PDFs through `pdftotext -layout`, docx and pptx by unzipping the document XML and stripping tags, xlsx through `openpyxl` read-only capped at 2000 rows per sheet; write each result to `text/<relative path>.txt`; skip any file whose extracted text is newer than its source; honour `BUDGET_SECONDS` by marking the remainder `pending`; honour `SHARD="i/N"` by taking only files whose md5 modulo N equals i, and write to `manifest.<i>.tsv`; cap output at 4 MB per file; catch every extraction error, count it, log it, and carry on.

`search_corpus.py` contract: load `manifest.tsv` into a path to tier map, run `rg -i --no-heading --line-number` over `text/`, map each hit back to its source path by stripping the index prefix and the `.txt` suffix, apply the `--tier`, `--path` and `--ext` filters, and print tier, source path, line number and the matching line.

## Scope

This skill finds and cites documents. Interpreting Order Manager runtime behaviour belongs to `simcorp-om-runtime-triage`, the service platform to `simcorp-service-platform`, compliance rule design to `simcorp-compliance-rules`, and flow mapping with measured overlays to `simcorp-fo-flow-architect`. Search first, then hand the citations to the skill that owns the domain.