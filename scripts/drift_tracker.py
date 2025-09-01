#!/usr/bin/env python3
"""
Drift tracker for lattice signals (Repo 13)
- Inputs: WAV audio or TXT numeric (single-column samples with --sample-rate, or two columns time,value)
- Method: sliding-window FFT around a target frequency; extracts peak per window
- Outputs: CSV with time_s, peak_hz, amplitude, drift_ppm; optional PNG plot
"""
from __future__ import annotations
import argparse
import os
from typing import Optional, Tuple, List

import numpy as np
import matplotlib.pyplot as plt

try:
    from scipy.io import wavfile
except ImportError:
    wavfile = None


def load_data(path: str, sample_rate: Optional[float]) -> Tuple[np.ndarray, float]:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".wav":
        if wavfile is None:
            raise RuntimeError("scipy is required for WAV input: pip install scipy")
        fs, data = wavfile.read(path)
        # Normalize to float
        if data.dtype.kind in ("i", "u"):
            max_int = np.iinfo(data.dtype).max
            data = data.astype(np.float64) / max_int
        elif data.dtype.kind == "f":
            data = data.astype(np.float64)
        # If stereo, pick channel with largest variance
        if data.ndim == 2 and data.shape[1] > 1:
            variances = [np.var(data[:, i]) for i in range(data.shape[1])]
            ch = int(np.argmax(variances))
            data = data[:, ch]
        return data, float(fs)
    else:
        arr = np.loadtxt(path)
        if arr.ndim == 1:
            # Single column data
            if sample_rate is None:
                raise ValueError("For single-column TXT, --sample-rate is required (Hz).")
            return arr.astype(np.float64), float(sample_rate)
        else:
            arr = np.atleast_2d(arr)
            if arr.shape[1] == 1:
                if sample_rate is None:
                    raise ValueError("For single-column TXT, --sample-rate is required (Hz).")
                return arr[:, 0].astype(np.float64), float(sample_rate)
            elif arr.shape[1] >= 2:
                t = arr[:, 0].astype(np.float64)
                x = arr[:, 1].astype(np.float64)
                dt_vals = np.diff(t)
                dt_vals = dt_vals[dt_vals > 0]  # Remove any non-positive differences
                if len(dt_vals) == 0:
                    raise ValueError("Non-increasing time column; cannot infer sample rate.")
                dt = np.median(dt_vals)
                if dt <= 0:
                    raise ValueError("Non-increasing time column; cannot infer sample rate.")
                fs = 1.0 / dt
                return x, float(fs)
            else:
                raise ValueError("Unrecognized TXT format.")


def sliding_peak_drift(x: np.ndarray, fs: float, target: float, band: float,
                        window_s: float, step_s: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = len(x)
    nwin = max(8, int(round(window_s * fs)))
    nstep = max(1, int(round(step_s * fs)))
    start_idx = np.arange(0, max(1, n - nwin + 1), nstep)
    times = []
    peaks_hz = []
    amps = []
    for s in start_idx:
        e = s + nwin
        if e > n:
            break
        seg = x[s:e]
        seg = seg - np.mean(seg)
        w = np.hanning(len(seg))
        segw = seg * w
        spec = np.fft.rfft(segw)
        freqs = np.fft.rfftfreq(len(segw), d=1.0 / fs)
        amp = (2.0 / np.sum(w)) * np.abs(spec)
        fmin = max(0.0, target - band / 2.0)
        fmax = target + band / 2.0
        m = (freqs >= fmin) & (freqs <= fmax)
        if not np.any(m):
            continue
        local_amp = amp[m]
        local_freqs = freqs[m]
        k = int(np.argmax(local_amp))
        # Quadratic interpolation around the peak for sub-bin accuracy when possible
        if 0 < k < len(local_amp) - 1:
            y0, y1, y2 = local_amp[k - 1], local_amp[k], local_amp[k + 1]
            denom = (y0 - 2 * y1 + y2)
            if denom != 0:
                delta = 0.5 * (y0 - y2) / denom
            else:
                delta = 0.0
            df = (local_freqs[1] - local_freqs[0])
            f_peak = local_freqs[k] + delta * df
            a_peak = y1 - 0.25 * (y0 - y2) * delta
        else:
            f_peak = local_freqs[k]
            a_peak = local_amp[k]
        t_mid = (s + e) / 2.0 / fs
        times.append(t_mid)
        peaks_hz.append(f_peak)
        amps.append(a_peak)
    return np.asarray(times), np.asarray(peaks_hz), np.asarray(amps)


def save_csv(path: str, t: np.ndarray, f: np.ndarray, a: np.ndarray, target: float) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    drift_ppm = (f - target) / target * 1e6
    data = np.column_stack([t, f, a, drift_ppm])
    header = "time_s,peak_hz,amplitude,drift_ppm"
    np.savetxt(path, data, delimiter=",", header=header, comments="", fmt=["%.6f", "%.6f", "%.6e", "%.3f"])


def plot_drift(path: Optional[str], t: np.ndarray, f: np.ndarray, target: float,
               band: float, spec_hint: Optional[Tuple[np.ndarray, np.ndarray]] = None,
               title: str = "Frequency Drift") -> None:
    if not path:
        return
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    plt.figure(figsize=(10, 6))
    if spec_hint is not None:
        tfreqs, tmag = spec_hint
        # Plot a faint background of the mean spectrum in the band as context if provided
        plt.plot(tfreqs, tmag, color="gray", lw=0.8, alpha=0.4, label="Band spectrum")
    plt.plot(t, f, ".-", lw=1.0, ms=3.0, label="Peak")
    plt.axhline(target, color="tab:red", ls="--", lw=1, label=f"target {target:.3f} Hz")
    plt.ylim(target - band / 2.0, target + band / 2.0)
    plt.xlabel("Time (s)")
    plt.ylabel("Peak frequency (Hz)")
    plt.title(title)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=160)


def main():
    ap = argparse.ArgumentParser(description="Track drift near a target frequency over time")
    ap.add_argument("--input", required=True, help="Path to .wav or .txt file")
    ap.add_argument("--sample-rate", type=float, default=None, help="Hz (needed for single-column TXT)")
    ap.add_argument("--target", type=float, default=7467.8, help="Target frequency (Hz)")
    ap.add_argument("--band", type=float, default=10.0, help="Band width around target (Hz)")
    ap.add_argument("--window", type=float, default=2.0, help="Sliding window length (s)")
    ap.add_argument("--step", type=float, default=0.25, help="Step between windows (s)")
    ap.add_argument("--out-csv", default="output/drift.csv", help="CSV path to save drift data")
    ap.add_argument("--out-plot", default="output/drift.png", help="PNG path to save drift plot")
    ap.add_argument("--focus", action="store_true", help="Focus y-axis on target±band/2")
    args = ap.parse_args()

    x, fs = load_data(args.input, args.sample_rate)

    t, f, a = sliding_peak_drift(x, fs, args.target, args.band, args.window, args.step)

    if len(t) == 0:
        print("No windows processed. Check input length or parameters.")
        return

    # Save CSV
    save_csv(args.out_csv, t, f, a, args.target)

    # Summaries
    fmin, fmax = float(np.min(f)), float(np.max(f))
    fmed = float(np.median(f))
    print(f"Windows: {len(t)}  fs: {fs:.3f} Hz  target: {args.target:.3f} Hz  band: ±{args.band/2:.3f} Hz")
    print(f"Peak Hz: min={fmin:.3f}, median={fmed:.3f}, max={fmax:.3f}, range={fmax-fmin:.3f} Hz")

    # Optional band spectrum snapshot for context
    # Compute a single full-record spectrum and crop to the band
    x0 = x - np.mean(x)
    w = np.hanning(len(x0))
    spec = np.fft.rfft(x0 * w)
    freqs = np.fft.rfftfreq(len(x0), d=1.0 / fs)
    amp = (2.0 / np.sum(w)) * np.abs(spec)
    m = (freqs >= (args.target - args.band/2)) & (freqs <= (args.target + args.band/2))
    spec_hint = (freqs[m], amp[m]) if np.any(m) else None

    # Plot
    plot_drift(args.out_plot, t, f, args.target, args.band if args.focus else (max(f) - min(f) + 1.0), spec_hint=spec_hint,
               title="Frequency Drift Near Target")


if __name__ == "__main__":
    main()