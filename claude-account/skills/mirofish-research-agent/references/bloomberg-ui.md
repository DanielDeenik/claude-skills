# Bloomberg Terminal Design System

A design language for financial research agents that feels professional, data-dense,
and trustworthy — inspired by Bloomberg Terminal aesthetics adapted for React + Tailwind.

---

## Color Palette

All colors must be defined as CSS custom properties or Tailwind config values, never
hardcoded inline.

### Core Colors
| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#0a0e17` | Main background — near-black with blue undertone |
| `--bg-secondary` | `#111827` | Card/panel backgrounds |
| `--bg-tertiary` | `#1a2332` | Elevated surfaces, hover states |
| `--border-default` | `#1e293b` | Subtle borders between panels |
| `--border-active` | `#334155` | Active/focused borders |

### Data Colors (semantic — color encodes meaning)
| Token | Hex | Meaning |
|-------|-----|---------|
| `--data-bullish` | `#00ff88` | Positive signals, gains, approval |
| `--data-bearish` | `#ff3366` | Negative signals, losses, rejection |
| `--data-neutral` | `#ffaa00` | Amber — caution, monitoring, DEFER |
| `--data-info` | `#00d4ff` | Cyan — informational, timestamps, metadata |
| `--data-muted` | `#64748b` | Slate — secondary text, disabled states |

### Signal Category Colors
| Token | Hex | Category |
|-------|-----|----------|
| `--signal-fundamental` | `#818cf8` | Indigo — fundamental data signals |
| `--signal-structural` | `#34d399` | Emerald — structural/industry signals |
| `--signal-behavioral` | `#f59e0b` | Amber — behavioral/flow signals |
| `--signal-sentiment` | `#f472b6` | Pink — sentiment delta signals |

---

## Typography

| Element | Font | Size | Weight | Case |
|---------|------|------|--------|------|
| Data/numbers | `'JetBrains Mono', 'Fira Code', monospace` | 13px | 400 | — |
| Labels | `'Inter', system-ui, sans-serif` | 11px | 500 | UPPERCASE |
| Section headers | `'Inter', system-ui, sans-serif` | 13px | 600 | UPPERCASE |
| Thesis text | `'Inter', system-ui, sans-serif` | 14px | 400 | Sentence |
| Score/conviction | `'JetBrains Mono', monospace` | 24px | 700 | — |

Load fonts from Google Fonts CDN or use system fallbacks. Never embed font files.

---

## Layout Principles

### Density
- Bloomberg terminals pack maximum data per pixel. Resist the urge to add whitespace.
- Padding inside panels: `p-3` (12px). Gap between panels: `gap-2` (8px).
- No panel larger than 50% viewport height unless scrollable.

### Grid System
- Use CSS Grid with named areas for the main layout.
- Default research agent layout:

```
+------------------+------------------+
|  MISSION HEADER (full width)        |
+------------------+------------------+
| SIGNAL GRID      | THESIS PANEL     |
| (4-col mosaic)   | (structured)     |
|                  |                  |
+------------------+------------------+
| CATALYST CHAIN   | RISK MATRIX      |
+------------------+------------------+
| HITL CONTROLS (full width)          |
+------------------+------------------+
```

### Responsive
- Desktop: full grid as above
- Tablet: stack thesis below signals
- Mobile: single column, collapsible sections

---

## Component Patterns

### Mission Header
```jsx
// Tailwind classes pattern
<div className="bg-[var(--bg-secondary)] border-b border-[var(--border-default)] px-4 py-3">
  <div className="flex items-center justify-between">
    <div className="flex items-center gap-3">
      <span className="font-mono text-[var(--data-info)] text-xs">MISSION</span>
      <h1 className="font-mono text-white text-lg font-bold">{assetName}</h1>
      <span className="px-2 py-0.5 text-xs font-medium rounded bg-[var(--bg-tertiary)]
        text-[var(--data-info)] border border-[var(--border-default)]">
        {assetClass}
      </span>
    </div>
    <span className="font-mono text-[var(--data-muted)] text-xs">{timestamp}</span>
  </div>
</div>
```

### Signal Fragment Card
Each mosaic fragment is a compact card with:
- Category color bar on the left border (4px, using signal category colors)
- Source label (uppercase, muted)
- Signal text (14px, white)
- Confidence badge (monospace, colored by strength)
- Timestamp (muted, bottom-right)

### Conviction Meter
A horizontal bar showing conviction 1-10:
- Segments light up left-to-right
- Colors transition: red (1-3) → amber (4-6) → green (7-10)
- Current value displayed as large monospace number

### HITL Control Bar
- Fixed at bottom of viewport or bottom of agent panel
- Three prominent buttons: APPROVE (green), DEFER (amber), REJECT (red)
- Textarea for reasoning (required before action)
- Keyboard shortcuts: `A` approve, `D` defer, `R` reject

### Data Table
- No alternating row colors — use subtle bottom borders
- Header row: uppercase, muted color, smaller font
- Data cells: monospace for numbers, left-align text, right-align numbers
- Sortable columns with arrow indicators
- Hover: row background shifts to `--bg-tertiary`

---

## Animation & Real-Time Feel

- **Pulse:** New data points get a brief cyan pulse animation (0.5s)
- **Fade-in:** Panels load with a 150ms fade-in, staggered by 50ms
- **Ticker:** Scrolling ticker bar for latest signals (optional, top of agent)
- **Timestamp:** Every data point shows relative time ("2m ago") that updates live
- No loading spinners — use skeleton screens with the terminal aesthetic

```css
@keyframes dataPulse {
  0% { box-shadow: 0 0 0 0 rgba(0, 212, 255, 0.4); }
  100% { box-shadow: 0 0 0 8px rgba(0, 212, 255, 0); }
}
```

---

## Keyboard Shortcuts

Research agents should support keyboard navigation:

| Key | Action |
|-----|--------|
| `1-4` | Focus signal category (Fundamental/Structural/Behavioral/Sentiment) |
| `T` | Toggle thesis panel expand/collapse |
| `A` | Approve at HITL gate |
| `D` | Defer at HITL gate |
| `R` | Reject at HITL gate |
| `?` | Show keyboard shortcut overlay |
| `Esc` | Close any expanded panel |

---

## Applying to JSX Artifacts

When building standalone JSX artifacts (React components for Claude artifacts):

1. Define all colors as a `THEME` object at the top of the file — single source of truth
2. Use inline styles or Tailwind classes that reference the theme object
3. Import only from available libraries: `recharts`, `lucide-react`, `d3`
4. No localStorage — use `useState` for all state
5. Default export a component with no required props
6. Make the component self-contained: data fetching simulation, state management, UI all in one file

```jsx
const THEME = {
  bg: { primary: '#0a0e17', secondary: '#111827', tertiary: '#1a2332' },
  border: { default: '#1e293b', active: '#334155' },
  data: { bullish: '#00ff88', bearish: '#ff3366', neutral: '#ffaa00', info: '#00d4ff', muted: '#64748b' },
  signal: { fundamental: '#818cf8', structural: '#34d399', behavioral: '#f59e0b', sentiment: '#f472b6' },
  font: { mono: "'JetBrains Mono', 'Fira Code', monospace", sans: "'Inter', system-ui, sans-serif" }
};
```

This THEME object is the only place colors/fonts appear. Everything else references it.
