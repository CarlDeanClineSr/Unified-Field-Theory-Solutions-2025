#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

import pandas as pd


def main(csv_path: str, out_dir: str, foam_delta_rho_over_rho_avg: float | None, foam_chi_mod: float | None, foam_notes: str | None):
    # Baseline (overridable via env)
    baseline_br = float(os.getenv("NA62_BASELINE_BR", 1.06e-10))      # 10.6 x 10^-11
    baseline_sigma = float(os.getenv("NA62_BASELINE_SIGMA", 3.7e-11)) # quick-audit bucket

    # Allow foam metrics from env if not provided via CLI
    if foam_delta_rho_over_rho_avg is None:
        foam_delta_rho_over_rho_avg = os.getenv("FOAM_DELTA_RHO_OVER_RHO_AVG")
        foam_delta_rho_over_rho_avg = float(foam_delta_rho_over_rho_avg) if foam_delta_rho_over_rho_avg not in (None, "") else None
    if foam_chi_mod is None:
        foam_chi_mod = os.getenv("FOAM_CHI_MOD")
        foam_chi_mod = float(foam_chi_mod) if foam_chi_mod not in (None, "") else None
    if foam_notes is None:
        foam_notes = os.getenv("FOAM_NOTES")

    df = pd.read_csv(csv_path)

    # Normalize booleans for veto
    df["passed_veto"] = df["passed_veto"].astype(str).str.lower().isin(["1", "true", "t", "yes", "y"])
    passed = df[df["passed_veto"] == True].copy()

    # Weights
    passed["w"] = pd.to_numeric(passed.get("weight", 1.0), errors="coerce").fillna(1.0)

    # Classification (case-insensitive)
    cls = passed.get("classification", pd.Series(["uncertain"] * len(passed)))
    cls = cls.astype(str).str.lower().fillna("uncertain")

    obs_signal_w = passed.loc[cls == "signal", "w"].sum()
    total_w = passed["w"].sum()
    observed_rate = float(obs_signal_w / total_w) if total_w > 0 else 0.0

    # χ² vs baseline (toy)
    chi2 = ((observed_rate - baseline_br) / baseline_sigma) ** 2 if baseline_sigma > 0 else float("nan")

    summary = {
        "input_csv": str(csv_path),
        "n_rows": int(len(df)),
        "n_passed_veto": int(len(passed)),
        "obs_signal_weight": float(obs_signal_w),
        "total_weight": float(total_w),
        "observed_rate": observed_rate,
        "baseline_br": baseline_br,
        "baseline_sigma": baseline_sigma,
        "chi2_vs_baseline": chi2,
        # Optional Foam Audit fields (run-level)
        "foam_delta_rho_over_rho_avg": float(foam_delta_rho_over_rho_avg) if foam_delta_rho_over_rho_avg is not None else None,
        "foam_chi_mod": float(foam_chi_mod) if foam_chi_mod is not None else None,
        "foam_notes": foam_notes or None,
        "audit_note": "Toy calculation on curated sample; replace with real candidates and physics cuts.",
    }

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    with open(out / "na62_audit_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Markdown summary (compact)
    md_lines = [
        "# NA62 Audit Summary\n",
        f"- Input: `{csv_path}`",
        f"- Rows: {summary['n_rows']} (passed veto: {summary['n_passed_veto']})",
        f"- Observed signal weight / total weight: {obs_signal_w:.4g} / {total_w:.4g}",
        f"- Observed rate (toy): {observed_rate:.6g}",
        f"- Baseline BR: {baseline_br:.3g} ± {baseline_sigma:.2g}",
        f"- χ² vs baseline (toy): {chi2:.3g}",
    ]

    # Append Foam Audit if provided
    if summary["foam_delta_rho_over_rho_avg"] is not None or summary["foam_chi_mod"] is not None or summary["foam_notes"] is not None:
        md_lines.append("\n## Foam Audit")
        if summary["foam_delta_rho_over_rho_avg"] is not None:
            md_lines.append(f"- Δρ/ρ_avg: {summary['foam_delta_rho_over_rho_avg']}")
        if summary["foam_chi_mod"] is not None:
            md_lines.append(f"- χ_mod: {summary['foam_chi_mod']}")
        if summary["foam_notes"] is not None:
            md_lines.append(f"- Notes: {summary['foam_notes']}")

    md_lines.append("\nNote: This is a harness check on sample data. Replace with real candidates and add physics cuts (missing mass, π⁺ momentum windows).\n")

    (out / "na62_audit_summary.md").write_text("\n".join(md_lines))
    print("\n".join(md_lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="NA62 audit (toy) with optional Foam Audit fields")
    ap.add_argument("--csv", default="data/templates/na62_kaon_candidates_template.csv")
    ap.add_argument("--out", default="results")
    ap.add_argument("--foam-delta-rho-over-rho-avg", type=float, default=None, dest="foam_drho_over_rho_avg",
                    help="Optional Δρ/ρ_avg (dimensionless) to surface in the summary (or set FOAM_DELTA_RHO_OVER_RHO_AVG)")
    ap.add_argument("--foam-chi-mod", type=float, default=None, dest="foam_chi_mod",
                    help="Optional χ_mod (goodness-of-fit) to surface in the summary (or set FOAM_CHI_MOD)")
    ap.add_argument("--foam-notes", type=str, default=None, dest="foam_notes",
                    help="Optional notes for the Foam Audit section (or set FOAM_NOTES)")
    args = ap.parse_args()

    main(args.csv, args.out, args.foam_drho_over_rho_avg, args.foam_chi_mod, args.foam_notes)