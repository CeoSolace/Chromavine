import os
import time
import shutil
import threading
import json
from datetime import datetime
from pathlib import Path

class AutoSaveManager:
    def __init__(self, interval=30):
        self.interval = interval
        self.autosave_dir = Path.home() / ".chromavine" / "autosaves"
        self.autosave_dir.mkdir(parents=True, exist_ok=True)
        self.project_path = "current_project.cvproj"
        self.running = False
        self.thread = None
        self.lock = threading.Lock()

    def save_project(self):
        if not os.path.exists(self.project_path):
            return
        with self.lock:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            backup_path = self.autosave_dir / f"autosave_{timestamp}.cvproj"
            try:
                shutil.copy2(self.project_path, backup_path)
            except Exception:
                return

        autosaves = sorted(self.autosave_dir.glob("autosave_*.cvproj"))
        for old in autosaves[:-10]:
            try:
                old.unlink()
            except Exception:
                pass

    def _loop(self):
        while self.running:
            self.save_project()
            slept = 0
            while slept < self.interval and self.running:
                time.sleep(1)
                slept += 1

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def get_latest_autosave(self):
        autosaves = sorted(self.autosave_dir.glob("autosave_*.cvproj"))
        return autosaves[-1] if autosaves else None

    def restore_latest(self):
        latest = self.get_latest_autosave()
        if latest and os.path.exists(self.project_path):
            backup = self.project_path + ".crashbackup"
            shutil.copy2(self.project_path, backup)
        if latest:
            shutil.copy2(latest, self.project_path)
