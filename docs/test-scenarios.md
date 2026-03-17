# Test Scenarios

## Scenario 1: Nmap Port Scan

### Kali commands for nmap

```bash
nmap -sS -Pn -T4 -p 1-1000 192.168.241.144
nmap -A -T4 192.168.241.144
```

### Expected outcome

- Connectivity confirmed
- Possible host/service visibility on Ubuntu
- Limited Wazuh evidence unless network telemetry is enhanced

## Scenario 2: Hydra SSH Brute Force

### Preconditions

- Ubuntu SSH server running on port `22`
- Kali can reach Ubuntu over the network

### Kali commands for hydra

```bash
printf "123456\npassword\nadmin123\nubuntu\nkali\n" > pass.txt
hydra -l ubuntu -P pass.txt ssh://192.168.241.144 -t 4 -V
```

### Ubuntu monitoring terminals

```bash
sudo tail -f /var/ossec/logs/alerts/alerts.json
```

```bash
sudo tail -f /var/ossec/logs/integrations/ml_ids_predictions.json
```

### Expected Wazuh rules

- `5503` — PAM user login failed
- `5760` — sshd authentication failed
- `5715` — sshd authentication success

### Expected project outcome

- Hydra activity generates Wazuh alerts
- ML integration enriches those alerts automatically
- Result can be documented with screenshots and dashboard evidence
