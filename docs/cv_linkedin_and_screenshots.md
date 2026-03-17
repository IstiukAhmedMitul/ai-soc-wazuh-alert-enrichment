# CV + LinkedIn + Screenshot Guide

## 1) CV Content (Ready to Paste)

### Project Title

AI-Enhanced SOC Alert Enrichment using Wazuh SIEM and Python ML Integration

### 2-Line Summary

Built an end-to-end SOC lab where Wazuh SIEM alerts are enriched by a custom Python integration that applies a trained binary IDS model (Benign vs Attack). Simulated attacks from Kali Linux (Nmap, Hydra), validated detections in Wazuh, and generated ML-enriched outputs for incident triage.

### CV Bullet Version (4 bullets)

- Designed and implemented a Wazuh SOC lab (Ubuntu manager + Kali agent) with live attack simulation and centralized alerting.
- Developed a custom Python Wazuh integration to load `joblib` model artifacts, parse JSON alerts, perform feature extraction/scaling, and classify alerts as `Benign` or `Attack`.
- Executed controlled adversary simulations (`nmap` scans and Hydra SSH brute-force attempts) and validated detections via Wazuh rule events (authentication failed/success patterns).
- Produced operational documentation (setup, rollback, test scenarios) and reproducible evidence artifacts for dashboard-driven SOC demonstration.

### ATS-Friendly Skills Line

Wazuh SIEM, SOC Monitoring, Incident Detection, Python, scikit-learn, Joblib, Linux, JSON Parsing, Alert Enrichment, Threat Simulation, Nmap, Hydra, Security Operations

---

## 2) LinkedIn Post Captions (Ready to Use)

### Option A (Professional)

Built and completed my AI-enhanced SOC project using Wazuh SIEM + Python ML integration.  
I implemented a custom alert enrichment pipeline that classifies Wazuh alerts as Benign/Attack and validated it with attack simulations from Kali (Nmap + Hydra SSH brute-force).

Key outcomes:

- End-to-end SOC flow from attack simulation to SIEM detection
- Automated ML enrichment of JSON alerts
- Dashboard + evidence-driven validation

Next step: improving feature alignment with network telemetry (Suricata/Zeek) for stronger ML signal quality.

`#CyberSecurity #SOC #Wazuh #SIEM #BlueTeam #ThreatDetection #Python #MachineLearning #InfoSec #SecurityOperations`

### Option B (Concise)

Completed my SOC project: Wazuh SIEM + custom Python ML alert enrichment.  
Simulated attacks from Kali, detected events in Wazuh, and generated enriched predictions for SOC triage.  
Excited to keep improving the pipeline with network telemetry integrations.

`#CyberSecurity #SOCAnalyst #Wazuh #SIEM #BlueTeam #Python #MachineLearning`

### Option C (Story Style)

I wanted a project that felt close to real SOC workflow, so I built one:  
Kali attack simulation -> Ubuntu/Wazuh detection -> Python ML enrichment -> analyst-ready outputs.

The most valuable learning: integrating security tooling is not just model accuracy, it is data quality, field mapping, and operational reliability.

`#CyberSecurity #SOC #Wazuh #DetectionEngineering #BlueTeam #Linux #InfoSec`

---

## 3) Step-by-Step Screenshot Plan (Do This Now)

You already have Wazuh dashboard open. Capture screenshots in this exact order.

### A. Prepare before screenshots

1. On Ubuntu terminal 1, run:

   ```bash
   sudo tail -f /var/ossec/logs/alerts/alerts.json
   ```

2. On Ubuntu terminal 2, run:

   ```bash
   sudo tail -f /var/ossec/logs/integrations/ml_ids_predictions.json
   ```

3. On Kali, keep your Hydra command history visible (or rerun controlled test if needed).
4. Create a screenshot folder in your project: `docs/screenshots/`

### B. Wazuh Dashboard capture steps

1. In dashboard, open Security events / Alerts view.
2. Set time range to the attack window (example: Last 15 minutes).
3. Add filter for source IP from Kali (`192.168.241.128`) if available.
4. Capture screenshot #1: Alerts list showing SSH-related events.
5. Click an event with rule `5760` (`sshd: authentication failed`).
6. Capture screenshot #2: event details pane (`full_log`, `srcip`, `dstuser`, timestamp).
7. Open event with rule `5715` (`sshd: authentication success`).
8. Capture screenshot #3: successful auth event details.
9. Capture screenshot #4: timeline/histogram showing event burst around attack time.

### C. Terminal evidence capture

1. Kali terminal screenshot #5:
   - Hydra command + attempts + final result line.
2. Ubuntu terminal screenshot #6:
   - `alerts.json` lines including `5503`, `5760`, `5715`.
3. Ubuntu terminal screenshot #7:
   - `ml_ids_predictions.json` lines showing enriched outputs for those rule IDs.

### D. Architecture/evidence screenshot

1. Capture screenshot #8:
   - Your architecture diagram slide or README architecture section.

---

## 4) Screenshot Naming Convention

Use this naming format:

- `01_dashboard_alerts_overview.png`
- `02_dashboard_5760_failed_auth.png`
- `03_dashboard_5715_success_auth.png`
- `04_dashboard_timeline.png`
- `05_kali_hydra_output.png`
- `06_ubuntu_wazuh_alerts_json.png`
- `07_ubuntu_ml_enrichment_log.png`
- `08_architecture_flow.png`

---

## 5) How to Use Screenshots in Report/README

In your README or report, use one subsection per stage:

1. Attack simulation (Kali)
2. SIEM detection (Wazuh dashboard)
3. ML enrichment output (integration log)
4. End-to-end architecture

For each screenshot include:

- What happened
- Why it matters for SOC workflow
- Evidence fields (rule id, src ip, timestamp, prediction label)

---

## 6) Short Interview Script (30–45 sec)

"I built an AI-enhanced SOC lab using Wazuh on Ubuntu with a Kali attack node. I integrated a custom Python script that consumes Wazuh JSON alerts, applies a trained binary IDS model, and writes enriched predictions. I validated the pipeline using Hydra SSH brute-force simulations and confirmed detections in Wazuh dashboard plus enriched output logs. This project demonstrates SOC workflow integration, detection validation, and operational alert enrichment."
