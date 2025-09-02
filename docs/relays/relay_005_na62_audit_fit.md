# Relay 005: NA62 Audit Fit

**Purpose**: Demonstrate unified ledger logic for ultra-rare K+ → π+νν̄ decay analysis, showing how the same audit framework scales from capsule-level audio drift to particle physics event counting.

## Input Data

**Source**: `data/templates/na62_kaon_candidates_template.csv`

Expected columns: run_id, event_id, E_in_GeV, p_in_GeV, E_out_pi_GeV, p_out_pi_GeV, passed_veto, classification, weight, source_url, notes

## Audit Checks

### Energy/Momentum Consistency
- Verify E² - p²c² = m²c⁴ for incoming kaon
- Check momentum conservation: p_in = p_out_pi + p_missing  
- Validate energy conservation within detector resolution
- Flag events with >3σ deviations for review

### Event Classification 
- **Signal candidates**: passed_veto=true, classification=signal
- **Background events**: classification=background or sidebands
- **Uncertain events**: classification=candidate, require additional review

### Background vs Signal Tagging
- Count events per classification category
- Calculate signal/background ratios per run
- Track veto system efficiency (passed_veto rates)
- Monitor for systematic shifts between runs

## Ledger Fields

Each event generates a unified ledger entry:
```
timestamp: [event_time_UTC]
setup: NA62_run_[run_id]_kaon_beam
measured: candidate_event_E[energy]_p[momentum]
checks: [conservation_status]
classification: [signal/background/candidate]
weight: [detection_weight]
source_url: cern.ch/NA62/run_[run_id]/event_[event_id]
notes: [any_anomalies_or_flags]
```

## Output

**Rate Table**: Counts per classification bin:
```
| Run ID | Signal | Background | Candidate | Total | S/B Ratio |
|--------|--------|------------|-----------|-------|-----------|
| 001    | 3      | 847        | 12        | 862   | 0.0035    |
| 002    | 1      | 923        | 8         | 932   | 0.0011    |
```

**Summary Note** (5 sentences):
Analysis of [N] events from NA62 runs shows [X] signal candidates with energy-momentum conservation validated to [Y]σ precision. Background rates of [Z] events per run remain consistent with Standard Model predictions. Veto system efficiency maintained at [A]% across all runs. No significant systematic deviations observed in momentum spectra. Results support ultra-rare decay branch ratio of [B] ± [C] consistent with theoretical expectations.