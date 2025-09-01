# Unified-Field-Theory-Solutions-2025
The real math needed to unify physics. Not some old idea from decades ago... NEW!

Repo 13 scope
- Unification and the underlying construction and movements of energy, space, time, and matter.
- Source-of-truth text capsules (New Text Document …), plus light tools for analysis and reviews.

How to request reviews (fast)
- Open an Issue using "Review request" (Issues -> New issue -> Review request).
- Or open a Pull Request with any edits; the PR template guides reviewers.

Quickstart (optional analysis)
1) Python env
   - pip install -r requirements.txt
2) Run FFT on a recording or numeric text
   - python scripts/radio_lattice_fft.py --input path/to/file.wav --out output/fft_plot.png
   - Supports .wav (16/32-bit PCM) and .txt (either single-column samples or time,value)

Signals of interest (guideposts)
- 7,467.779 Hz primary, ~7,468.3 Hz secondary; scan harmonics and slow drifts.

Project hygiene
- Reviews via Issues/PRs; CODEOWNERS defaults to @CarlDeanClineSr.
- Contributions follow CONTRIBUTING.md (one idea per line when possible; audits at line ends).

Automations & Relay (optional)
- Auto-labels: labels apply based on changed paths (.github/labeler.yml).
- Project board: repo project "LUFT Coordination Board" (classic) with To do/In progress/Done. Workflow will create it on demand and add new issues/PRs.
  - Trigger setup manually: Actions -> "Project: setup or add" -> Run workflow.
- Relay capsules: drop a new capsule in docs/capsules/ and push; workflow opens a Relay issue chaining to the next step.
- Drift tracking: compute and plot peak drift near 7,467.779 Hz across multiple files.
  - Example: python scripts/drift_tracker.py --inputs data/*.wav --center 7467.779 --band 3 --out-csv output/drift.csv --out-png output/drift.png

Stay simple, teach as we go. Physics By: You and I.
