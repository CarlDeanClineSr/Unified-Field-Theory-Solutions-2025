# Relay 005 — NA62 Decay

## Overview
NA62 kaon decay analysis focusing on K+→π+νν̄ candidates through systematic preselection and veto processes.

## Data Sources
- Template: data/templates/na62_kaon_candidates_template.csv
- Analysis: NA62 experimental data with event classification

## Analysis Pipeline
1. Load candidate events from CSV template
2. Apply preselection criteria
3. Execute veto processes
4. Generate audit summary

## Baseline Parameters
- BR baseline: 1.06e-10
- Sigma baseline: 3.7e-11

## References
- Capsule: capsules/005/
- Documentation: docs/relays/relay_005_na62_audit_fit.md