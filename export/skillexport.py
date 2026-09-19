#!/usr/bin/env python3
"""skillexport: build, scan, index and verify the claude-skills repository.

Subcommands
  cloud   copy Claude account skills and installed plugins from a Cowork sync cache
  mac     copy the skill sources listed in a sources file from a local root folder
  scan    scan the repository for credentials (values are always masked in output)
  index   write README.md, EXPORT_REPORT.md and MANIFEST.sha256
  verify  check every file against the source-side checksums and MANIFEST.sha256

Every location is passed on the command line. Nothing about the machine is assumed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

GENERATED = {"README.md", "EXPORT_REPORT.md", "MANIFEST.sha256", ".gitignore"}
EXPORT_DIR = "export"
CHECKSUM_DIR = "export/checksums"
SKILL_FILE = "SKILL.md"
PACKAGE_SUFFIX = ".skill"


# ----------------------------------------------------------------------------- helpers
def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def iso_mtime(ts: float) -> str:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def entry_hash(p: Path) -> str:
    if p.is_symlink():
        return hashlib.sha256(("symlink:" + os.readlink(p)).encode()).hexdigest()
    return sha256_file(p)


def load_patterns(path: str | None) -> list[str]:
    pats: list[str] = []
    if path:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                pats.append(line)
    return pats


def matches(name: str, is_dir: bool, patterns: list[str]) -> str | None:
    for pat in patterns:
        if pat.endswith("/"):
            if is_dir and fnmatch.fnmatch(name, pat[:-1]):
                return pat
        elif fnmatch.fnmatch(name, pat):
            return pat
    return None


def repo_files(repo: Path) -> list[Path]:
    out = []
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        dp = Path(dirpath)
        for d in list(dirnames):
            if (dp / d).is_symlink():
                out.append(dp / d)
        for fn in sorted(filenames):
            out.append(dp / fn)
    return sorted(out)


def rel(repo: Path, p: Path) -> str:
    return p.relative_to(repo).as_posix()


def write_json(p: Path, data) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=1, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8")


def read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


# ----------------------------------------------------------------------------- copying
class Copier:
    """Copies files into the repo, hashing the source and the copy, recording what was skipped."""

    def __init__(self, repo: Path, patterns: list[str], display_base: Path, display_name: str):
        self.repo = repo
        self.patterns = patterns
        self.display_base = display_base
        self.display_name = display_name
        self.files: dict[str, str] = {}
        self.mtimes: dict[str, str] = {}
        self.bytes = 0
        self.excluded: list[dict] = []
        self.broken_symlinks: list[dict] = []
        self.dereferenced: list[dict] = []
        self.errors: list[str] = []

    def show(self, p: Path) -> str:
        """Path as recorded in the export: relative to the named source root, never a machine path."""
        try:
            return f"{self.display_name}/{p.relative_to(self.display_base).as_posix()}"
        except ValueError:
            return f"{self.display_name}/{p.name}"

    def _copy_file(self, s: Path, d: Path, src_root: Path) -> None:
        key = rel(self.repo, d)
        d.parent.mkdir(parents=True, exist_ok=True)
        if s.is_symlink():
            target = os.readlink(s)
            try:
                real = s.resolve(strict=True)
                valid = real.exists() and real != s.absolute()
            except (OSError, RuntimeError):
                valid, real = False, None
            if not valid:
                self.broken_symlinks.append({"repo_path": key, "source": self.show(s), "target": target})
                return
            root_real = src_root.resolve()
            inside = str(real).startswith(str(root_real) + os.sep) or real == root_real
            if inside:
                if d.exists() or d.is_symlink():
                    d.unlink()
                os.symlink(target, d)
                self.files[key] = entry_hash(d)
                self.mtimes[key] = iso_mtime(s.lstat().st_mtime)
                return
            # link points outside the source: store the content it points to
            self.dereferenced.append({"repo_path": key, "source": self.show(s), "target": target})
            s = real
        src_hash = sha256_file(s)
        shutil.copy2(s, d)
        dst_hash = sha256_file(d)
        if src_hash != dst_hash:
            self.errors.append(f"hash mismatch after copy: {self.show(s)}")
        self.files[key] = src_hash
        self.mtimes[key] = iso_mtime(s.stat().st_mtime)
        self.bytes += d.stat().st_size

    def copy(self, src: Path, dst: Path) -> dict:
        before = len(self.files)
        before_bytes = self.bytes
        if src.is_dir() and not src.is_symlink():
            for dirpath, dirnames, filenames in os.walk(src):
                dp = Path(dirpath)
                relp = dp.relative_to(src)
                keep = []
                for dn in sorted(dirnames):
                    full = dp / dn
                    if full.is_symlink():
                        filenames.append(dn)
                        continue
                    pat = matches(dn, True, self.patterns)
                    if pat:
                        self.excluded.append({"source": self.show(full), "pattern": pat, "kind": "dir"})
                    else:
                        keep.append(dn)
                dirnames[:] = keep
                for fn in sorted(set(filenames)):
                    s = dp / fn
                    pat = matches(fn, False, self.patterns)
                    if pat:
                        self.excluded.append({"source": self.show(s), "pattern": pat, "kind": "file"})
                        continue
                    self._copy_file(s, dst / relp / fn, src)
        elif src.exists() or src.is_symlink():
            self._copy_file(src, dst, src.parent)
        else:
            self.errors.append(f"missing source: {self.show(src)}")
        return {"files": len(self.files) - before, "bytes": self.bytes - before_bytes}

    def write_part(self, part: str, meta: dict) -> None:
        cdir = self.repo / CHECKSUM_DIR
        cdir.mkdir(parents=True, exist_ok=True)
        lines = [f"{h}  {p}" for p, h in sorted(self.files.items())]
        (cdir / f"{part}.sha256").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        meta = dict(meta)
        meta.update({
            "part": part,
            "file_count": len(self.files),
            "bytes": self.bytes,
            "excluded": self.excluded,
            "broken_symlinks": self.broken_symlinks,
            "dereferenced_symlinks": self.dereferenced,
            "errors": self.errors,
            "source_mtimes": self.mtimes,
        })
        write_json(cdir / f"{part}.json", meta)


# ----------------------------------------------------------------------------- cloud
def cmd_cloud(a) -> int:
    repo = Path(a.repo)
    patterns = load_patterns(a.excludes)
    captured = utcnow()
    problems = 0

    sroot = Path(a.skills_root)
    man = read_json(sroot / "manifest.json")
    exclude_sources = set(a.exclude_source or [])
    skills = sorted(man.get("skills", []), key=lambda s: s["name"])
    exported = [s for s in skills if s.get("source") not in exclude_sources]
    left_out = [s for s in skills if s.get("source") in exclude_sources]
    missing = [s["name"] for s in exported if not (sroot / s["name"] / SKILL_FILE).is_file()]
    if missing:
        print("ERROR manifest entries without SKILL.md:", missing, file=sys.stderr)
        return 2
    listed = {s["name"] for s in skills}
    unlisted = sorted(d.name for d in sroot.iterdir() if d.is_dir() and not d.name.startswith(".") and d.name not in listed)
    staging = [p.name for p in sroot.iterdir() if p.name.startswith(".") and p.is_dir() and any(p.iterdir())]

    c = Copier(repo, patterns, sroot, "account-skill-sync")
    per_skill = []
    for s in exported:
        r = c.copy(sroot / s["name"], repo / "claude-account" / "skills" / s["name"])
        per_skill.append({"name": s["name"], "source": s.get("source"), "updatedAt": s.get("updatedAt"),
                          "skillId": s.get("skillId"), "files": r["files"], "bytes": r["bytes"]})
    filtered = {k: v for k, v in man.items() if k != "skills"}
    filtered["skills"] = exported
    write_json(repo / "claude-account" / "manifest.json", filtered)
    c.files["claude-account/manifest.json"] = sha256_file(repo / "claude-account" / "manifest.json")
    c.write_part("claude-account", {
        "label": "Skills synced to the Claude account",
        "captured_utc": captured,
        "rows": [{"dest": "claude-account/skills", "origin": "Claude account skill sync", "kind": "dir"}],
        "manifest_lastUpdated": man.get("lastUpdated"),
        "exclude_sources": sorted(exclude_sources),
        "left_out_by_source": [{"name": s["name"], "source": s.get("source")} for s in left_out],
        "unlisted_folders": unlisted,
        "nonempty_staging_dirs": staging,
        "skills": per_skill,
    })
    problems += len(c.errors) + len(unlisted) + len(staging)
    print(f"claude-account: exported {len(exported)} skills, left out {len(left_out)} by source, "
          f"{len(c.files)} files, {c.bytes} bytes, errors {len(c.errors)}, unlisted {unlisted}, staging {staging}")

    proot = Path(a.plugins_root)
    pman = read_json(proot / "manifest.json")
    c2 = Copier(repo, patterns, proot, "plugin-sync")
    plist = []
    for p in sorted(pman.get("plugins", []), key=lambda x: x["name"]):
        src = proot / p["name"]
        if not src.is_dir():
            c2.errors.append(f"plugin folder missing: {p['name']}")
            continue
        r = c2.copy(src, repo / "claude-plugins" / p["name"])
        skill_count = sum(1 for _ in src.rglob(SKILL_FILE))
        plist.append({"name": p["name"], "version": p.get("version"), "marketplaceName": p.get("marketplaceName"),
                      "updatedAt": p.get("updatedAt"), "files": r["files"], "bytes": r["bytes"], "skills": skill_count})
    write_json(repo / "claude-plugins" / "manifest.json", pman)
    c2.files["claude-plugins/manifest.json"] = sha256_file(repo / "claude-plugins" / "manifest.json")
    listed_p = {p["name"] for p in pman.get("plugins", [])}
    unlisted_p = sorted(d.name for d in proot.iterdir() if d.is_dir() and not d.name.startswith(".") and d.name not in listed_p)
    generation_copies, other_unlisted = [], []
    for u in unlisted_p:
        base = u.split("~", 1)[0]
        if "~" in u and base in listed_p:
            same = tree_signature(proot / u) == tree_signature(proot / base)
            generation_copies.append({"folder": u, "of": base, "identical": same})
            if not same:
                other_unlisted.append(u)
        else:
            other_unlisted.append(u)
    c2.write_part("claude-plugins", {
        "label": "Installed Claude plugins",
        "captured_utc": captured,
        "rows": [{"dest": "claude-plugins", "origin": "Claude plugin sync", "kind": "dir"}],
        "manifest_lastUpdated": pman.get("lastUpdated"),
        "plugins": plist,
        "cache_generation_copies": generation_copies,
        "unlisted_folders": other_unlisted,
        "not_copied_top_level_files": sorted(f.name for f in proot.iterdir() if f.is_file() and f.name != "manifest.json"),
    })
    problems += len(c2.errors) + len(other_unlisted)
    print(f"claude-plugins: {len(plist)} plugins, {len(c2.files)} files, {c2.bytes} bytes, errors {len(c2.errors)}, "
          f"cache generation copies {generation_copies}, other unlisted {other_unlisted}")
    return 1 if problems else 0


# ----------------------------------------------------------------------------- mac
def cmd_mac(a) -> int:
    root = Path(a.root)
    repo = Path(a.repo)
    patterns = load_patterns(a.excludes)
    captured = utcnow()
    rows = []
    for line in Path(a.sources).read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cols = line.split("\t")
        if len(cols) != 3:
            print(f"ERROR bad sources row: {line!r}", file=sys.stderr)
            return 2
        rows.append({"dest": cols[0].strip(), "source": cols[1].strip(), "kind": cols[2].strip()})
    parts: dict[str, list[dict]] = {}
    for r in rows:
        parts.setdefault(r["dest"].split("/")[0], []).append(r)
    if a.only_part:
        parts = {k: v for k, v in parts.items() if k in set(a.only_part)}
    problems = 0
    for part, prow in parts.items():
        c = Copier(repo, patterns, root, root.name)
        done = []
        for r in prow:
            src = root / r["source"]
            if r["kind"] == "dir" and not src.is_dir():
                c.errors.append(f"expected folder: {r['source']}")
                continue
            if r["kind"] == "file" and not src.is_file():
                c.errors.append(f"expected file: {r['source']}")
                continue
            res = c.copy(src, repo / r["dest"])
            skills = sum(1 for _ in src.rglob(SKILL_FILE)) if src.is_dir() else 0
            done.append({"dest": r["dest"], "origin": r["source"], "kind": r["kind"], "files": res["files"],
                         "bytes": res["bytes"], "skill_dirs_at_source": skills})
        c.write_part(part, {"label": part, "captured_utc": captured, "root_name": root.name, "rows": done})
        problems += len(c.errors)
        print(f"{part}: {len(c.files)} files, {c.bytes} bytes, excluded {len(c.excluded)}, broken symlinks {len(c.broken_symlinks)}, errors {c.errors}")

    if a.completeness:
        listed = [root / r["source"] for r in rows]
        unlisted = []
        for dirpath, dirnames, filenames in os.walk(root):
            dp = Path(dirpath)
            dirnames[:] = [d for d in dirnames if not matches(d, True, patterns)]
            if any(dp == l or l in dp.parents for l in listed if l.is_dir()):
                dirnames[:] = []
                continue
            for fn in filenames:
                p = dp / fn
                if fn == SKILL_FILE or fn.endswith(PACKAGE_SUFFIX):
                    if not any(p == l or l in p.parents for l in listed):
                        unlisted.append(str(p.relative_to(root)))
        write_json(repo / CHECKSUM_DIR / "mac-completeness.json", {"root_name": root.name, "checked_utc": utcnow(), "unlisted_skill_items": sorted(unlisted), "excluded_patterns": patterns})
        print("completeness: unlisted skill items outside excluded folders:", unlisted if unlisted else "none")
        problems += len(unlisted)
    return 1 if problems else 0


# ----------------------------------------------------------------------------- scan
PROVIDER_RULES = [
    ("github-token", r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    ("github-pat", r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    ("anthropic-key", r"\bsk-ant-[A-Za-z0-9_\-]{20,}"),
    ("openai-key", r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_\-]{32,}"),
    ("aws-access-key", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("google-api-key", r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    ("slack-token", r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    ("stripe-live-key", r"\b[rs]k_live_[0-9A-Za-z]{20,}"),
    ("notion-token", r"\b(?:secret_[A-Za-z0-9]{43}|ntn_[A-Za-z0-9]{40,})\b"),
    ("huggingface-token", r"\bhf_[A-Za-z0-9]{34,}\b"),
    ("voyage-key", r"\bpa-[A-Za-z0-9_\-]{40,}"),
    ("private-key-block", r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY-----"),
    ("jwt", r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"),
    ("url-with-password", r"\b[a-zA-Z][a-zA-Z0-9+.\-]{1,20}://[^\s:/@'\"<>]{1,64}:([^\s@/'\"<>]{3,})@[^\s/'\"<>]+"),
]
GENERIC_RULE = re.compile(
    r"(?i)\b(password|passwd|pwd|secret|client_secret|api[_-]?key|apikey|access[_-]?token|auth[_-]?token|token)\b\s*[:=]\s*[\"']?([^\s\"'<>,;)}\]]{8,})")
PLACEHOLDER = re.compile(
    r"(?i)^(your|my|<|\$|\{|\[|%|xxx|\*|\.\.\.|example|placeholder|changeme|change_me|dummy|test|sample|none|null|nil|true|false|"
    r"os\.|process\.env|env\.|environ|getenv|config\.|settings\.|self\.|args\.|opts\.|input|os_|str\(|f\"|redacted|replace|insert|todo|"
    r"password|secret|token|api_?key|string|required|optional|os\.environ)")
URL_PLACEHOLDER_PASS = re.compile(r"(?i)^(pass(word)?|pwd|secret|xxx+|\*+|<.*>|\$\{?.*|changeme|example|user|postgres|root|admin|test)$")


def mask(value: str) -> str:
    return (value[:4] + "***" + f"(len {len(value)})") if len(value) > 4 else "***"


def scan_text(text: str, where: str, findings: list[dict]) -> None:
    for lineno, line in enumerate(text.splitlines(), 1):
        if len(line) > 5000:
            line = line[:5000]
        for rule, rx in PROVIDER_RULES:
            for m in re.finditer(rx, line):
                val = m.group(1) if (rule == "url-with-password" and m.groups()) else m.group(0)
                if rule == "url-with-password" and URL_PLACEHOLDER_PASS.match(val):
                    continue
                findings.append({"where": where, "line": lineno, "rule": rule, "severity": "high", "masked": mask(val)})
        for m in GENERIC_RULE.finditer(line):
            val = m.group(2)
            if PLACEHOLDER.match(val) or len(set(val)) <= 2 or "(" in val:
                continue
            # identifiers such as GEMINI_API_KEY or api_key_value are variable references, not values
            if re.fullmatch(r"[A-Z][A-Z0-9_]*", val) or re.fullmatch(r"[a-z_][a-z_.]*", val):
                continue
            findings.append({"where": where, "line": lineno, "rule": "generic-" + m.group(1).lower(), "severity": "review", "masked": mask(val)})


def is_binary(data: bytes) -> bool:
    return b"\x00" in data[:8192]


def cmd_scan(a) -> int:
    repo = Path(a.repo)
    findings: list[dict] = []
    scanned = 0
    for p in repo_files(repo):
        r = rel(repo, p)
        if p.is_symlink() or r.startswith(CHECKSUM_DIR) or r == f"{EXPORT_DIR}/secret-scan.json":
            continue
        try:
            data = p.read_bytes()
        except OSError as e:
            findings.append({"where": r, "line": 0, "rule": "unreadable", "severity": "review", "masked": str(e)})
            continue
        if zipfile.is_zipfile(p):
            try:
                with zipfile.ZipFile(p) as z:
                    for info in z.infolist():
                        if info.is_dir() or info.file_size > 20_000_000:
                            continue
                        member = z.read(info)
                        if not is_binary(member):
                            scan_text(member.decode("utf-8", "replace"), f"{r}!{info.filename}", findings)
                            scanned += 1
            except zipfile.BadZipFile:
                pass
            continue
        if is_binary(data) or len(data) > 50_000_000:
            continue
        scan_text(data.decode("utf-8", "replace"), r, findings)
        scanned += 1
    out = {"scanned_utc": utcnow(), "text_files_scanned": scanned, "findings": findings}
    write_json(repo / EXPORT_DIR / "secret-scan.json", out)
    high = [f for f in findings if f["severity"] == "high"]
    print(f"scanned {scanned} text files; high {len(high)}; review {len(findings) - len(high)}")
    for f in findings:
        print(f"  [{f['severity']}] {f['rule']} {f['where']}:{f['line']} {f['masked']}")
    return 0


# ----------------------------------------------------------------------------- index
def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    lines = text[3:end].splitlines()
    data: dict[str, str] = {}
    i = 0
    while i < len(lines):
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in (">", "|", ">-", "|-", ">+", "|+"):
            buf = []
            i += 1
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                buf.append(lines[i].strip())
                i += 1
            data[key] = (" " if val.startswith(">") else " ").join(b for b in buf if b).strip()
            continue
        buf = [val]
        j = i + 1
        while j < len(lines) and lines[j].startswith((" ", "\t")) and not re.match(r"^\s*-\s", lines[j]):
            buf.append(lines[j].strip())
            j += 1
        val = " ".join(x for x in buf if x)
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        data[key] = val
        i = j
    return data


def clean(text: str, limit: int | None = None) -> str:
    t = (text or "").replace("\u2014", " - ").replace("\u2013", "-").replace("\u2192", " to ").replace("\u21d2", " to ")
    t = t.replace("->", " to ").replace("=>", " to ")
    t = re.sub(r"\s+", " ", t).strip().replace("|", "\\|")
    if limit and len(t) > limit:
        cut = t[:limit]
        t = cut[: cut.rfind(" ")] + " ..." if " " in cut else cut + " ..."
    return t


def tree_signature(d: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(x for x in d.rglob("*") if x.is_file() or x.is_symlink()):
        h.update(p.relative_to(d).as_posix().encode())
        h.update(entry_hash(p).encode())
    return h.hexdigest()


def fmt_bytes(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return str(n)


def cmd_index(a) -> int:
    repo = Path(a.repo)
    cdir = repo / CHECKSUM_DIR
    parts = {p.stem: read_json(p) for p in sorted(cdir.glob("*.json")) if p.stem != "mac-completeness"}
    completeness = read_json(cdir / "mac-completeness.json") if (cdir / "mac-completeness.json").exists() else None
    scan = read_json(repo / EXPORT_DIR / "secret-scan.json") if (repo / EXPORT_DIR / "secret-scan.json").exists() else None
    review = read_json(repo / EXPORT_DIR / "secret-review.json") if (repo / EXPORT_DIR / "secret-review.json").exists() else {}
    order = [k for k in ("claude-account", "claude-plugins", "mac-superagent", "mac-other", "third-party") if k in parts] + \
            [k for k in parts if k not in ("claude-account", "claude-plugins", "mac-superagent", "mac-other", "third-party")]

    skills = []
    for p in repo_files(repo):
        if p.name == SKILL_FILE and not rel(repo, p).startswith(EXPORT_DIR + "/"):
            d = p.parent
            fm = parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
            skills.append({"dir": rel(repo, d), "part": rel(repo, d).split("/")[0], "name": fm.get("name") or d.name,
                           "description": fm.get("description", ""), "folder": d.name})
    packages = [rel(repo, p) for p in repo_files(repo) if p.name.endswith(PACKAGE_SUFFIX)]
    all_files = [p for p in repo_files(repo)]
    payload = [p for p in all_files if rel(repo, p).split("/")[0] not in (EXPORT_DIR,) and rel(repo, p) not in GENERATED]

    def count_skills(prefix: str) -> int:
        return sum(1 for s in skills if s["dir"] == prefix or s["dir"].startswith(prefix + "/"))

    def count_files(prefix: str) -> int:
        return sum(1 for p in payload if rel(repo, p) == prefix or rel(repo, p).startswith(prefix + "/"))

    captured = sorted({v.get("captured_utc", "") for v in parts.values() if v.get("captured_utc")})
    acct = parts.get("claude-account", {})
    acct_meta = {s["name"]: s for s in acct.get("skills", [])}

    # account versus mac comparison
    comp = []
    a_dir = repo / "claude-account" / "skills"
    m_dir = repo / "mac-superagent" / "skills"
    if a_dir.is_dir() and m_dir.is_dir():
        a_names = {d.name for d in a_dir.iterdir() if (d / SKILL_FILE).is_file()}
        m_names = {d.name for d in m_dir.iterdir() if (d / SKILL_FILE).is_file()}
        mac_mt = parts.get("mac-superagent", {}).get("source_mtimes", {})
        for n in sorted(a_names | m_names):
            newest_mac = max((t for k, t in mac_mt.items() if k.startswith(f"mac-superagent/skills/{n}/")), default="")
            if n in a_names and n in m_names:
                status = "identical" if tree_signature(a_dir / n) == tree_signature(m_dir / n) else "differs"
            elif n in a_names:
                status = "account only"
            else:
                status = "Mac only"
            comp.append({"name": n, "status": status, "account_updated": (acct_meta.get(n, {}).get("updatedAt") or "")[:10],
                         "mac_newest_file": newest_mac[:10]})

    L = []
    L.append("# claude-skills\n")
    L.append("Private export of every Claude skill in use: the skills synced to the Claude account, the installed plugins, "
             "the skill folders kept on the Mac, and a downloaded third-party skill pack. "
             f"Captured {', '.join(captured)} (UTC).\n")
    L.append("## Layout\n")
    L.append("| Folder in this repo | Origin | Skills | Files |")
    L.append("|---|---|---:|---:|")
    for k in order:
        for r in parts[k].get("rows", []):
            origin = r.get("origin", "")
            if parts[k].get("root_name"):
                origin = f"{parts[k]['root_name']}/{origin}"
            L.append(f"| `{r['dest']}` | {clean(origin)} | {count_skills(r['dest'])} | {count_files(r['dest'])} |")
    L.append(f"| **Total** | | **{len(skills)}** | **{len(payload)}** |\n")
    L.append(f"A skill is counted as a folder holding a `SKILL.md`. Packaged `.skill` files: {len(packages)}.\n")
    if acct.get("left_out_by_source"):
        names = ", ".join(f"{x['name']} ({x['source']})" for x in acct["left_out_by_source"])
        L.append(f"Left out of `claude-account`: Anthropic built-ins marked by the account manifest source field: {names}. "
                 "The anthropic entries carry a license that forbids copies outside Claude.\n")

    if comp:
        L.append("## Account copy versus Mac copy\n")
        L.append("| Skill | Status | Account updated | Newest Mac file |")
        L.append("|---|---|---|---|")
        for c in comp:
            L.append(f"| {c['name']} | {c['status']} | {c['account_updated']} | {c['mac_newest_file']} |")
        counts = {}
        for c in comp:
            counts[c["status"]] = counts.get(c["status"], 0) + 1
        L.append("\n" + ", ".join(f"{v} {k}" for k, v in sorted(counts.items())) + ".\n")

    L.append("## Skill index\n")
    for k in order:
        ks = sorted((s for s in skills if s["part"] == k), key=lambda s: s["dir"])
        if not ks:
            continue
        L.append(f"### {k} ({len(ks)})\n")
        L.append("| Skill | Path | Description |")
        L.append("|---|---|---|")
        limit = 220 if k == "third-party" else None
        for s in ks:
            L.append(f"| {clean(s['name'])} | `{s['dir']}` | {clean(s['description'], limit) or '(no description in SKILL.md)'} |")
        L.append("")
    if packages:
        L.append("### Packaged .skill files\n")
        for p in packages:
            L.append(f"- `{p}`")
        L.append("")
    L.append("## Verify\n")
    L.append("Every file is checksummed at its source before copying. From a clone, run:\n")
    L.append("```\npython3 export/skillexport.py verify --repo .\n```\n")
    L.append("## Refresh\n")
    L.append("`export/skillexport.py` rebuilds the export: `cloud` reads a Cowork skill and plugin sync cache, `mac` copies the "
             "sources listed in `export/sources.tsv` from the consulting folder, then `scan`, `index` and `verify`. "
             "Run `python3 export/skillexport.py --help` for arguments. `export/excludes.txt` holds the exclusion patterns.\n")
    (repo / "README.md").write_text("\n".join(L), encoding="utf-8")

    R = []
    R.append("# Export report\n")
    R.append(f"Generated {utcnow()} (UTC).\n")
    R.append("## Parts\n")
    R.append("| Part | Captured (UTC) | Files | Size | Excluded items | Broken symlinks skipped | Copy errors |")
    R.append("|---|---|---:|---:|---:|---:|---:|")
    for k in order:
        v = parts[k]
        R.append(f"| {k} | {v.get('captured_utc','')} | {v.get('file_count',0)} | {fmt_bytes(v.get('bytes',0))} | "
                 f"{len(v.get('excluded',[]))} | {len(v.get('broken_symlinks',[]))} | {len(v.get('errors',[]))} |")
    R.append("")
    for k in order:
        v = parts[k]
        R.append(f"### {k}\n")
        for r in v.get("rows", []):
            origin = f"{v['root_name']}/{r['origin']}" if v.get("root_name") else r.get("origin", "")
            extra = f", {r['files']} files" if "files" in r else ""
            R.append(f"- `{r['dest']}` from {clean(origin)}{extra}")
        if v.get("manifest_lastUpdated"):
            R.append(f"- Sync manifest lastUpdated: {v['manifest_lastUpdated']} (epoch ms)")
        if v.get("left_out_by_source"):
            R.append("- Left out by manifest source value: " + ", ".join(f"{x['name']} ({x['source']})" for x in v["left_out_by_source"]))
        if "plugins" in v:
            for p in v["plugins"]:
                R.append(f"- Plugin {p['name']} version {p.get('version')} from {p.get('marketplaceName')}: {p['skills']} skills, {p['files']} files")
            if v.get("not_copied_top_level_files"):
                R.append("- Sync metadata files not copied: " + ", ".join(v["not_copied_top_level_files"]))
        pats = {}
        for e in v.get("excluded", []):
            pats[e["pattern"]] = pats.get(e["pattern"], 0) + 1
        if pats:
            R.append("- Excluded by pattern: " + ", ".join(f"`{p}` {n}" for p, n in sorted(pats.items())))
        for b in v.get("broken_symlinks", []):
            R.append(f"- Broken symlink skipped: `{b['repo_path']}` pointing to `{b['target']}`")
        for b in v.get("dereferenced_symlinks", []):
            R.append(f"- Symlink stored as the file it points to: `{b['repo_path']}`")
        for e in v.get("errors", []):
            R.append(f"- Error: {e}")
        for g in v.get("cache_generation_copies", []):
            R.append(f"- Older sync cache generation `{g['folder']}` not copied: {'identical to' if g['identical'] else 'DIFFERS from'} `{g['of']}`")
        if v.get("unlisted_folders"):
            R.append("- Folders in the sync cache not in its manifest: " + ", ".join(v["unlisted_folders"]))
        R.append("")
    if completeness is not None:
        R.append("## Completeness check on the Mac folder\n")
        un = completeness.get("unlisted_skill_items", [])
        R.append(f"Searched `{completeness.get('root_name')}` for `SKILL.md` files and `.skill` packages outside the exported sources "
                 f"(skipping folders matched by the exclusion patterns): {len(un)} found.\n")
        for u in un:
            R.append(f"- {u}")
        R.append("")
    R.append("## Credential scan\n")
    if scan is None:
        R.append("Not run.\n")
    else:
        high = [f for f in scan["findings"] if f["severity"] == "high"]
        R.append(f"Scanned {scan['text_files_scanned']} text files including files inside `.skill` and zip packages, "
                 f"{scan['scanned_utc']}. Provider-format hits: {len(high)}. Generic assignments for review: {len(scan['findings']) - len(high)}. Values are masked.\n")
        if scan["findings"]:
            R.append("| Severity | Rule | Location | Masked value | Review |")
            R.append("|---|---|---|---|---|")
            for f in scan["findings"]:
                key = f"{f['where']}:{f['line']}"
                R.append(f"| {f['severity']} | {f['rule']} | `{clean(key)}` | `{f['masked']}` | {clean(review.get(key, 'not reviewed'))} |")
            R.append("")
    lower = {}
    for p in all_files:
        lower.setdefault(rel(repo, p).lower(), []).append(rel(repo, p))
    collisions = [v for v in lower.values() if len(v) > 1]
    R.append("## Path checks\n")
    R.append(f"Paths that differ only by letter case (a problem on macOS clones): {len(collisions)}.")
    for v in collisions:
        R.append(f"- {', '.join(v)}")
    big = [(rel(repo, p), p.stat().st_size) for p in all_files if not p.is_symlink() and p.stat().st_size > 50 * 1024 * 1024]
    R.append(f"\nFiles over 50 MB: {len(big)}.")
    for b in big:
        R.append(f"- {b[0]} {fmt_bytes(b[1])}")
    R.append("")
    (repo / "EXPORT_REPORT.md").write_text("\n".join(R), encoding="utf-8")

    lines = []
    for p in repo_files(repo):
        r = rel(repo, p)
        if r == "MANIFEST.sha256":
            continue
        lines.append(f"{entry_hash(p)}  {r}")
    (repo / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"index: {len(skills)} skills, {len(packages)} packages, {len(payload)} payload files, {len(lines)} manifest entries, case collisions {len(collisions)}")
    return 0


# ----------------------------------------------------------------------------- verify
def cmd_verify(a) -> int:
    repo = Path(a.repo)
    expected: dict[str, str] = {}
    for f in sorted((repo / CHECKSUM_DIR).glob("*.sha256")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                h, p = line.split("  ", 1)
                expected[p] = h
    bad, missing = [], []
    for p, h in expected.items():
        fp = repo / p
        if not (fp.exists() or fp.is_symlink()):
            missing.append(p)
        elif entry_hash(fp) != h:
            bad.append(p)
    payload = [rel(repo, p) for p in repo_files(repo)
               if rel(repo, p).split("/")[0] != EXPORT_DIR and rel(repo, p) not in GENERATED]
    uncovered = sorted(set(payload) - set(expected))
    mf_bad, mf_missing, mf_extra = [], [], []
    mf = repo / "MANIFEST.sha256"
    if mf.exists():
        listed = {}
        for line in mf.read_text(encoding="utf-8").splitlines():
            if line.strip():
                h, p = line.split("  ", 1)
                listed[p] = h
        present = {rel(repo, p) for p in repo_files(repo)} - {"MANIFEST.sha256"}
        mf_missing = sorted(set(listed) - present)
        mf_extra = sorted(present - set(listed))
        mf_bad = sorted(p for p in set(listed) & present if entry_hash(repo / p) != listed[p])
    ok = not (bad or missing or uncovered or mf_bad or mf_missing or mf_extra)
    print(f"source checksums: {len(expected)} entries, mismatched {len(bad)}, missing {len(missing)}, payload files not covered {len(uncovered)}")
    print(f"MANIFEST.sha256: {'present' if mf.exists() else 'absent'}, mismatched {len(mf_bad)}, missing {len(mf_missing)}, unlisted {len(mf_extra)}")
    for label, items in (("mismatch", bad), ("missing", missing), ("not covered", uncovered), ("manifest mismatch", mf_bad),
                         ("manifest missing", mf_missing), ("manifest unlisted", mf_extra)):
        for i in items[:20]:
            print(f"  {label}: {i}")
    print("VERIFY OK" if ok else "VERIFY FAILED")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cloud", help="copy account skills and plugins from a sync cache")
    c.add_argument("--skills-root", required=True)
    c.add_argument("--plugins-root", required=True)
    c.add_argument("--repo", required=True)
    c.add_argument("--excludes")
    c.add_argument("--exclude-source", action="append", help="manifest source value to leave out (repeatable)")
    m = sub.add_parser("mac", help="copy sources listed in a sources file")
    m.add_argument("--root", required=True)
    m.add_argument("--repo", required=True)
    m.add_argument("--sources", required=True)
    m.add_argument("--excludes")
    m.add_argument("--only-part", action="append", help="limit to a top-level repo folder (repeatable)")
    m.add_argument("--completeness", action="store_true", help="search the root for skill items outside the listed sources")
    s = sub.add_parser("scan", help="scan for credentials")
    s.add_argument("--repo", required=True)
    i = sub.add_parser("index", help="write README.md, EXPORT_REPORT.md, MANIFEST.sha256")
    i.add_argument("--repo", required=True)
    v = sub.add_parser("verify", help="verify checksums")
    v.add_argument("--repo", required=True)
    a = ap.parse_args()
    return {"cloud": cmd_cloud, "mac": cmd_mac, "scan": cmd_scan, "index": cmd_index, "verify": cmd_verify}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
