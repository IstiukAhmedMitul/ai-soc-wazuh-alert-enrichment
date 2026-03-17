# Rollback Guide

## Back up configuration before changes

```bash
sudo cp /var/ossec/etc/ossec.conf /var/ossec/etc/ossec.conf.bak.$(date +%F-%H%M%S)
```

## Disable the custom integration

1. Remove the `custom-ml-ids` `<integration>` block from `/var/ossec/etc/ossec.conf`
2. Restart Wazuh manager

```bash
sudo systemctl restart wazuh-manager
```

## Remove deployed files

```bash
sudo rm -f /var/ossec/integrations/custom-ml-ids
sudo rm -f /var/ossec/integrations/custom-ml-ids.py
sudo rm -rf /var/ossec/integrations/models
sudo rm -f /var/ossec/logs/integrations/ml_ids_predictions.json
```

## Restore previous config backup

```bash
sudo cp /var/ossec/etc/ossec.conf.bak.<timestamp> /var/ossec/etc/ossec.conf
sudo systemctl restart wazuh-manager
```

## Post-demo hardening

- Change weak demo credentials immediately
- Remove temporary wordlists from Kali
- Keep the lab isolated from production traffic
