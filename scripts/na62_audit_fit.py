#!/usr/bin/env python3
"""
NA62 Audit Fit Script for Relay 005

Analyzes NA62 kaon decay candidates (K+→π+νν̄) with systematic 
preselection and veto processes. Generates audit summary.
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("Error: pandas is required. Install with: pip install pandas")
    sys.exit(1)


def load_and_validate_csv(csv_path):
    """Load CSV and perform basic validation."""
    try:
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} events from {csv_path}")
        
        # Basic validation
        required_cols = ['event_id', 'classification', 'veto_status', 'source_url']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"Warning: Missing expected columns: {missing_cols}")
        
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None


def apply_preselection(df):
    """Apply preselection criteria."""
    print("Applying preselection criteria...")
    
    # Simple preselection: events with valid particle_type
    if 'particle_type' in df.columns:
        preselected = df[df['particle_type'].isin(['kaon', 'pion'])]
        print(f"Preselection: {len(preselected)}/{len(df)} events pass")
        return preselected
    
    return df


def apply_veto(df):
    """Apply veto processes."""
    print("Applying veto processes...")
    
    if 'veto_status' in df.columns:
        veto_passed = df[df['veto_status'] == 'pass']
        print(f"Veto: {len(veto_passed)}/{len(df)} events pass")
        return veto_passed
    
    return df


def generate_audit_summary(df, output_dir):
    """Generate audit summary and save to markdown."""
    print("Generating audit summary...")
    
    # Count by classification
    if 'classification' in df.columns:
        classification_counts = df['classification'].value_counts()
        print("Classification counts:")
        for cls, count in classification_counts.items():
            print(f"  {cls}: {count}")
    
    # Weight statistics if available
    weight_stats = {}
    if 'weight' in df.columns:
        weight_stats = {
            'total_weight': df['weight'].sum(),
            'mean_weight': df['weight'].mean(),
            'std_weight': df['weight'].std()
        }
        print(f"Weight statistics: total={weight_stats['total_weight']:.3f}, "
              f"mean={weight_stats['mean_weight']:.3f}")
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate summary markdown
    summary_path = Path(output_dir) / "relay-005-audit-summary.md"
    with open(summary_path, 'w') as f:
        f.write("# Relay 005 — NA62 Audit Summary\n\n")
        f.write(f"**Analysis Date:** {pd.Timestamp.now().isoformat()}\n\n")
        f.write(f"**Total Events Processed:** {len(df)}\n\n")
        
        if 'classification' in df.columns:
            f.write("## Event Classification\n\n")
            for cls, count in classification_counts.items():
                f.write(f"- {cls}: {count}\n")
            f.write("\n")
        
        if weight_stats:
            f.write("## Weight Statistics\n\n")
            f.write(f"- Total weight: {weight_stats['total_weight']:.3f}\n")
            f.write(f"- Mean weight: {weight_stats['mean_weight']:.3f}\n")
            f.write(f"- Std weight: {weight_stats['std_weight']:.3f}\n\n")
        
        f.write("## Environment\n\n")
        baseline_br = os.environ.get('NA62_BASELINE_BR', 'not set')
        baseline_sigma = os.environ.get('NA62_BASELINE_SIGMA', 'not set')
        f.write(f"- Baseline BR: {baseline_br}\n")
        f.write(f"- Baseline Sigma: {baseline_sigma}\n")
    
    print(f"Audit summary saved to: {summary_path}")
    return summary_path


def main():
    parser = argparse.ArgumentParser(description='NA62 Audit Fit for Relay 005')
    parser.add_argument('--csv', required=True, help='Path to CSV file with candidate events')
    parser.add_argument('--out', default='results', help='Output directory for results')
    
    args = parser.parse_args()
    
    print(f"Starting NA62 audit fit analysis...")
    print(f"Input CSV: {args.csv}")
    print(f"Output directory: {args.out}")
    
    # Load data
    df = load_and_validate_csv(args.csv)
    if df is None:
        sys.exit(1)
    
    # Apply analysis pipeline
    df = apply_preselection(df)
    df = apply_veto(df)
    
    # Generate summary
    summary_path = generate_audit_summary(df, args.out)
    
    print(f"Analysis complete. Summary: {summary_path}")


if __name__ == '__main__':
    main()