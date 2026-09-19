# Claude Code Skills Mega-Package — Installation Guide

## What's Inside

**386 skills, 56 agents, 62 commands, 25 hooks** from 13 GitHub repos, organized into a single `.claude/` directory.

### Skills Breakdown by Source

| Source Repo | Skills | What It Does |
|---|---|---|
| **ay-skills** (alirezarezvani/claude-skills) | 216 | 192+ skills across engineering, marketing, product, compliance, C-level advisory |
| **everything-claude-code** (affaan-m/everything-claude-code) | 125 | Full operating system: API design, backend patterns, TDD, security, content engine |
| **superpowers** (obra/superpowers) | 14 | Spec-first development: brainstorming, TDD, debugging, code review, git worktrees |
| **ui-ux-pro-max** (nextlevelbuilder/ui-ux-pro-max-skill) | 7 | 161 design rules, color palettes, font pairings, slides, brand systems |
| **n8n** (czlonkowski/n8n-mcp + n8n-skills) | 7 | n8n workflow patterns, code, expressions, node config, validation |
| **best-practices** (shanraisshan/claude-code-best-practice) | 7 | Production tips, agent browser, weather, time, presentation skills |
| **claude-mem** (thedotmack/claude-mem) | 5 | Persistent memory: mem-search, smart-explore, timeline-report |
| **obsidian** (kepano/obsidian-skills) | 5 | Obsidian vault: markdown, bases, CLI, JSON canvas, defuddle |

### Also Included

- **get-shit-done** (gsd-build/get-shit-done) — 57 commands + 18 agents for context persistence
- **claude-code-hooks-mastery** (disler/claude-code-hooks-mastery) — 25 hook implementations
- **context-engineering-intro** (coleam00/context-engineering-intro) — PRP generation commands
- 6 reference CLAUDE.md files from key repos

---

## Installation

### Option 1: Copy Entire Package (Recommended)

```bash
# From your project root:
cp -r package/.claude/ .claude/
cp -r package/references/ .claude/references/
```

### Option 2: Cherry-Pick Specific Repos

```bash
# Example: Only install superpowers + ui-ux-pro-max
cp -r package/.claude/skills/superpowers/ .claude/skills/superpowers/
cp -r package/.claude/skills/ui-ux-pro-max/ .claude/skills/ui-ux-pro-max/
```

### Option 3: Install as Claude Code Plugin (for superpowers, ui-ux-pro-max)

Some repos are also available as official Claude plugins:
```bash
# In Claude Code terminal:
/install-plugin superpowers
/install-plugin ui-ux-pro-max
```

---

## Directory Structure

```
.claude/
├── skills/                    # 386 SKILL.md files
│   ├── ay-skills/             # 216 skills (product, engineering, marketing, C-level)
│   ├── everything-claude-code/ # 125 skills (full dev operating system)
│   ├── superpowers/           # 14 skills (spec-first workflow)
│   ├── ui-ux-pro-max/        # 7 skills (design intelligence)
│   ├── n8n/                   # 7 skills (workflow automation)
│   ├── best-practices/        # 7 skills (production tips)
│   ├── claude-mem/            # 5 skills (persistent memory)
│   └── obsidian/              # 5 skills (knowledge management)
├── agents/                    # 56 agent definitions
│   ├── everything-claude-code/
│   ├── get-shit-done/
│   └── n8n/
├── commands/                  # 62 command files
│   ├── get-shit-done/
│   ├── superpowers/
│   └── context-engineering/
├── hooks/                     # 25 hook implementations
└── references/                # 6 CLAUDE.md files from key repos
```

---

## AI Product Manager Skills

See `PM_SKILLS_CATALOG.md` for a comprehensive catalog of **317 PM-related skills** extracted from all repos, organized by category:

1. Product Strategy & Vision (48 skills)
2. Product Discovery & Research (71 skills)
3. Product Metrics & Analytics (69 skills)
4. User-Centric Design (59 skills)
5. Roadmapping & Planning (20 skills)
6. Go-to-Market & Pricing (25 skills)
7. Stakeholder Management (22 skills)
8. Team & Process (3 skills)

---

## Source Repos

| # | Repo | GitHub |
|---|---|---|
| 1 | everything-claude-code | https://github.com/affaan-m/everything-claude-code |
| 2 | superpowers | https://github.com/obra/superpowers |
| 3 | ui-ux-pro-max | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill |
| 4 | claude-mem | https://github.com/thedotmack/claude-mem |
| 5 | get-shit-done | https://github.com/gsd-build/get-shit-done |
| 6 | awesome-claude-code | https://github.com/hesreallyhim/awesome-claude-code |
| 7 | obsidian-skills | https://github.com/kepano/obsidian-skills |
| 8 | lightrag | https://github.com/HKUDS/LightRAG |
| 9 | n8n-mcp | https://github.com/czlonkowski/n8n-mcp |
| 10 | context-engineering-intro | https://github.com/coleam00/context-engineering-intro |
| 11 | ay-skills | https://github.com/alirezarezvani/claude-skills |
| 12 | claude-code-best-practice | https://github.com/shanraisshan/claude-code-best-practice |
| 13 | awesome-agent-skills | https://github.com/VoltAgent/awesome-agent-skills |
| 14 | claude-code-hooks-mastery | https://github.com/disler/claude-code-hooks-mastery |

---

## Notes

- **LightRAG** is a Python framework (not a skill collection) — install separately via pip if needed
- **awesome-claude-code** and **awesome-agent-skills** are curated directories (reference lists, not installable skills)
- Some skills may overlap across repos — this is intentional for completeness
- The `references/` directory contains CLAUDE.md files that provide project-level context engineering examples
