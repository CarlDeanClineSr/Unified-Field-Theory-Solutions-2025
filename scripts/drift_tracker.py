#!/usr/bin/env python3
"""
Drift tracker for lattice peaks near a center frequency.
- Accepts multiple inputs (.wav or .txt time/value or sample-only with --sample-rate)
- Finds the strongest peak within a band around --center (Hz)
- Outputs CSV of (file, peak_hz, amp, timestamp) and optional PNG plot over file order
Usage:
  python scripts/drift_tracker.py --inputs data/*.wav --center 7467.779 --band 3 --out-csv output/drift.csv --out-png output/drift.png
"""
from __future__ import annotations
import argparse, glob, os, math
from typing import Optional, Tuple, List
import numpy as np
import matplotlib.pyplot as plt

try:
    from scipy.io import wavfile
except ImportError:
    wavfile = None

from radio_lattice_fft import load_data, compute_spectrum  # reuse loader if available


def load_any(path: str, sample_rate: Optional[float]):
    # Fallback to local loader to avoid circular import issues
    ext = os.path.splitext(path)[1].lower()
    if ext == '.wav':
        if wavfile is None:
            raise RuntimeError('scipy is required for WAV input: pip install scipy')
        fs, data = wavfile.read(path)
        if data.dtype.kind in ('i','u'):
            data = data.astype(np.float64) / np.iinfo(data.dtype).max
        elif data.dtype.kind == 'f':
            data = data.astype(np.float64)
        if data.ndim == 2 and data.shape[1] > 1:
            variances = [np.var(data[:, i]) for i in range(data.shape[1])]
            data = data[:, int(np.argmax(variances))]
        return data, float(fs)
    else:
        arr = np.loadtxt(path)
        arr = np.atleast_2d(arr)
        if arr.shape[1] == 1:
            if sample_rate is None:
                raise ValueError('For single-column TXT, --sample-rate is required (Hz).')
            return arr[:,0].astype(np.float64), float(sample_rate)
        else:
            t = arr[:,0].astype(np.float64)
            x = arr[:,1].astype(np.float64)
            dt = np.median(np.diff(t))
            if dt <= 0:
                raise ValueError('Non-increasing time column; cannot infer sample rate.')
            return x, float(1.0/dt)


def peak_in_band(freqs: np.ndarray, amp: np.ndarray, center: float, band: float) -> Tuple[float,float]:
    mask = (freqs >= center - band) & (freqs <= center + band)
    if not np.any(mask):
        return math.nan, math.nan
    sub_f = freqs[mask]
    sub_a = amp[mask]
    i = int(np.argmax(sub_a))
    return float(sub_f[i]), float(sub_a[i])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--inputs', nargs='+', required=True, help='Files or globs (use shell expansion)')
    ap.add_argument('--center', type=float, required=True, help='Center frequency (Hz)')
    ap.add_argument('--band', type=float, default=2.0, help='+/- band around center (Hz)')
    ap.add_argument('--sample-rate', type=float, default=None, help='Hz (needed for single-column TXT)')
    ap.add_argument('--out-csv', default=None, help='CSV output path')
    ap.add_argument('--out-png', default=None, help='PNG plot path')
    args = ap.parse_args()

    # Expand globs
    files: List[str] = []
    for pattern in args.inputs:
        matches = glob.glob(pattern)
        files.extend(matches if matches else [pattern])
    files = [f for f in files if os.path.exists(f)]
    if not files:
        raise SystemExit('No input files found.')

    rows = []
    peaks = []
    for f in sorted(files):
        x, fs = load_any(f, args.sample_rate)
        freqs, amp = compute_spectrum(x, fs)
        peak_f, peak_a = peak_in_band(freqs, amp, args.center, args.band)
        ts = ''
        # Try to infer timestamp from filename (YYYYMMDD_HHMM etc.)
        base = os.path.basename(f)
        ts = base
        rows.append((f, peak_f, peak_a, ts))
        peaks.append(peak_f)
        print(f"{f}: peak {peak_f:.6f} Hz, amp {peak_a:.3e}")

    if args.out_csv:
        os.makedirs(os.path.dirname(args.out_csv) or '.', exist_ok=True)
        with open(args.out_csv, 'w', encoding='utf-8') as fp:
            fp.write('file,peak_hz,amplitude,timestamp\n')
            for f, pf, pa, ts in rows:
                fp.write(f'{f},{pf},{pa},{ts}\n')

    if args.out_png:
        os.makedirs(os.path.dirname(args.out_png) or '.', exist_ok=True)
        plt.figure(figsize=(10,4))
        plt.plot(range(len(peaks)), peaks, marker='o', lw=1)
        plt.axhline(args.center, color='r', ls='--', alpha=0.5)
        plt.xlabel('file index (sorted)')
        plt.ylabel('peak frequency (Hz)')
        plt.title(f'Drift near {args.center} Hz (±{args.band} Hz)')
        plt.grid(alpha=0.3)
        plt.savefig(args.out_png, dpi=160, bbox_inches='tight')

if __name__ == '__main__':
    main()