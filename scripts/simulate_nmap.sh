#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: ./simulate_nmap.sh <target-ip>"
  exit 1
fi

TARGET_IP="$1"

echo "Running SYN scan against $TARGET_IP"
nmap -sS -Pn -T4 -p 1-1000 "$TARGET_IP"

echo "Running service and OS scan against $TARGET_IP"
nmap -A -T4 "$TARGET_IP"
