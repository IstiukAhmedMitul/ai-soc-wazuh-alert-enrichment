#!/usr/bin/env bash
set -euo pipefail

echo "=== Wazuh alerts ==="
sudo tail -f /var/ossec/logs/alerts/alerts.json
