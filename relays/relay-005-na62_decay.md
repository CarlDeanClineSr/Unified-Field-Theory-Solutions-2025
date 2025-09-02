# Relay 005 — NA62 K⁺ → π⁺ ν ν̄ Audit (with Foam Modulation Check)

Objective
- Audit a curated, human-reviewed set of NA62 K⁺ → π⁺ ν ν̄ candidate events against the public baseline branching ratio.
- Produce a compact result block (observed signal weight, total weight, observed rate, χ² vs baseline) and log it to a run ledger.
- Wire in a Foam Audit lane so Δρ/ρ_avg and χ_mod fits are recorded from run one, enabling modulation hypothesis testing as data accrues.

Inputs
- CSV (contributors' template): data/templates/na62_kaon_candidates_template.csv
  - Columns (required unless noted):
    - run_id, event_id
    - E_in_GeV, p_in_GeV
    - E_out_pi_GeV, p_out_pi_GeV
    - passed_veto (true/false)
    - classification (signal/background/uncertain)
    - weight (float, default 1.0)
    - source_url (reference)
    - notes (free text)

Outputs
- When executed locally, the audit script emits to results/:
  - results/na62_audit_summary.json (machine‑readable)
  - results/na62_audit_summary.md (compact paste‑ready block)
- Ledger entries live under: capsules/005/ledgers/

Method (compact)
1) Load candidates and filter to passed_veto == true.
2) Observed signal weight = sum(weight | classification == "signal" & passed_veto).
3) Total weight = sum(weight | passed_veto).
4) Observed rate (toy) = observed_signal_weight / total_weight.
5) Compare to NA62 baseline branching ratio (baseline_br ± baseline_sigma) via χ² = ((obs − br)/sigma)².
6) Emit summary and notes for ledger logging.

Baseline (quick‑audit defaults, override via env)
- NA62_BASELINE_BR = 1.06e-10  # 10.6 × 10^-11
- NA62_BASELINE_SIGMA = 3.7e-11 # conservative uncertainty bucket for harness checks

Foam Audit lane (run‑level fields)
- Δρ/ρ_avg (dimensionless)
- χ_mod (goodness‑of‑fit for modulation model)
- Fit metadata (method, windows/bins, notes)
- These are recorded in each ledger under "Foam Audit". The audit script accepts optional foam values via CLI flags or environment variables so they can be surfaced in the summary.

Usage
- Populate/append data/templates/na62_kaon_candidates_template.csv with curated events.
- Run:
  - python scripts/na62_audit_fit.py \
    --csv data/templates/na62_kaon_candidates_template.csv \
    --out results \
    [--foam-delta-rho-over-rho-avg 0.0] [--foam-chi-mod 0.0]
- Or via env:
  - FOAM_DELTA_RHO_OVER_RHO_AVG=... FOAM_CHI_MOD=... NA62_BASELINE_BR=... NA62_BASELINE_SIGMA=... python scripts/na62_audit_fit.py

Next steps
- Replace sample rows with real candidate entries (first 30–51 from NA62 public releases) and iterate ledgers.
- Add physics cuts (missing mass, π⁺ momentum windows) and enhance the foam fit procedure.
- Use the ledger cadence to pivot to Relay 006/007 without losing continuity.

References
- NA62 collaboration public releases and combined analyses (keep exact citations in the ledger notes per run).