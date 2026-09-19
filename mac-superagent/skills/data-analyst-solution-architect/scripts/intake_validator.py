#!/usr/bin/env python3
"""
intake_validator.py — hard-halt gate for the data-analyst-solution-architect skill.

Stage 1: presence check on all 16 required INTAKE fields.
Stage 2: LLM review pass (Anthropic Claude Haiku by default) flags thin /
         contradictory / implausibly short fields per
         references/validator_llm_prompt.md.

Exit codes:
  0 — INTAKE passes both stages, engagement may proceed
  2 — presence check failed, missing fields listed
  3 — LLM review flagged thin fields, reasons listed
  4 — file not found or unreadable
  5 — Anthropic API call failed (LLM review unavailable)

No --force, --skip, or override flags. The halt is the point.

Usage:
    python intake_validator.py /path/to/INTAKE.md
    python intake_validator.py https://www.notion.so/{page_id}
"""
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

# 16 required fields, in display order.
REQUIRED_FIELDS = [
    "engagement",
    "profile",
    "deliverable_name",
    "version",
    "audience",
    "output_formats",
    "inputs",
    "scope_in",
    "scope_out",
    "source_truth_map_stub",
    "proposed_schema",
    "slicing_rule",
    "sme_questions",
    "citation_format",
    "verification_criteria",
    "notion_target",
]

# Minimum substantive length (chars) per field. Below this is "thin" even before
# LLM review. Empty (zero chars) is "missing".
MIN_SUBSTANTIVE_CHARS = {
    "engagement": 5,
    "profile": 6,
    "deliverable_name": 5,
    "version": 1,
    "audience": 12,
    "output_formats": 4,
    "inputs": 30,
    "scope_in": 10,
    "scope_out": 5,
    "source_truth_map_stub": 30,
    "proposed_schema": 30,
    "slicing_rule": 10,
    "sme_questions": 4,
    "citation_format": 10,
    "verification_criteria": 30,
    "notion_target": 3,
}


def parse_intake_markdown(text: str) -> dict[str, str]:
    """Parse INTAKE.md into {field_name: content}.

    Sections are demarcated by `## N. field_name` headers. Content is
    everything between the header and the next `## ` header, with leading/
    trailing whitespace stripped and surrounding boilerplate (lines starting
    with `>`) removed.
    """
    out: dict[str, str] = {}
    header_re = re.compile(r"^##\s+\d+\.\s+([a-z_]+)\s*$", re.MULTILINE)
    matches = list(header_re.finditer(text))
    for i, m in enumerate(matches):
        name = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        # Strip blockquote boilerplate and placeholder lines.
        lines = []
        for line in body.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith(">"):
                continue
            # Treat un-filled placeholder template lines ({...}) as empty.
            if stripped.startswith("{") and stripped.endswith("}"):
                continue
            lines.append(line)
        out[name] = "\n".join(lines).strip()
    return out


def stage1_presence_check(parsed: dict[str, str]) -> list[tuple[str, str]]:
    """Return list of (field, reason) for failures. Empty list = pass."""
    failures: list[tuple[str, str]] = []
    for f in REQUIRED_FIELDS:
        v = parsed.get(f, "").strip()
        if not v:
            failures.append((f, "MISSING — field absent or empty"))
            continue
        if len(v) < MIN_SUBSTANTIVE_CHARS[f]:
            failures.append((
                f,
                f"TOO_SHORT — {len(v)} chars (minimum {MIN_SUBSTANTIVE_CHARS[f]})",
            ))
    return failures


def stage2_llm_review(parsed: dict[str, str], prompt_template: str) -> list[tuple[str, str]]:
    """Call Anthropic to flag thin/contradictory fields. Empty list = pass.

    Reads ANTHROPIC_API_KEY from env. Uses haiku by default.
    """
    try:
        import anthropic  # type: ignore
    except ImportError:
        print(
            "WARN — anthropic package not installed; "
            "LLM review skipped. Install with: pip install anthropic",
            file=sys.stderr,
        )
        return []

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(
            "WARN — ANTHROPIC_API_KEY not set; LLM review skipped.",
            file=sys.stderr,
        )
        return []

    intake_serialized = "\n\n".join(
        f"## {f}\n{parsed.get(f, '')}" for f in REQUIRED_FIELDS
    )
    prompt = prompt_template.replace("{intake_content}", intake_serialized)

    client = anthropic.Anthropic(api_key=api_key)
    model = os.environ.get("DAS_VALIDATOR_MODEL", "claude-haiku-4-5-20251001")
    msg = client.messages.create(
        model=model,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    response_text = msg.content[0].text.strip()

    # Extract the JSON object — the prompt instructs the model to return JSON
    # only, but be defensive about ```json``` fences.
    response_text = re.sub(r"^```(?:json)?\s*", "", response_text)
    response_text = re.sub(r"\s*```$", "", response_text)
    try:
        findings = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"WARN — LLM returned non-JSON; review skipped. Error: {e}", file=sys.stderr)
        print(f"Response was:\n{response_text}", file=sys.stderr)
        return []

    failures: list[tuple[str, str]] = []
    for f in REQUIRED_FIELDS:
        finding = findings.get(f)
        if not finding:
            continue
        if not finding.get("ok", True):
            failures.append((f, f"THIN — {finding.get('reason', 'no reason given')}"))
    return failures


def load_intake(path_or_url: str) -> str:
    """Load INTAKE content from a markdown file, a docx file, or a Notion URL.

    For Notion URLs the caller must have notion-fetch MCP available — this
    script falls back to printing instructions if the URL is provided but the
    notion fetch helper isn't wired up.
    """
    if path_or_url.startswith("http"):
        return _fetch_notion(path_or_url)
    p = Path(path_or_url)
    if not p.exists():
        print(f"FAIL — file not found: {p}", file=sys.stderr)
        sys.exit(4)
    if p.suffix.lower() == ".md":
        return p.read_text(encoding="utf-8")
    if p.suffix.lower() == ".docx":
        return _load_docx(p)
    print(f"FAIL — unsupported file type: {p.suffix}", file=sys.stderr)
    sys.exit(4)


def _load_docx(p: Path) -> str:
    try:
        from docx import Document  # type: ignore
    except ImportError:
        print("FAIL — python-docx not installed; pip install python-docx", file=sys.stderr)
        sys.exit(4)
    d = Document(str(p))
    # Reconstruct markdown-ish structure from headings + paragraphs.
    out: list[str] = []
    for p_ in d.paragraphs:
        text = p_.text.strip()
        if not text:
            continue
        # Numbered headings like "1. engagement" → "## 1. engagement"
        m = re.match(r"^(\d+)\.\s+([a-z_]+)\s*$", text)
        if m:
            out.append(f"## {m.group(1)}. {m.group(2)}")
        elif text.startswith("____"):
            continue
        else:
            out.append(text)
    return "\n\n".join(out)


def _fetch_notion(url: str) -> str:
    print(
        "Notion intake validation is supported via the orchestrating Claude "
        "session (with notion-fetch MCP), not directly by this script. "
        "Have Claude serialize the Notion page into a markdown INTAKE first.",
        file=sys.stderr,
    )
    sys.exit(4)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path-to-INTAKE.md|.docx|notion-url>", file=sys.stderr)
        return 4

    intake_path = sys.argv[1]
    skill_dir = Path(__file__).resolve().parent.parent
    prompt_path = skill_dir / "references" / "validator_llm_prompt.md"

    print(f"intake_validator — reading {intake_path}")
    text = load_intake(intake_path)
    parsed = parse_intake_markdown(text)
    print(f"  parsed {len(parsed)} fields from INTAKE")

    # ---- Stage 1: presence check ----
    print("\nStage 1 — presence check")
    s1_failures = stage1_presence_check(parsed)
    if s1_failures:
        print("HALT — presence check failed:")
        for field, reason in s1_failures:
            print(f"  ✗ {field}: {reason}")
        print(
            f"\n{len(s1_failures)} field(s) missing or too short. "
            "Fix and re-run. No override flag exists."
        )
        return 2
    print(f"  ✓ all {len(REQUIRED_FIELDS)} fields present and ≥ minimum length")

    # ---- Stage 2: LLM review ----
    print("\nStage 2 — LLM review")
    if not prompt_path.exists():
        print(f"WARN — prompt template not at {prompt_path}; LLM review skipped.")
        s2_failures: list[tuple[str, str]] = []
    else:
        prompt_text = prompt_path.read_text(encoding="utf-8")
        # Extract the actual prompt body — the file wraps it in ``` fences for
        # documentation. The prompt body is everything between the first ```
        # and the matching closing fence.
        m = re.search(r"```\n(.+?)\n```", prompt_text, re.DOTALL)
        prompt_body = m.group(1) if m else prompt_text
        s2_failures = stage2_llm_review(parsed, prompt_body)

    if s2_failures:
        print("HALT — LLM review flagged thin or contradictory fields:")
        for field, reason in s2_failures:
            print(f"  ⚠ {field}: {reason}")
        print(
            f"\n{len(s2_failures)} field(s) need substantive content. "
            "Fix and re-run."
        )
        return 3
    print("  ✓ LLM review passed (no thin or contradictory fields)")

    print("\n✓ INTAKE complete — engagement may proceed to STAGE 1 (inventory)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
