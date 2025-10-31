import os
import json
import urllib.request
import subprocess
import shutil
from datetime import datetime, date
from pathlib import Path
from core.device_key import DeviceKeyManager

class UpdateManager:
    # GitHub release URLs
    MANIFEST_URL = "https://github.com/CeoSolace/Chromavine/releases/latest/download/latest.json"
    BASE_DOWNLOAD_URL = "https://github.com/CeoSolace/Chromavine/releases/latest/download/"

    def __init__(self, config):
        self.config = config
        self.local_manifest = "updates/latest.json"
        os.makedirs("updates", exist_ok=True)

    def fetch_manifest(self):
        """Fetch latest.json from GitHub Releases."""
        try:
            req = urllib.request.Request(self.MANIFEST_URL)
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = resp.read().decode('utf-8')
                data = json.loads(raw)
                with open(self.local_manifest, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                return data
        except Exception:
            return None

    def verify_signature(self):
        """Verify latest.json.sig using embedded public_key.pem."""
        sig_path = self.local_manifest + ".sig"
        pubkey_path = "resources/public_key.pem"

        if not os.path.exists(self.local_manifest) or not os.path.exists(sig_path):
            return False

        # Ensure public key exists
        if not os.path.exists(pubkey_path):
            return False

        try:
            result = subprocess.run([
                "gpg", "--quiet", "--keyring", pubkey_path,
                "--verify", sig_path, self.local_manifest
            ], capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

    def check_update_needed(self):
        last_verified = date.fromisoformat(self.config["last_verified"])
        days = (date.today() - last_verified).days
        return days > self.config["reminder_days"]

    def should_restrict(self):
        last_verified = date.fromisoformat(self.config["last_verified"])
        days = (date.today() - last_verified).days
        return days > self.config["restricted_days"]

    def import_offline_package(self, zip_path):
        """Import and verify signed ZIP update manually."""
        if not os.path.isfile(zip_path) or not os.path.isfile(zip_path + ".sig"):
            return False

        # Verify signature
        try:
            result = subprocess.run([
                "gpg", "--quiet", "--verify",
                zip_path + ".sig",
                zip_path
            ], capture_output=True)
            if result.returncode != 0:
                return False
        except Exception:
            return False

        # Extract and replace
        extract_to = "updates/staging"
        if os.path.exists(extract_to):
            shutil.rmtree(extract_to)
        os.makedirs(extract_to)
        shutil.unpack_archive(zip_path, extract_to)

        for item in os.listdir(extract_to):
            src = os.path.join(extract_to, item)
            dst = item
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
            shutil.move(src, dst)

        shutil.rmtree(extract_to)

        # Finalize
        self._update_verified()
        return True

    def _update_verified(self):
        """Update last_verified and ensure device key is ready."""
        DeviceKeyManager.get_or_create_device_key()  # Ensure key exists
        self.config["last_verified"] = date.today().isoformat()
        with open("config.json", "w") as f:
            json.dump(self.config, f, indent=2)
