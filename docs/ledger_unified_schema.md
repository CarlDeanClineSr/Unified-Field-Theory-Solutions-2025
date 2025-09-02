# Unified Ledger Schema

This schema defines common fields for cross-scale audit logging, from audio drift (capsule scale) to particle physics (NA62) and cosmology (JWST). The unified approach ensures consistent tracking across all experimental domains.

## Core Five-Field Structure

| Field | Description | Example |
|-------|-------------|---------|
| **Who/When** | UTC timestamp + operator/source | `2025-01-15T14:30:00Z_operator_id` |
| **Setup/Context** | Equipment, environment, conditions | `helix_mk2_antenna_7468Hz_clear_sky` |
| **Measured** | Primary observation/data | `peak_amplitude_1.2e-15T` |
| **Checks** | Validation, consistency tests | `energy_conservation_ok` |
| **Notes** | Anomalies, references, next steps | `unusual_spike_see_run_log_47` |

## Optional Extended Fields

- `counts`: Event counts per bin/category
- `rates`: Derived rates and ratios  
- `provenance`: `source_url` for data traceability
- `classification`: Signal vs background tagging
- `weight`: Statistical weight or confidence
- `deviation`: Difference from baseline/expected

## Cross-Scale Mapping Examples

### Audio Drift (Capsule Scale)
```
timestamp: 2025-01-15T14:30:00Z
setup: helix_mk2_7468Hz_basement_lab
measured: phase_drift_0.15rad_per_min
checks: no_external_interference
notes: steady_ambient_conditions
```

### NA62 Rare K+ → π+νν̄ Events
```
timestamp: 2025-01-15T14:30:00Z
setup: NA62_kaon_beam_run_001
measured: candidate_events_3_in_1e12
checks: momentum_energy_conservation_ok
classification: signal_candidate
weight: 0.87
source_url: cern.ch/NA62/run_001
notes: passed_all_veto_systems
```

### JWST High-z Galaxies
```
timestamp: 2025-01-15T14:30:00Z  
setup: JWST_NIRCam_CEERS_field
measured: galaxy_z13.2_logM_10.1
checks: photometry_consistent_3sigma
classification: high_z_candidate
source_url: mast.stsci.edu/CEERS_123
notes: unusually_massive_for_redshift
```

## Key Requirements

- **UTC timestamps**: All entries must use UTC format for temporal consistency
- **Source provenance**: Include `source_url` when applicable for data traceability  
- **Minimal fields**: Use only fields necessary for the specific audit
- **Consistent classification**: Use standard signal/background/candidate categories
- **Conservation checks**: Always validate relevant physical conservation laws