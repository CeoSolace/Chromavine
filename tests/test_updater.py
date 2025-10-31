import os
import json
import tempfile
from unittest.mock import patch
from core.updater import UpdateManager

def test_update_config_saves_verified_date():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        config = {
            "last_verified": "1970-01-01",
            "reminder_days": 7,
            "restricted_days": 14,
            "autosave_interval": 30
        }
        with open("config.json", "w") as f:
            json.dump(config, f)

        updater = UpdateManager(config)
        updater._update_verified()

        with open("config.json", "r") as f:
            new_config = json.load(f)

        assert new_config["last_verified"] != "1970-01-01"
