# NA62 Candidate Curation Guide (Relay 005)

Purpose
- Capture a first tranche (30–51) of public K⁺ → π⁺ ν ν̄ candidate events for quick audit and foam‑fit checks.

Source material
- Use NA62 public releases and auxiliary material. Record a source_url for each row and keep full citations in the run ledger.

How to curate
1) Start with data/na62/curated_candidates.csv (header only).
2) Append rows with the required fields:
   - run_id: 2025-09-03_run-02 (or current run id)
   - event_id: the public event id (or traced identifier)
   - E_in_GeV, p_in_GeV: kaon beam estimates
   - E_out_pi_GeV, p_out_pi_GeV: reconstructed π⁺ energy/momentum
   - passed_veto: true if event passes published veto criteria
   - classification: signal/background/uncertain (human judgement; keep notes)
   - weight: default 1.0 unless noted
   - source_url: permalink to the NA62 communication/plot/listing
   - notes: brief context or selection remarks
3) After 30–51 rows are entered and checked, run the audit harness locally to generate a summary (do not commit results/ outputs).

Foam Audit
- From run two onward, log:
  - Δρ/ρ_avg (dimensionless)
  - χ_mod (goodness‑of‑fit for modulation model)
  - Fit method, windows/bins, notes
- Add these to the ledger for the run.

Commit discipline
- Commit the CSV and the run ledger.
- Do not commit results/ outputs; they are ignored by .gitignore and published via CI artifacts if needed.