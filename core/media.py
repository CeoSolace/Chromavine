import subprocess
import json
import os
import tempfile
from pathlib import Path

class MediaEngine:
    def __init__(self):
        self.supported_codecs = {"video": ["h264", "hevc", "vp9", "prores"], "audio": ["aac", "mp3", "flac", "pcm_s16le"]}
        self.supported_containers = ["mp4", "mov", "mkv", "webm", "avi"]

    def probe(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Media file not found: {filepath}")
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            filepath
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError("ffprobe failed")
        return json.loads(result.stdout)

    def generate_proxy(self, input_path, output_path, width=640, height=360, fps=30):
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf", f"scale={width}:{height}",
            "-r", str(fps),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            raise RuntimeError("Proxy generation failed")

    def extract_audio(self, video_path, audio_path):
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vn", "-acodec", "pcm_s16le",
            "-ar", "48000", "-ac", "2",
            audio_path
        ]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            raise RuntimeError("Audio extraction failed")

    def is_gpu_available(self):
        # Basic check — real impl would query VAAPI/NVENC/Metal
        try:
            subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True, check=True)
            return True
        except Exception:
            return False
