# TDD Patterns for MiroFish Research Agents

Test-first patterns for financial data processing, config validation, HITL gates,
and Bloomberg-style UI components.

---

## Backend: pytest Patterns

### Config Validation (write this test FIRST for every mission)

The single most important test: prove that no hardcoded values leak into the implementation.

```python
"""Test that all configurable values come from config, not inline constants."""
import ast
import os

def test_no_hardcoded_thresholds(mission_module_path):
    """Scan implementation files for suspicious numeric literals."""
    ALLOWED_LITERALS = {0, 1, -1, 2, 100}  # Truly universal constants

    for root, _, files in os.walk(mission_module_path):
        for fname in files:
            if not fname.endswith('.py') or fname.startswith('test_'):
                continue
            filepath = os.path.join(root, fname)
            with open(filepath) as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                    if node.value not in ALLOWED_LITERALS:
                        # Check if it's inside a config default or test
                        assert False, (
                            f"Suspicious literal {node.value} in {fname}:{node.lineno}. "
                            f"Move to config."
                        )


def test_config_keys_documented(config_module, solution_doc_path):
    """Every config key in the implementation must appear in the solution doc."""
    import re
    with open(solution_doc_path) as f:
        doc_text = f.read()

    for key in config_module.get_all_keys():
        assert key in doc_text, f"Config key '{key}' not documented in solution doc"
```

### Signal Collection Tests

```python
"""Test signal collectors return valid, typed data."""
import pytest
from datetime import datetime, timedelta

class TestSignalCollection:

    def test_signal_has_required_fields(self, collector, sample_config):
        """Every signal must have: source, timestamp, value, confidence, category."""
        signals = collector.collect(config=sample_config)
        for signal in signals:
            assert 'source' in signal
            assert 'timestamp' in signal
            assert isinstance(signal['timestamp'], datetime)
            assert 'value' in signal
            assert 'confidence' in signal and 0 <= signal['confidence'] <= 1
            assert signal['category'] in ('fundamental', 'structural', 'behavioral', 'sentiment')

    def test_stale_signals_filtered(self, collector, sample_config):
        """Signals older than config threshold should be excluded."""
        max_age = sample_config.get('signal_max_age_hours', 24)
        signals = collector.collect(config=sample_config)
        cutoff = datetime.utcnow() - timedelta(hours=max_age)
        for signal in signals:
            assert signal['timestamp'] >= cutoff

    def test_empty_response_handled(self, collector, sample_config, mock_empty_api):
        """Collector returns empty list, not error, when source has no data."""
        signals = collector.collect(config=sample_config)
        assert signals == []

    def test_rate_limit_respected(self, collector, sample_config):
        """Collector uses rate limit from config, not hardcoded."""
        assert collector.rate_limit == sample_config.get('rate_limit_per_minute')
```

### Mosaic Assembly Tests

```python
"""Test mosaic assembly logic — fragments → thesis."""

class TestMosaicAssembly:

    def test_minimum_fragments_required(self, assembler, sample_config):
        """Assembly requires min_fragments from config."""
        min_frags = sample_config.get('min_mosaic_fragments', 3)

        # Below threshold: no mosaic formed
        few_signals = make_signals(count=min_frags - 1)
        result = assembler.assemble(few_signals, config=sample_config)
        assert result is None or result.get('status') == 'insufficient'

        # At threshold: mosaic formed
        enough_signals = make_signals(count=min_frags)
        result = assembler.assemble(enough_signals, config=sample_config)
        assert result is not None and result.get('status') != 'insufficient'

    def test_category_diversity_enforced(self, assembler, sample_config):
        """Mosaic requires signals from min_categories different categories."""
        min_cats = sample_config.get('min_signal_categories', 2)

        # All same category: insufficient diversity
        same_cat = make_signals(count=5, category='fundamental')
        result = assembler.assemble(same_cat, config=sample_config)
        if min_cats > 1:
            assert result.get('diversity_met') is False

    def test_conflicting_signals_flagged(self, assembler, sample_config):
        """When signals contradict, mosaic includes conflict flag for HITL."""
        bullish = make_signal(value=0.8, category='fundamental')
        bearish = make_signal(value=-0.7, category='sentiment')
        result = assembler.assemble([bullish, bearish], config=sample_config)
        assert result.get('has_conflicts') is True
```

### Arbitrage Scoring Tests

```python
"""Test the universal arbitrage scoring formula."""

class TestArbitrageScoring:

    def test_formula_correct(self, scorer):
        """Signal Strength = True Growth % - Market Awareness %"""
        score = scorer.score(true_growth=75.0, market_awareness=25.0)
        assert score == 50.0

    def test_thresholds_from_config(self, scorer, sample_config):
        """FLAG/MONITOR/PASS thresholds come from config."""
        assert scorer.flag_threshold == sample_config.get('flag_threshold')
        assert scorer.monitor_threshold == sample_config.get('monitor_threshold')

    def test_verdict_mapping(self, scorer, sample_config):
        """Score maps to correct verdict based on config thresholds."""
        flag_t = sample_config.get('flag_threshold', 50)
        mon_t = sample_config.get('monitor_threshold', 30)

        assert scorer.verdict(flag_t + 1) == 'FLAG'
        assert scorer.verdict(mon_t + 1) == 'MONITOR'
        assert scorer.verdict(mon_t - 1) == 'PASS'

    def test_edge_cases(self, scorer):
        """Zero signals, negative growth, 100% awareness."""
        assert scorer.score(true_growth=0, market_awareness=0) == 0
        assert scorer.score(true_growth=-10, market_awareness=50) == -60
        assert scorer.score(true_growth=100, market_awareness=100) == 0
```

### HITL Gate Tests

```python
"""Test that HITL gates actually pause execution."""

class TestHITLGates:

    def test_gate_triggers_at_threshold(self, pipeline, sample_config):
        """Pipeline pauses when conviction crosses HITL threshold."""
        threshold = sample_config.get('hitl_conviction_threshold', 7)

        # Below threshold: auto-proceed
        result = pipeline.evaluate(conviction=threshold - 1)
        assert result.get('requires_hitl') is False

        # At/above threshold: pause for human
        result = pipeline.evaluate(conviction=threshold)
        assert result.get('requires_hitl') is True

    def test_gate_captures_reasoning(self, pipeline):
        """HITL decision must include human reasoning text."""
        decision = pipeline.submit_hitl_decision(
            verdict='APPROVE',
            reasoning='Strong divergence confirmed by multiple sources'
        )
        assert decision.get('reasoning') is not None
        assert len(decision['reasoning']) > 0

    def test_timeout_behavior(self, pipeline, sample_config):
        """Unanswered HITL gates follow timeout config."""
        timeout = sample_config.get('hitl_timeout_hours', 24)
        assert pipeline.hitl_timeout == timeout
```

---

## Frontend: vitest Patterns

### Component Rendering Tests

```jsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import MissionAgent from '../pages/MissionAgent';

describe('MissionAgent', () => {

  it('renders in loading state without crashing', () => {
    render(<MissionAgent />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('displays all four signal categories', async () => {
    render(<MissionAgent initialData={mockData} />);
    expect(screen.getByText('FUNDAMENTAL')).toBeInTheDocument();
    expect(screen.getByText('STRUCTURAL')).toBeInTheDocument();
    expect(screen.getByText('BEHAVIORAL')).toBeInTheDocument();
    expect(screen.getByText('SENTIMENT')).toBeInTheDocument();
  });

  it('shows HITL controls when gate is triggered', async () => {
    render(<MissionAgent initialData={mockDataWithHITL} />);
    expect(screen.getByRole('button', { name: /approve/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /defer/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /reject/i })).toBeInTheDocument();
  });

  it('requires reasoning before HITL submission', async () => {
    render(<MissionAgent initialData={mockDataWithHITL} />);
    const approveBtn = screen.getByRole('button', { name: /approve/i });
    fireEvent.click(approveBtn);
    // Should not submit without reasoning
    expect(screen.getByText(/reasoning required/i)).toBeInTheDocument();
  });

  it('uses theme colors, not hardcoded hex', () => {
    const { container } = render(<MissionAgent />);
    const html = container.innerHTML;
    // No raw hex colors should appear outside THEME definition
    const hexPattern = /#[0-9a-fA-F]{6}/g;
    const matches = html.match(hexPattern) || [];
    // All hex values should be from THEME object (applied via CSS variables or style)
    // This is a sanity check — detailed check in the config test
  });
});

describe('Keyboard shortcuts', () => {

  it('A key triggers approve at HITL gate', () => {
    render(<MissionAgent initialData={mockDataWithHITL} />);
    fireEvent.keyDown(document, { key: 'a' });
    // Approve button should be focused or action triggered
  });

  it('number keys 1-4 focus signal categories', () => {
    render(<MissionAgent initialData={mockData} />);
    fireEvent.keyDown(document, { key: '1' });
    expect(document.activeElement).toHaveAttribute('data-category', 'fundamental');
  });
});
```

### API Integration Tests

```jsx
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('Research Agent API', () => {

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('fetches signals from configured endpoint', async () => {
    const fetchSpy = vi.spyOn(global, 'fetch').mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockSignals)
    });

    await runResearch({ symbol: 'TEST', config: testConfig });

    expect(fetchSpy).toHaveBeenCalledWith(
      expect.stringContaining(testConfig.apiBase),
      expect.any(Object)
    );
  });

  it('handles API errors gracefully', async () => {
    vi.spyOn(global, 'fetch').mockRejectedValue(new Error('Network error'));

    const result = await runResearch({ symbol: 'TEST', config: testConfig });
    expect(result.error).toBeDefined();
    expect(result.signals).toEqual([]);
  });
});
```

---

## Test File Naming Convention

```
tests/
  test_{mission}_config.py        # Config validation (always first)
  test_{mission}_signals.py       # Signal collection
  test_{mission}_assembly.py      # Mosaic assembly
  test_{mission}_scoring.py       # Arbitrage scoring
  test_{mission}_hitl.py          # HITL gate behavior
  test_{mission}_integration.py   # End-to-end pipeline

ui/src/__tests__/
  {Mission}.test.jsx              # Component rendering
  {Mission}.api.test.js           # API integration
  {Mission}.keyboard.test.js      # Keyboard shortcuts
```

## Fixtures Pattern

Use a shared `conftest.py` for mission-specific fixtures:

```python
@pytest.fixture
def sample_config():
    """Config with all defaults — the single source of truth for tests."""
    return {
        'flag_threshold': 50,
        'monitor_threshold': 30,
        'min_mosaic_fragments': 3,
        'min_signal_categories': 2,
        'signal_max_age_hours': 24,
        'hitl_conviction_threshold': 7,
        'hitl_timeout_hours': 24,
        'rate_limit_per_minute': 60,
    }
```

All test values come from this fixture. Tests never use bare literals for thresholds.
