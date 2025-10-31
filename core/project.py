import os
import json
from datetime import datetime

class Project:
    def __init__(self, filepath=None):
        self.filepath = filepath or "current_project.cvproj"
        self.data = {
            "metadata": {
                "created": datetime.utcnow().isoformat(),
                "modified": datetime.utcnow().isoformat(),
                "app_version": "1.0"
            },
            "canvas": {
                "width": 1920,
                "height": 1080,
                "fps": 30.0,
                "aspect_ratio": 1.777,
                "color_space": "Rec.709"
            },
            "video_tracks": [],
            "audio_tracks": [],
            "compositions": [],
            "scenes_3d": []
        }

    def load(self):
        if not os.path.exists(self.filepath):
            return False
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        return True

    def save(self):
        self.data["metadata"]["modified"] = datetime.utcnow().isoformat()
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

    def set_canvas(self, width, height, fps, aspect_ratio=None, color_space="Rec.709"):
        self.data["canvas"]["width"] = int(width)
        self.data["canvas"]["height"] = int(height)
        self.data["canvas"]["fps"] = float(fps)
        self.data["canvas"]["aspect_ratio"] = float(aspect_ratio) if aspect_ratio else width / height
        self.data["canvas"]["color_space"] = color_space

    def add_video_track(self, name="Video Track"):
        track = {
            "name": name,
            "clips": [],
            "muted": False,
            "locked": False
        }
        self.data["video_tracks"].append(track)

    def add_audio_track(self, name="Audio Track"):
        track = {
            "name": name,
            "clips": [],
            "volume": 1.0,
            "muted": False,
            "solo": False
        }
        self.data["audio_tracks"].append(track)
