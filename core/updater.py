import os
import json
import urllib.request
import subprocess
import shutil
from datetime import datetime, timedelta

class UpdateManager:
    def __init__(self, config):
        self.config = config
        self.manifest_url = "https://updates.chromavine.app/latest.json"
        self.local_manifest = "updates/latest.json"
        os.makedirs("updates", exist_ok=True)

    def fetch_manifest(self):
        try:
            req = urllib.request.Request(self.manifest_url)
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = resp.read().decode('utf-8')
                data = json.loads(raw)
                with open(self.local_manifest, 'w') as f:
                    json.dump(data, f, indent=2)
                return data
        except Exception:
            return None

    def verify_signature(self):
        if not os.path.exists(self.local_manifest) or not os.path.exists(self.local_manifest + ".sig"):
            return False
        try:
            result = subprocess.run([
                "gpg", "--quiet", "--verify",
                self.local_manifest + ".sig",
                self.local_manifest
            ], capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

    def check_update_needed(self):
        last_verified = datetime.fromisoformat(self.config["last_verified"])
        days = (datetime.utcnow() - last_verified).days
        return days > self.config["reminder_days"]

    def should_restrict(self):
        last_verified = datetime.fromisoformat(self.config["last_verified"])
        days = (datetime.utcnow() - last_verified).days
        return days > self.config["restricted_days"]

    def import_offline_package(self, zip_path):
        if not os.path.isfile(zip_path) or not os.path.isfile(zip_path + ".sig"):
            return False
        try:
            result = subprocess.run([
                "gpg", "--quiet", "--verify",
                zip_path + ".sig",
                zip_path
            ], capture_output=True)
            if result.returncode != 0:
                return False
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
            self._update_verified()
            return True
        except Exception:
            return False

    def _update_verified(self):
        self.config["last_verified"] = datetime.utcnow().date().isoformat()
        with open("config.json", "w") as f:
            json.dump(self.config, f, indent=2)
