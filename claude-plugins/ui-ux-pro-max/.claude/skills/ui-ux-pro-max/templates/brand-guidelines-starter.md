# Brand Guidelines v1.0

> Last updated: 2026-03-31
> Status: Active

## Quick Reference

| Element | Value |
|---------|-------|
| Primary Color | #0D9488 |
| Secondary Color | #1E3A5F |
| Primary Font | IBM Plex Sans |
| Voice | Precise, Empowering, Trustworthy |

---

## 1. Color Palette

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Teal 600 | #0D9488 | rgb(13,148,136) | CTAs, headers, links, primary actions |
| Teal 700 | #0F766E | rgb(15,118,110) | Hover states, emphasis |
| Teal 50 | #F0FDFA | rgb(240,253,250) | Tinted backgrounds, highlights |

### Secondary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Navy 800 | #1E3A5F | rgb(30,58,95) | Sidebar, navigation, dark accents |
| Navy 900 | #162D4A | rgb(22,45,74) | Dark sections, footers |
| Slate Blue | #475569 | rgb(71,85,105) | Supporting text, secondary UI |

### Neutral Palette

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| White | #FFFFFF | rgb(255,255,255) | Page backgrounds |
| Slate 50 | #F8FAFC | rgb(248,250,252) | Cards, surface areas |
| Slate 100 | #F1F5F9 | rgb(241,245,249) | Section backgrounds |
| Slate 200 | #E2E8F0 | rgb(226,232,240) | Borders, dividers |
| Slate 500 | #64748B | rgb(100,116,139) | Muted text, captions |
| Slate 900 | #0F172A | rgb(15,23,42) | Primary text, headings |

### Semantic Colors

| State | Hex | Usage |
|-------|-----|-------|
| Success | #16A34A | Positive actions, confirmations, completed tasks |
| Warning | #D97706 | Cautions, pending states, approaching deadlines |
| Error | #DC2626 | Errors, destructive actions, overdue items |
| Info | #0284C7 | Informational messages, tips |

### Accessibility

- Text on white background: 12.6:1 contrast ratio (AAA)
- Primary teal on white: 4.5:1 contrast ratio (AA)
- Navy on white: 9.7:1 contrast ratio (AAA)
- All interactive elements meet WCAG 2.1 AA standards

---

## 2. Typography

### Font Stack

```css
--font-heading: 'IBM Plex Sans', 'Inter', system-ui, -apple-system, sans-serif;
--font-body: 'IBM Plex Sans', 'Inter', system-ui, -apple-system, sans-serif;
--font-mono: 'IBM Plex Mono', 'JetBrains Mono', monospace;
```

### Type Scale

| Element | Size (Desktop) | Size (Mobile) | Weight | Line Height |
|---------|----------------|---------------|--------|-------------|
| H1 | 40px | 28px | 700 | 1.2 |
| H2 | 32px | 24px | 600 | 1.25 |
| H3 | 24px | 20px | 600 | 1.3 |
| H4 | 20px | 18px | 600 | 1.35 |
| Body | 15px | 15px | 400 | 1.6 |
| Body Large | 17px | 17px | 400 | 1.6 |
| Small | 13px | 13px | 400 | 1.5 |
| Caption | 12px | 12px | 500 | 1.4 |

### Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
```

---

## 3. Logo Usage

### Variants

| Variant | File | Use Case |
|---------|------|----------|
| Full Horizontal | logo-full-horizontal.svg | Headers, documents, dashboards |
| Stacked | logo-stacked.svg | Square spaces, app icons |
| Icon Only | logo-icon.svg | Favicons, small spaces, mobile |
| Monochrome | logo-mono.svg | Limited color contexts, print |

### Clear Space

Minimum clear space = height of the logo icon (mark)

### Minimum Size

| Context | Minimum Width |
|---------|---------------|
| Digital - Full Logo | 120px |
| Digital - Icon | 24px |
| Print - Full Logo | 35mm |
| Print - Icon | 10mm |

### Don'ts

- Don't rotate or skew the logo
- Don't change colors outside approved palette
- Don't add shadows or effects
- Don't crop or modify proportions
- Don't place on busy backgrounds without sufficient contrast

---

## 4. Voice & Tone

### Brand Personality

| Trait | Description |
|-------|-------------|
| **Precise** | Clear, specific language. No vague claims — show the numbers, name the feature. |
| **Empowering** | Help users feel capable and in control of their work. |
| **Trustworthy** | Honest about limitations, reliable in delivery. Enterprise-grade credibility. |
| **Efficient** | Respect the reader's time. Say it once, say it well. |

### Voice Chart

| Trait | We Are | We Are Not |
|-------|--------|------------|
| Precise | Specific, data-informed, concrete | Vague, hyperbolic, hand-wavy |
| Empowering | Supportive, enabling, respectful | Patronizing, prescriptive |
| Trustworthy | Honest, consistent, transparent | Salesy, over-promising |
| Efficient | Concise, direct, well-structured | Verbose, repetitive, fluffy |

### Tone by Context

| Context | Tone | Example |
|---------|------|---------|
| Marketing | Confident, benefit-driven | "Ship projects on time, every time." |
| Product UI | Clear, instructional | "Drag tasks to reorder your sprint." |
| Error messages | Calm, solution-focused | "Couldn't save — check your connection and try again." |
| Success | Brief, affirming | "Sprint planned. You're ready to go." |
| Onboarding | Warm, guiding | "Let's set up your first project in under 2 minutes." |

### Prohibited Terms

| Avoid | Reason |
|-------|--------|
| Revolutionary | Overused, vague |
| Best-in-class | Unsubstantiated claim |
| Seamless | Overused |
| Synergy | Corporate jargon |
| Leverage | Use "use" instead |
| Disruptive | Overused startup jargon |
| 10x | Hyperbolic unless backed by data |

---

## 5. Imagery Guidelines

### Photography Style

- **Lighting:** Clean, even studio or natural office lighting
- **Subjects:** Real professionals in focused work environments
- **Color treatment:** Neutral or lightly teal-tinted post-processing
- **Composition:** Clean backgrounds, focused subjects, minimal clutter

### Illustrations

- Style: Modern geometric, clean vector with subtle teal accents
- Colors: Brand palette only — teal, navy, slates
- Line weight: 1.5–2px consistent stroke
- Corners: 4px rounded

### Icons

- Style: Outlined, 24px base grid
- Stroke: 1.5px consistent
- Corner radius: 2px
- Fill: None (outline only), teal for active states

---

## 6. Design Components

### Buttons

| Type | Background | Text | Border | Border Radius |
|------|------------|------|--------|---------------|
| Primary | #0D9488 | #FFFFFF | none | 8px |
| Secondary | Transparent | #0D9488 | 1px #0D9488 | 8px |
| Tertiary | Transparent | #64748B | none | 8px |
| Destructive | #DC2626 | #FFFFFF | none | 8px |

### Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Tight spacing |
| sm | 8px | Compact elements |
| md | 16px | Standard spacing |
| lg | 24px | Section spacing |
| xl | 32px | Large gaps |
| 2xl | 48px | Section dividers |
| 3xl | 64px | Page-level spacing |

### Border Radius

| Element | Radius |
|---------|--------|
| Buttons | 8px |
| Cards | 12px |
| Inputs | 8px |
| Modals | 16px |
| Pills/Tags | 9999px |
| Avatars | 9999px |

---

## AI Image Generation

### Base Prompt Template

Always prepend to image generation prompts:

```
Professional, clean B2B SaaS aesthetic. Teal (#0D9488) and navy (#1E3A5F) accent colors on white/light gray backgrounds. Modern geometric style, high contrast, structured composition. Corporate but approachable.
```

### Style Keywords

| Category | Keywords |
|----------|----------|
| **Lighting** | Even studio lighting, soft ambient, clean |
| **Mood** | Professional, confident, productive, focused |
| **Composition** | Structured, grid-aligned, balanced, minimal |
| **Treatment** | High contrast, crisp edges, muted backgrounds |
| **Aesthetic** | Modern corporate, clean SaaS, enterprise-grade |

### Visual Mood Descriptors

- Focused productivity — tools that get out of the way
- Structured clarity — information hierarchy that guides the eye
- Confident restraint — premium feel through simplicity, not excess

### Visual Don'ts

| Avoid | Reason |
|-------|--------|
| Neon or overly saturated colors | Conflicts with professional tone |
| Busy, cluttered compositions | Undermines the clarity brand promise |
| Stock photos with forced smiles | Feels inauthentic to B2B audience |
| Excessive gradients or glows | Clashes with clean, structured aesthetic |

### Example Prompts

**Hero Banner:**
```
Clean SaaS dashboard interface showing project management tools, teal (#0D9488) accent elements on white background, structured grid layout, professional lighting, isometric perspective, 4K quality
```

**Social Media Post:**
```
Minimal B2B SaaS branded graphic, navy (#1E3A5F) background, teal (#0D9488) geometric accents, IBM Plex Sans typography, clean layout with ample whitespace, professional and modern
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-31 | Initial guidelines — teal/navy palette, IBM Plex Sans, professional voice |
