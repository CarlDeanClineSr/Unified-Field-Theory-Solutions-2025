# Relay 006: JWST Audit Fit

**Purpose**: Demonstrate unified ledger logic for high-redshift galaxy mass/redshift anomaly detection, showing how capsule-level audit principles scale to cosmological observations and mass function deviations.

## Input Data

**Source**: `data/templates/jwst_galaxies_template.csv`

Expected columns: id, z, logM_star, SFR, field, survey, source_url, notes

## Audit Checks

### Per-Galaxy Ledger Entry
- Record provenance (source_url, field, survey)
- Validate photometric redshift consistency
- Check stellar mass estimates against SFR correlations
- Flag unusual mass-to-light ratios or SFR outliers

### Selection Window Validation
- Confirm galaxies fall within target redshift range
- Verify magnitude limits and completeness corrections
- Check for systematic selection biases by field position
- Validate against known contamination sources

### Mass Function Baseline Comparison
- Bin galaxies by redshift and stellar mass
- Compare observed counts to theoretical mass function
- Calculate deviation significance (σ) per bin  
- Identify excess or deficit regions requiring investigation

## Ledger Fields

Each galaxy generates a unified ledger entry:
```
timestamp: [observation_time_UTC]
setup: JWST_[instrument]_[field]_[survey]
measured: galaxy_z[redshift]_logM[mass]_SFR[star_formation]
checks: [photometry_consistency_status]
classification: [high_z_candidate/confirmed/contamination]
source_url: [mast.stsci.edu/archive_link]
notes: [unusual_properties_or_flags]
```

## Output

**Count Table**: Observed vs expected per redshift/mass bin:
```
| z-bin     | logM-bin | Observed | Expected | Deviation (σ) | Notes |
|-----------|----------|----------|----------|---------------|-------|
| 12.0-13.0 | 9.5-10.0 | 15       | 8.2      | +2.4          | excess |
| 12.0-13.0 | 10.0-10.5| 8        | 3.1      | +2.8          | excess |
| 13.0-14.0 | 9.5-10.0 | 3        | 1.2      | +1.6          | marginal |
```

**Summary Note** (5 sentences):
Analysis of [N] high-redshift galaxies from JWST [survey] reveals [X] candidates at z > 12 with unusually high stellar masses. Observed galaxy counts exceed theoretical predictions by [Y]σ in the 10^9.5-10^10.5 M⊙ mass range at z = 12-13. Photometric consistency checks validate [Z]% of candidates with <3σ scatter in color-magnitude relations. No significant contamination from lower-redshift interlopers detected in spectroscopic follow-up subsample. Results suggest either enhanced early star formation efficiency or systematic underestimation of high-z galaxy abundances in current models.