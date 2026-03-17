#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np


DEFAULT_MODEL_PATH = "/var/ossec/integrations/models/binary_ids_model.pkl"
DEFAULT_SCALER_PATH = "/var/ossec/integrations/models/binary_scaler.pkl"
DEFAULT_FEATURE_LIST_PATH = "/var/ossec/integrations/models/binary_feature_list.pkl"
DEFAULT_MAPPING_PATH = "/var/ossec/integrations/models/feature_mapping.json"
DEFAULT_OUTPUT_PATH = "/var/ossec/logs/integrations/ml_ids_predictions.json"


def _to_float(value):
    if value is None:
        return None

    if isinstance(value, bool):
        return 1.0 if value else 0.0

    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        stripped = value.strip().lower()
        if stripped in {"", "null", "none", "nan", "-"}:
            return None
        if stripped in {"true", "yes", "y"}:
            return 1.0
        if stripped in {"false", "no", "n"}:
            return 0.0
        try:
            return float(stripped)
        except ValueError:
            protocol_map = {
                "tcp": 6.0,
                "udp": 17.0,
                "icmp": 1.0,
                "ipv6-icmp": 58.0,
            }
            return protocol_map.get(stripped)

    return None


def flatten_json(data, prefix="", out=None):
    if out is None:
        out = {}

    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            flatten_json(value, new_prefix, out)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            new_prefix = f"{prefix}[{index}]"
            flatten_json(value, new_prefix, out)
    else:
        out[prefix] = data

    return out


def build_aliases(feature_name):
    aliases = {feature_name}
    aliases.add(feature_name.replace(" ", "_"))
    aliases.add(feature_name.lower())
    aliases.add(feature_name.lower().replace(" ", "_"))
    aliases.add(feature_name.replace(".", "_"))
    aliases.add(feature_name.lower().replace(".", "_"))
    return list(aliases)


def load_mapping(mapping_path):
    mapping_file = Path(mapping_path)
    if not mapping_file.exists():
        return {}

    with mapping_file.open("r", encoding="utf-8") as file:
        mapping = json.load(file)

    return mapping if isinstance(mapping, dict) else {}


def lookup_mapped_value(feature_name, mapping, flat_alert):
    candidates = mapping.get(feature_name)
    if not candidates:
        return None

    if isinstance(candidates, str):
        candidates = [candidates]

    for path in candidates:
        if path in flat_alert:
            value = _to_float(flat_alert[path])
            if value is not None:
                return value

    return None


def extract_features(alert, feature_names, mapping):
    flat = flatten_json(alert)

    values = []
    missing = []

    for feature in feature_names:
        feature_value = lookup_mapped_value(feature, mapping, flat)

        if feature_value is None:
            for alias in build_aliases(feature):
                if alias in flat:
                    feature_value = _to_float(flat[alias])
                    if feature_value is not None:
                        break

        if feature_value is None:
            feature_value = 0.0
            missing.append(feature)

        values.append(feature_value)

    return np.array(values, dtype=np.float64).reshape(1, -1), missing


def predict(alert_path):
    model_path = os.getenv("ML_MODEL_PATH", DEFAULT_MODEL_PATH)
    scaler_path = os.getenv("ML_SCALER_PATH", DEFAULT_SCALER_PATH)
    feature_list_path = os.getenv("ML_FEATURE_LIST_PATH", DEFAULT_FEATURE_LIST_PATH)
    mapping_path = os.getenv("ML_FEATURE_MAPPING_PATH", DEFAULT_MAPPING_PATH)
    output_path = os.getenv("ML_OUTPUT_PATH", DEFAULT_OUTPUT_PATH)

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    feature_names = joblib.load(feature_list_path)
    mapping = load_mapping(mapping_path)

    with open(alert_path, "r", encoding="utf-8") as file:
        alert = json.load(file)

    X_raw, missing_features = extract_features(alert, feature_names, mapping)
    X_scaled = scaler.transform(X_raw)

    prediction_int = int(model.predict(X_scaled)[0])
    label = "Attack" if prediction_int == 1 else "Benign"

    probability = None
    if hasattr(model, "predict_proba"):
        try:
            probability = float(model.predict_proba(X_scaled)[0][prediction_int])
        except Exception:
            probability = None

    enriched = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "wazuh_ml_ids_integration",
        "wazuh": {
            "id": alert.get("id"),
            "rule_id": alert.get("rule", {}).get("id"),
            "rule_description": alert.get("rule", {}).get("description"),
            "agent": alert.get("agent", {}).get("name"),
        },
        "ml_prediction": {
            "label": label,
            "class": prediction_int,
            "confidence": probability,
            "missing_feature_count": len(missing_features),
            "missing_features": missing_features[:25],
        },
    }

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("a", encoding="utf-8") as out:
        out.write(json.dumps(enriched) + "\n")

    print(json.dumps(enriched))


def main():
    if len(sys.argv) < 2:
        print("Usage: ml_ids_integration.py <alert_json_path>", file=sys.stderr)
        sys.exit(1)

    alert_path = sys.argv[1]

    try:
        predict(alert_path)
    except Exception as error:
        err = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "wazuh_ml_ids_integration",
            "status": "error",
            "message": str(error),
            "alert_path": alert_path,
        }
        print(json.dumps(err), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
