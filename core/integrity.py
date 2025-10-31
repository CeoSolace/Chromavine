import os
import hashlib
import json
import shutil
from pathlib import Path

class IntegrityChecker:
    PROTECTED_PATHS = [
        "ui/assets/logo.png",
        "ui/assets/watermark.png",
        "core/media.py",
        "core/render.py",
        "core/timeline.py",
        "core/project.py",
        "main.py"
    ]

    def __init__(self, hashlist_path="updates/hashlist.json"):
        self.hashlist_path = hashlist_path

    def compute_sha256(self, filepath):
        if not os.path.isfile(filepath):
            return None
        h = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            return h.hexdigest()
        except Exception:
            return None

    def load_hashlist(self):
        if not os.path.exists(self.hashlist_path):
            return {}
        try:
            with open(self.hashlist_path, "r") as f:
                data = json.load(f)
                return data.get("files", {})
        except Exception:
            return {}

    def verify_full(self):
        hashlist = self.load_hashlist()
        for path in self.PROTECTED_PATHS:
            expected = hashlist.get(path)
            if expected is None:
                continue
            actual = self.compute_sha256(path)
            if actual != expected:
                return False
        return True

    def restore_corrupted(self):
        hashlist = self.load_hashlist()
        for path in self.PROTECTED_PATHS:
            expected = hashlist.get(path)
            if expected is None:
                continue
            actual = self.compute_sha256(path)
            if actual == expected:
                continue
            backup = path + ".bak"
            if os.path.exists(backup):
                try:
                    shutil.copy2(backup, path)
                except Exception:
                    pass
