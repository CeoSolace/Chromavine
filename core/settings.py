import json
import os

class SettingsManager:
    DEFAULTS = {
        "ui_mode": "Pro",
        "autosave_enabled": True,
        "autosave_interval": 30,
        "proxy_enabled": False,
        "proxy_resolution": [640, 360],
        "gpu_accel": True,
        "last_export_dir": os.path.expanduser("~"),
        "restricted_mode": False
    }

    def __init__(self, config_path="user_settings.json"):
        self.config_path = config_path
        self.settings = self.load()

    def load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    user = json.load(f)
                    # Merge with defaults
                    merged = self.DEFAULTS.copy()
                    merged.update(user)
                    return merged
            except Exception:
                pass
        return self.DEFAULTS.copy()

    def save(self):
        with open(self.config_path, "w") as f:
            json.dump(self.settings, f, indent=2)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()
