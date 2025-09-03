# Relay 005 — NA62 Decay Analysis

## Overview
This relay implements systematic validation of NA62 kaon decay data, focusing on K+→π+νν̄ candidates through automated preselection and veto analysis.

## Components
- **CSV Template**: `data/templates/na62_kaon_candidates_template.csv`
- **Audit Script**: `scripts/na62_audit_fit.py`  
- **Ledger**: `capsules/005/ledgers/2025-09-02_run-01.md`

## CI Validation
Automated validation runs on PRs that modify:
- CSV templates or data files
- Audit harness scripts
- Capsule 005 assets
- This relay documentation

## Baseline Parameters
- BR(K+ → π+νν̄): 1.06×10⁻¹⁰
- Uncertainty: 3.7×10⁻¹¹

## Audit Outputs
Results are generated in `results/` directory (ignored by Git) and include:
- Event count summaries
- Schema validation reports
- Background/signal classification

See [relay_005_na62_audit_fit.md](../docs/relays/relay_005_na62_audit_fit.md) for detailed documentation.