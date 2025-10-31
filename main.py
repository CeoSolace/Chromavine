import sys
import os
import json
from datetime import datetime
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.autosave import AutoSaveManager
from core.integrity import IntegrityChecker
from core.updater import UpdateManager

def load_config():
    if not os.path.exists("config.json"):
        default = {
            "last_verified": "1970-01-01",
            "reminder_days": 7,
            "restricted_days": 14,
            "autosave_interval": 30
        }
        with open("config.json", "w") as f:
            json.dump(default, f, indent=2)
        return default
    with open("config.json", "r") as f:
        return json.load(f)

def main():
    app = QApplication(sys.argv)

    config = load_config()
    today = datetime.utcnow().date()

    # Integrity check
    integrity = IntegrityChecker()
    if not integrity.verify_full():
        integrity.restore_corrupted()

    # Update status
    last_verified = datetime.fromisoformat(config["last_verified"]).date()
    days_since = (today - last_verified).days
    restricted_mode = days_since > config["restricted_days"]

    # Start autosave
    autosave = AutoSaveManager(interval=config["autosave_interval"])
    autosave.start()

    # Launch UI
    window = MainWindow(restricted_mode=restricted_mode)
    window.show()

    exit_code = app.exec()
    autosave.stop()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
