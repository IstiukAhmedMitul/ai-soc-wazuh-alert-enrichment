# Architecture Overview

## End-to-End Flow

1. **Attack simulation from Kali**
   - `nmap` scan
   - `hydra` SSH brute-force simulation
2. **Target telemetry on Ubuntu**
   - SSH and PAM logs
   - system and Wazuh-generated event logs
3. **Wazuh manager processing**
   - rule matching
   - alert JSON generation
4. **Custom Python integration**
   - loads model artifacts
   - extracts mapped features
   - applies scaler
   - predicts binary class
5. **Enriched output**
   - writes JSON lines to `/var/ossec/logs/integrations/ml_ids_predictions.json`
6. **Analyst visibility**
   - raw Wazuh alerts
   - enriched ML output
   - optional dashboard visualizations

## Components

### Ubuntu VM
- Wazuh manager
- custom integration script
- model artifacts
- SSH server

### Kali VM
- Wazuh agent
- attacker tooling (`nmap`, `hydra`)

### ML Assets
- `binary_ids_model.pkl`
- `binary_scaler.pkl`
- `binary_feature_list.pkl`
- feature mapping JSON

## Design Decision

The integration enriches alerts outside the Wazuh core engine. This keeps the solution modular and reversible, which is safer for a demonstration environment.
