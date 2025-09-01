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

Stay simple, teach as we go. Physics By: You and I.

---

Drift tracking (new)
- Purpose: estimate frequency drift over time near a target (default 7,467.8 Hz) from WAV or TXT data.
- Run examples:
  - python scripts/drift_tracker.py --input path/to/file.wav --target 7467.8 --band 10 --window 2.0 --step 0.25 --out-csv output/drift.csv --out-plot output/drift.png
  - python scripts/drift_tracker.py --input path/to/samples.txt --sample-rate 48000 --focus --out-plot output/drift.png
- Outputs:
  - CSV with time_s, peak_hz, amplitude, drift_ppm
  - Optional PNG plot showing drift over time (and a compact spectrum view)

Automation (labels, project, relay)
- PR auto-labeler: labels changes based on file paths (see .github/labeler.yml).
- Issues triage: new issues get the "triage" label; titles starting with "Review:" also get "review".
- Project auto-add (optional): if you create a GitHub Project and set repo secrets, new issues/PRs will be auto-added (see docs/PROJECTS_SETUP.md).
- Relay to next: close an issue with the label "relay" to automatically open a follow-up issue that links back.
