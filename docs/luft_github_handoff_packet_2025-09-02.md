# 📦 LUFT GitHub Handoff Packet — Sep 02 2025

Drop this straight into your repo or paste into an issue so `ai-copilot-github` can rejoin the relay without reconstructing the past few days.

---

## Capsule Summaries

**Capsule 000 — Drift Tracking (Baseline)**  
- Objective: Monitor a steady tone at **7,467.779 Hz** for 60 s and measure any frequency drift (“foam drift”).  
- Deliverables: Drift plot (Hz vs. time), five-field ledger entry.  
- Status: Baseline run defined, awaiting first data.

**Capsule 001 — Perturbation Sweep**  
- Objective: Repeat Capsule 000 but change **one condition per run** (temperature, power source, mic distance, speaker orientation, nearby electronics).  
- Deliverables: Table of conditions vs. drift, short “what changed/what stayed” note, plot(s).  
- Status: Instructions and ledger template ready; baseline run to be logged.

**Capsule 004 — Replication Invite**  
- Objective: Independent replication of Capsule 001 on different hardware/room.  
- Deliverables: Same as Capsule 001, plus side-by-side comparison with Carl’s results.  
- Status: Invite text drafted; to be posted in issue #6 tagging collaborators.

---

## Current PR / Issue Links

- **PR #4** — Add initial AI relay capsule (Capsule 000) and kickoff checklist  
  - Contains: Capsule 000 description, ledger template, Underlay vocab.  
  - Status: Ready for review/merge after baseline data.

- **Issue #6** — Review request: Drift tracking setup and relay flow  
  - Use for: Posting Capsule 001 results, Capsule 004 replication, and feedback loop.

---

## SM Delta Map v0.1 — Collider Benchmark

Parameters:  
- η = −0.05  
- n = 2  
- BR_inv = 0.05 (5 % invisible width)  
- v = 246 GeV

Couplings:  
| κ_t   | κ_b   | κ_τ   | κ_V   | κ_γ    |
|-------|-------|-------|-------|--------|
| 0.9750| 1.0000| 1.0000| 1.0000| 1.0068 |

Width scale: 0.9325

Signal strengths μ:  
| Channel       | μ Value | Shift vs SM |
|---------------|---------|-------------|
| ggF → ZZ      | 0.956   | −4.4 %      |
| ggF → γγ      | 0.970   | −3.0 %      |
| VBF → γγ      | 1.018   | +1.8 %      |
| VH → bb       | 1.004   | +0.4 %      |

Interpretation:  
- ggF suppression from κ_t < 1  
- VBF → γγ enhancement from reduced destructive interference  
- Invisible width damps all μ slightly

---

## Five-Field Ledger Template (Self-Contained)

```markdown
# Capsule Ledger Entry
- **Who and when**: [Your Name], [Timestamp, e.g., 2025-09-02 19:37 UTC]
- **Setup**: [Source, e.g., phone speaker], [Mic/Sensor, e.g., laptop mic], [Room notes, e.g., quiet home office]
- **Measured**: [Main value(s), e.g., Drift = +0.015 Hz over 60 s], [Units, e.g., Hz]
- **Checks**: [Conservation/sanity, e.g., Noise floor < 0.010 Hz, stable for 30 s]
- **Notes**: [New thing learned], [Next test], [Attachments if any]
```

---

## Next Actions for `ai-copilot-github`

1. Merge PR #4 after Capsule 000 baseline data is attached.  
2. Run/log Capsule 001 baseline and perturbations; post in issue #6.  
   - Baseline: 7,467.779 Hz, 60 s, log drift.  
   - Perturbations: One change per run (temperature, power, distance, orientation, electronics), table drift shifts.  
3. Post Capsule 004 invite in issue #6 tagging collaborators (e.g., `@xAICollaborator`):
   ```markdown
   Hey [@xAICollaborator] — could you replicate Capsule 001 as Capsule 004 on your hardware/room?
   - Tone 7,467.779 Hz, 60 s runs
   - Change one variable per run (temperature, power, distance, orientation, nearby electronics)
   - Use the five-field ledger above
   - Share a drift table + one plot
   - Compare side-by-side with Carl’s Capsule 001 (note matches/differences)
   - Post in issue #6
   Thank you!
   ```
4. Keep SM Delta Map v0.1 in collider ledger for Run 3 comparisons.

---

## Pivot Options

- Capsule 003 (Two-tone Beats): Mix 7,467.7 Hz and 7,468.0 Hz, audit beat patterns.  
- Deepen 001 (Humidity): Add humidity perturbation, log drift shift.  
- Audit vs. Data: Match 001 drift to JWST z anomalies or NA62 decay rates.

---

Signal’s live at 12:37 PM PDT, 2025-09-02 (19:37 UTC). Timebase: UTC for all logs.
