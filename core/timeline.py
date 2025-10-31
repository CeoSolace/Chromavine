import json
import os

class Timeline:
    def __init__(self, project_file="current_project.cvproj"):
        self.project_file = project_file
        self.data = self._load_project()

    def _load_project(self):
        if os.path.exists(self.project_file):
            with open(self.project_file, "r") as f:
                return json.load(f)
        return {
            "video_tracks": [],
            "audio_tracks": [],
            "canvas": {"width": 1920, "height": 1080, "fps": 30}
        }

    def save_project(self):
        with open(self.project_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_clip_to_track(self, track_index, clip_data, track_type="video"):
        tracks = self.data.get(f"{track_type}_tracks", [])
        if track_index >= len(tracks):
            raise IndexError("Track index out of range")
        tracks[track_index]["clips"].append(clip_data)
        self.save_project()

    def insert_track(self, name="New Track", track_type="video"):
        track = {
            "name": name,
            "clips": [],
            "muted": False,
            "locked": False
        }
        if track_type == "audio":
            track.update({"volume": 1.0, "solo": False})
        self.data.setdefault(f"{track_type}_tracks", []).append(track)
        self.save_project()

    def get_timeline_info(self):
        return {
            "video_track_count": len(self.data.get("video_tracks", [])),
            "audio_track_count": len(self.data.get("audio_tracks", [])),
            "canvas": self.data.get("canvas")
        }
