#!/usr/bin/env python3
"""
Radio lattice FFT analysis for LUFT signals.
Provides core functionality for loading data and computing spectra.
"""
from __future__ import annotations
import argparse, os, math
from typing import Optional, Tuple
import numpy as np
import matplotlib.pyplot as plt

try:
    from scipy.io import wavfile
except ImportError:
    wavfile = None


def load_data(path: str, sample_rate: Optional[float] = None) -> Tuple[np.ndarray, float]:
    """Load data from WAV or TXT file."""
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


def compute_spectrum(data: np.ndarray, fs: float) -> Tuple[np.ndarray, np.ndarray]:
    """Compute frequency spectrum using FFT."""
    # Apply window to reduce spectral leakage
    window = np.hanning(len(data))
    windowed_data = data * window
    
    # Compute FFT
    fft_result = np.fft.fft(windowed_data)
    freqs = np.fft.fftfreq(len(data), 1/fs)
    
    # Take only positive frequencies
    positive_mask = freqs >= 0
    freqs = freqs[positive_mask]
    amplitude = np.abs(fft_result[positive_mask])
    
    return freqs, amplitude


def main():
    """Main function for command-line usage."""
    ap = argparse.ArgumentParser(description='Analyze radio lattice signals with FFT')
    ap.add_argument('--input', required=True, help='Input file (.wav or .txt)')
    ap.add_argument('--out', default='output/fft_plot.png', help='Output plot path')
    ap.add_argument('--sample-rate', type=float, default=None, help='Hz (needed for single-column TXT)')
    args = ap.parse_args()
    
    # Load data
    data, fs = load_data(args.input, args.sample_rate)
    print(f"Loaded {len(data)} samples at {fs} Hz")
    
    # Compute spectrum
    freqs, amplitude = compute_spectrum(data, fs)
    
    # Find peaks around LUFT frequencies
    luft_freq = 7467.779
    band = 5.0  # Hz
    mask = (freqs >= luft_freq - band) & (freqs <= luft_freq + band)
    
    if np.any(mask):
        sub_f = freqs[mask]
        sub_a = amplitude[mask]
        peak_idx = np.argmax(sub_a)
        peak_freq = sub_f[peak_idx]
        peak_amp = sub_a[peak_idx]
        print(f"Peak near {luft_freq} Hz: {peak_freq:.6f} Hz, amplitude {peak_amp:.3e}")
    
    # Create output directory
    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    
    # Plot spectrum
    plt.figure(figsize=(12, 6))
    plt.semilogy(freqs, amplitude)
    plt.axvline(luft_freq, color='r', linestyle='--', alpha=0.7, label=f'{luft_freq} Hz')
    plt.axvline(7468.3, color='orange', linestyle='--', alpha=0.7, label='7468.3 Hz')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Radio Lattice FFT Analysis')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(7460, 7475)  # Focus on LUFT frequency range
    plt.savefig(args.out, dpi=160, bbox_inches='tight')
    print(f"Plot saved to {args.out}")


if __name__ == '__main__':
    main()