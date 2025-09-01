#!/usr/bin/env python3
"""
Radio/Lattice FFT helper (Repo 13)
- Inputs: WAV audio or TXT numeric
  * WAV: reads mono/stereo PCM and auto-selects a channel
  * TXT: either single-column samples or two columns (time,value)
- Outputs: prints top peaks and optionally saves a PNG plot
"""
from __future__ import annotations
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional

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
        arr = np.atleast_2d(arr)
        if arr.shape[1] == 1:
            if sample_rate is None:
                raise ValueError("For single-column TXT, --sample-rate is required (Hz).")
            return arr[:, 0].astype(np.float64), float(sample_rate)
        elif arr.shape[1] >= 2:
            t = arr[:, 0].astype(np.float64)
            x = arr[:, 1].astype(np.float64)
            # Infer sampling rate from time spacing
            dt = np.median(np.diff(t))
            if dt <= 0:
                raise ValueError("Non-increasing time column; cannot infer sample rate.")
            fs = 1.0 / dt
            return x, float(fs)
        else:
            raise ValueError("Unrecognized TXT format.")


def compute_spectrum(x: np.ndarray, fs: float) -> Tuple[np.ndarray, np.ndarray]:
    n = len(x)
    # Detrend and window
    x = x - np.mean(x)
    window = np.hanning(n)
    xw = x * window
    # FFT
    spec = np.fft.rfft(xw)
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    # Scale to approximate amplitude spectrum
    amp = (2.0 / np.sum(window)) * np.abs(spec)
    return freqs, amp


def find_peaks(freqs: np.ndarray, amp: np.ndarray, k: int = 5,
               fmin: Optional[float] = None, fmax: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
    mask = np.ones_like(freqs, dtype=bool)
    if fmin is not None:
        mask &= freqs >= fmin
    if fmax is not None:
        mask &= freqs <= fmax
    f = freqs[mask]
    a = amp[mask]
    if len(a) == 0:
        return np.array([]), np.array([])
    idx = np.argpartition(a, -min(k, len(a)))[-min(k, len(a)):]
    order = np.argsort(a[idx])[::-1]
    top_idx = idx[order]
    return f[top_idx], a[order]


def main():
    ap = argparse.ArgumentParser(description="FFT peak scan for lattice signals")
    ap.add_argument("--input", required=True, help="Path to .wav or .txt file")
    ap.add_argument("--sample-rate", type=float, default=None, help="Hz (needed for single-column TXT)")
    ap.add_argument("--fmin", type=float, default=None, help="Min freq to report (Hz)")
    ap.add_argument("--fmax", type=float, default=None, help="Max freq to report (Hz)")
    ap.add_argument("--peaks", type=int, default=5, help="Number of peaks to list (default 5)")
    ap.add_argument("--out", default=None, help="Optional PNG path to save the spectrum plot")
    ap.add_argument("--focus", action="store_true",
                    help="Zoom plot around 7460–7480 Hz for quick lattice inspection")
    args = ap.parse_args()

    x, fs = load_data(args.input, args.sample_rate)
    freqs, amp = compute_spectrum(x, fs)
    pf, pa = find_peaks(freqs, amp, k=args.peaks, fmin=args.fmin, fmax=args.fmax)

    print(f"File: {args.input}")
    print(f"Samples: {len(x)}, fs: {fs:.3f} Hz")
    if len(pf) == 0:
        print("No peaks found in the selected band.")
    else:
        print("Top peaks (Hz : amplitude):")
        for f, a in zip(pf, pa):
            print(f"  {f:12.3f} : {a:.6e}")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(freqs, amp, lw=0.9)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (arb.)")
    plt.title("Amplitude Spectrum")
    if args.focus:
        plt.xlim(7460, 7480)
    plt.grid(alpha=0.3)
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        plt.savefig(args.out, dpi=160, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    main()