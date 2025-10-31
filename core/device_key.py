import os
import json
import hashlib
import secrets
from pathlib import Path

class DeviceKeyManager:
    KEY_PATH = Path.home() / ".chromavine" / "device.key"

    @classmethod
    def get_or_create_device_key(cls):
        cls.KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
        if cls.KEY_PATH.exists():
            try:
                with open(cls.KEY_PATH, "r") as f:
                    data = json.load(f)
                    if "device_key" in data and isinstance(data["device_key"], str) and len(data["device_key"]) == 64:
                        return data["device_key"]
            except Exception:
                pass

        # Generate new unique device key
        raw = secrets.token_bytes(32)
        device_key = hashlib.sha256(raw).hexdigest()
        with open(cls.KEY_PATH, "w") as f:
            json.dump({"device_key": device_key, "generated_on": "local"}, f)
        return device_key

    @classmethod
    def verify_device_key_in_update(cls, update_manifest):
        """
        Optional: future-proofing. If update manifest includes per-device binding,
        verify here. For now, just ensures local key exists.
        """
        return cls.get_or_create_device_key() is not None
