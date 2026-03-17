# Setup Guide

## 1. Copy integration assets to Ubuntu Wazuh manager

```bash
sudo mkdir -p /var/ossec/integrations/models
sudo cp binary_ids_model.pkl /var/ossec/integrations/models/
sudo cp binary_scaler.pkl /var/ossec/integrations/models/
sudo cp binary_feature_list.pkl /var/ossec/integrations/models/
sudo cp ml_ids_integration.py /var/ossec/integrations/custom-ml-ids.py
sudo cp feature_mapping.json /var/ossec/integrations/models/feature_mapping.json
```

## 2. Create executable integration launcher

```bash
sudo cp /var/ossec/integrations/custom-ml-ids.py /var/ossec/integrations/custom-ml-ids
sudo sed -i '1c #!/home/ubuntu/Desktop/ml_wazuh_project/.venv/bin/python' /var/ossec/integrations/custom-ml-ids
sudo chmod 750 /var/ossec/integrations/custom-ml-ids /var/ossec/integrations/custom-ml-ids.py
sudo chown root:wazuh /var/ossec/integrations/custom-ml-ids /var/ossec/integrations/custom-ml-ids.py
```

## 3. Install Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install joblib numpy scikit-learn==1.6.1
```

## 4. Add integration block to Wazuh

Add inside `/var/ossec/etc/ossec.conf`:

```xml
<integration>
  <name>custom-ml-ids</name>
  <level>3</level>
  <alert_format>json</alert_format>
</integration>
```

## 5. Prepare output location

```bash
sudo mkdir -p /var/ossec/logs/integrations
sudo touch /var/ossec/logs/integrations/ml_ids_predictions.json
sudo chown -R wazuh:wazuh /var/ossec/logs/integrations
sudo chmod 770 /var/ossec/logs/integrations
sudo chmod 660 /var/ossec/logs/integrations/ml_ids_predictions.json
```

## 6. Restart Wazuh

```bash
sudo systemctl daemon-reload
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager --no-pager -l
```

## 7. Validate

```bash
sudo tail -n 1 /var/ossec/logs/alerts/alerts.json > /tmp/test_alert.json
sudo /home/ubuntu/Desktop/ml_wazuh_project/.venv/bin/python /var/ossec/integrations/custom-ml-ids.py /tmp/test_alert.json
sudo tail -n 5 /var/ossec/logs/integrations/ml_ids_predictions.json
```
