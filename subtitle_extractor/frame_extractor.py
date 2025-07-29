import subprocess
from pathlib import Path
import hashlib

def extract_frames(video_path: str, fps: float = 1.0) -> Path:
    # 為每個影片檔案創建唯一的輸出目錄
    video_name = Path(video_path).stem
    # 使用檔案路徑的 hash 確保唯一性，避免同名檔案衝突
    path_hash = hashlib.md5(video_path.encode()).hexdigest()[:8]
    output_dir = Path(f".output/frames/{video_name}_{path_hash}")
    
    # 清理舊的 frames（如果存在）
    if output_dir.exists():
        import shutil
        shutil.rmtree(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps={fps}",
        "-y",  # 覆寫輸出檔案
        str(output_dir / "frame_%04d.png")
    ]
    subprocess.run(cmd, check=True)
    return output_dir