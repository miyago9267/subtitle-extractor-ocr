import subprocess
from pathlib import Path

def extract_frames(video_path: str, fps: float = 1.0) -> Path:
    output_dir = Path(".output/frames")
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps={fps}",
        str(output_dir / "frame_%04d.png")
    ]
    subprocess.run(cmd, check=True)
    return output_dir