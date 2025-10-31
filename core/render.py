import os
import subprocess
import json
from pathlib import Path

class RenderEngine:
    def __init__(self, project_file="current_project.cvproj"):
        self.project_file = project_file
        self.media_engine = MediaEngine()

    def load_project(self):
        if not os.path.exists(self.project_file):
            raise FileNotFoundError("No project to render")
        with open(self.project_file, "r") as f:
            return json.load(f)

    def render_timeline(self, output_path, resolution=None, fps=None, codec="h264", container="mp4"):
        proj = self.load_project()
        canvas = proj["canvas"]
        w = resolution[0] if resolution else canvas["width"]
        h = resolution[1] if resolution else canvas["height"]
        r = fps if fps else canvas["fps"]

        # Create temporary concat file
        clips = []
        for track in proj.get("video_tracks", []):
            for clip in track.get("clips", []):
                if "file" in clip:
                    clips.append(clip["file"])

        if not clips:
            raise ValueError("No clips to render")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tf:
            for clip in clips:
                if os.path.exists(clip):
                    tf.write(f"file '{os.path.abspath(clip)}'\n")
            concat_file = tf.name

        try:
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat", "-safe", "0",
                "-i", concat_file,
                "-vf", f"scale={w}:{h},fps={r}",
                "-c:v", "libx264" if codec == "h264" else codec,
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                output_path
            ]
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode != 0:
                raise RuntimeError("Render failed")
        finally:
            os.unlink(concat_file)
