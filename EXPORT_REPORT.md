# Export report

Generated 2026-09-19T08:01:43Z (UTC).

## Parts

| Part | Captured (UTC) | Files | Size | Excluded items | Broken symlinks skipped | Copy errors |
|---|---|---:|---:|---:|---:|---:|
| claude-account | 2026-09-19T07:56:10Z | 173 | 1.0 MB | 1 | 0 | 0 |
| claude-plugins | 2026-09-19T07:56:10Z | 355 | 3.4 MB | 0 | 0 | 0 |
| mac-superagent | 2026-09-19T07:59:12Z | 229 | 20.5 MB | 6 | 1 | 0 |
| mac-other | 2026-09-19T07:59:12Z | 14 | 140.1 KB | 0 | 0 | 0 |
| third-party | 2026-09-19T07:59:17Z | 2377 | 26.5 MB | 0 | 0 | 0 |

### claude-account

- `claude-account/skills` from Claude account skill sync
- Sync manifest lastUpdated: 1789804301691 (epoch ms)
- Left out by manifest source value: built-in-browser (anthropic-example), chrome-browser (anthropic-example), computer-use (anthropic-example), deep-research (anthropic-example), docs (anthropic-example), docx (anthropic), import-memory (anthropic-example), mcp-builder (anthropic-example), morning (anthropic-example), pdf (anthropic), pptx (anthropic), skill-creator (anthropic-example), xlsx (anthropic)
- Excluded by pattern: `__pycache__/` 1

### claude-plugins

- `claude-plugins` from Claude plugin sync
- Sync manifest lastUpdated: 1789580246663 (epoch ms)
- Plugin engineering version 0038 from knowledge-work-plugins: 10 skills, 14 files
- Plugin human-resources version 0038 from knowledge-work-plugins: 9 skills, 13 files
- Plugin lightrag-developer version 0002 from My Uploads: 1 skills, 24 files
- Plugin operations version 0038 from knowledge-work-plugins: 9 skills, 13 files
- Plugin product-management version 0038 from knowledge-work-plugins: 8 skills, 14 files
- Plugin productivity version 0039 from knowledge-work-plugins: 4 skills, 10 files
- Plugin superpowers version 0001 from My Uploads: 14 skills, 136 files
- Plugin ui-ux-pro-max version 0002 from My Uploads: 1 skills, 130 files
- Sync metadata files not copied: engineering.meta.json, human-resources.meta.json, lightrag-developer.meta.json, operations.meta.json, product-management.meta.json, productivity.meta.json, superpowers.meta.json, ui-ux-pro-max.meta.json

### mac-superagent

- `mac-superagent/skills` from a. Consulting - SimCorp/ix. SimCorp SuperAgent/skills, 227 files
- `mac-superagent/packages/mirofish-research-agent.skill` from a. Consulting - SimCorp/ix. SimCorp SuperAgent/mirofish-research-agent.skill, 1 files
- `mac-superagent/packages/simcorp-super-agent.skill` from a. Consulting - SimCorp/ix. SimCorp SuperAgent/simcorp-super-agent.skill, 1 files
- Excluded by pattern: `.DS_Store` 4, `__pycache__/` 1, `_to_delete/` 1
- Broken symlink skipped: `mac-superagent/skills/simcorp-dex-validator/scripts/schema_index.json` pointing to `schema_index.json`

### mac-other

- `mac-other/overnight-dev` from a. Consulting - SimCorp/ii. Manuals & Documentation/overnight-dev, 9 files
- `mac-other/website-dev-team.skill` from a. Consulting - SimCorp/ii. Manuals & Documentation/website-dev-team.skill, 1 files
- `mac-other/skill-upgrade` from a. Consulting - SimCorp/vi. Config & Architecture/Schema Reference/skill-upgrade, 4 files

### third-party

- `third-party/claude-skills-package` from a. Consulting - SimCorp/ii. Manuals & Documentation/claude-skills-package, 2377 files

## Completeness check on the Mac folder

Searched `a. Consulting - SimCorp` for `SKILL.md` files and `.skill` packages outside the exported sources (skipping folders matched by the exclusion patterns): 0 found.


## Credential scan

Scanned 3393 text files including files inside `.skill` and zip packages, 2026-09-19T08:00:45Z. Provider-format hits: 10. Generic assignments for review: 39. Values are masked.

| Severity | Rule | Location | Masked value | Review |
|---|---|---|---|---|
| review | generic-api-key | `third-party/claude-skills-package/.claude/agents/everything-claude-code/.agents/skills/api-design/SKILL.md:306` | `sk_l***(len 14)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-apikey | `third-party/claude-skills-package/.claude/agents/everything-claude-code/.agents/skills/security-review/SKILL.md:27` | `sk-p***(len 13)` | Reviewed: example or template value in third-party documentation, not a credential |
| high | url-with-password | `third-party/claude-skills-package/.claude/skills/ay-skills/docs/skills/engineering/secrets-vault-manager.md:229` | `{{pa***(len 12)` | Reviewed: placeholder credentials in an example connection string |
| review | generic-api_key | `third-party/claude-skills-package/.claude/skills/ay-skills/docs/skills/engineering-team/senior-secops.md:360` | `sk-1***(len 19)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-api_key | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering/docker-development/references/dockerfile-best-practices.md:129` | `sk-1***(len 8)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-apikey | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering/helm-chart-builder/references/values-design.md:219` | `sk-a***(len 9)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-password | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering/helm-chart-builder/scripts/values_validator.py:40` | `supe***(len 14)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-api-key | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering/helm-chart-builder/scripts/values_validator.py:42` | `sk-1***(len 8)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-password | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering/performance-profiler/references/profiling-recipes.md:423` | `load***(len 11)` | Reviewed: example or template value in third-party documentation, not a credential |
| high | url-with-password | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering/secrets-vault-manager/SKILL.md:218` | `{{pa***(len 12)` | Reviewed: placeholder credentials in an example connection string |
| review | generic-secret | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering/secrets-vault-manager/references/cloud_secret_stores.md:119` | `prod***(len 16)` | Reviewed: example or template value in third-party documentation, not a credential |
| high | url-with-password | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering/secrets-vault-manager/references/vault_patterns.md:185` | `{{pa***(len 12)` | Reviewed: placeholder credentials in an example connection string |
| review | generic-api_key | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering/tech-debt-tracker/assets/sample_codebase/src/frontend.js:5` | `abc1***(len 12)` | Reviewed: example or template value in third-party documentation, not a credential |
| high | url-with-password | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering/tech-debt-tracker/assets/sample_codebase/src/user_service.py:13` | `pass***(len 11)` | Reviewed: placeholder credentials in an example connection string |
| review | generic-api_key | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering/tech-debt-tracker/assets/sample_codebase/src/user_service.py:14` | `sk-1***(len 19)` | Reviewed: example or template value in third-party documentation, not a credential |
| high | aws-access-key | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering/terraform-patterns/scripts/tf_security_scanner.py:28` | `AKIA***(len 20)` | Reviewed: AKIAIOSFODNN7EXAMPLE, the public AWS documentation example key, not a credential |
| review | generic-password | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering/terraform-patterns/scripts/tf_security_scanner.py:93` | `hard***(len 18)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-password | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/aws-solution-architect/references/best_practices.md:342` | `db_c***(len 9)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-api_key | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/code-reviewer/references/common_antipatterns.md:363` | `sk-a***(len 15)` | Reviewed: example or template value in third-party documentation, not a credential |
| high | url-with-password | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/code-reviewer/references/common_antipatterns.md:364` | `pass***(len 11)` | Reviewed: placeholder credentials in an example connection string |
| review | generic-token | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/playwright-pro/templates/api/auth-headers.md:6` | ``{{a***(len 11)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-token | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/playwright-pro/templates/api/auth-headers.md:7` | ``{{e***(len 18)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-token | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/playwright-pro/templates/api/auth-headers.md:8` | ``{{r***(len 15)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-token | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/playwright-pro/templates/api/error-responses.md:6` | ``{{a***(len 11)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-token | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/playwright-pro/templates/api/graphql.md:6` | ``{{a***(len 11)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-token | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/playwright-pro/templates/api/rate-limiting.md:6` | ``{{a***(len 11)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-token | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/playwright-pro/templates/api/rest-crud.md:6` | ``{{a***(len 11)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-token | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/playwright-pro/templates/onboarding/email-verification.md:7` | ``{{v***(len 20)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-token | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/playwright-pro/templates/onboarding/email-verification.md:8` | ``{{e***(len 27)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-token | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/playwright-pro/templates/onboarding/email-verification.md:60` | `inva***(len 17)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-password | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/playwright-pro/templates/settings/password-change.md:7` | ``{{c***(len 18)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-password | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/playwright-pro/templates/settings/password-change.md:8` | ``{{n***(len 14)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-apikey | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/senior-backend/references/api_design_patterns.md:397` | `req.***(len 12)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-api_key | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/senior-secops/SKILL.md:349` | `sk-1***(len 19)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-password | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/senior-security/references/cryptography-implementation.md:453` | `user***(len 18)` | Reviewed: example or template value in third-party documentation, not a credential |
| high | url-with-password | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/senior-security/references/security-architecture-patterns.md:582` | `Supe***(len 14)` | Reviewed: placeholder credentials in an example connection string |
| review | generic-api_key | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/senior-security/references/security-architecture-patterns.md:583` | `sk-1***(len 19)` | Reviewed: example or template value in third-party documentation, not a credential |
| high | private-key-block | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/senior-security/scripts/secret_scanner.py:165` | `----***(len 31)` | Reviewed: key header text inside a secret scanner regex, no key material |
| high | private-key-block | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/senior-security/scripts/secret_scanner.py:174` | `----***(len 30)` | Reviewed: key header text inside a secret scanner regex, no key material |
| high | private-key-block | `third-party/claude-skills-package/.claude/skills/ay-skills/engineering-team/senior-security/scripts/secret_scanner.py:183` | `----***(len 35)` | Reviewed: key header text inside a secret scanner regex, no key material |
| review | generic-api_key | `third-party/claude-skills-package/.claude/skills/ay-skills/standards/security/security-standards.md:54` | `sk-1***(len 19)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-api-key | `third-party/claude-skills-package/.claude/skills/everything-claude-code/api-design/SKILL.md:306` | `sk_l***(len 14)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-token | `third-party/claude-skills-package/.claude/skills/everything-claude-code/django-patterns/SKILL.md:513` | `paym***(len 13)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-password | `third-party/claude-skills-package/.claude/skills/everything-claude-code/django-tdd/SKILL.md:126` | `admi***(len 12)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-api_key | `third-party/claude-skills-package/.claude/skills/everything-claude-code/docker-patterns/SKILL.md:281` | `sk-p***(len 13)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-token | `third-party/claude-skills-package/.claude/skills/everything-claude-code/python-testing/SKILL.md:246` | `resp***(len 14)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-apikey | `third-party/claude-skills-package/.claude/skills/everything-claude-code/security-review/SKILL.md:27` | `sk-p***(len 13)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-apikey | `third-party/claude-skills-package/.claude/skills/n8n/n8n-code-javascript/DATA_ACCESS.md:535` | `webh***(len 27)` | Reviewed: example or template value in third-party documentation, not a credential |
| review | generic-apikey | `third-party/claude-skills-package/.claude/skills/n8n/n8n-expression-syntax/SKILL.md:198` | `={{$***(len 15)` | Reviewed: example or template value in third-party documentation, not a credential |

## Path checks

Paths that differ only by letter case (a problem on macOS clones): 0.

Files over 50 MB: 0.
