from pathlib import Path
from typing import List, Tuple, Optional
from .utils import frame_to_timestamp, sanitize_filename

def write_txt(results: List[Tuple[str, str]], output_path: Optional[Path] = None, custom_filename: Optional[str] = None, frames_dir: Optional[Path] = None) -> None:
    if output_path is None:
        if frames_dir:
            # 在 frames 目錄中輸出
            if custom_filename:
                safe_filename = sanitize_filename(custom_filename)
                output_path = frames_dir / f"{safe_filename}.txt"
            else:
                output_path = frames_dir / "subtitles.txt"
        else:
            # 使用原始邏輯
            if custom_filename:
                safe_filename = sanitize_filename(custom_filename)
                output_path = Path(f".output/{safe_filename}.txt")
            else:
                output_path = Path(".output/result.txt")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for frame, text in results:
            f.write(f"{frame}: {text}\n")
    
    print(f"TXT 檔案已輸出至: {output_path}")

def write_srt(results: List[Tuple[str, str]], fps: float, output_path: Optional[Path] = None, custom_filename: Optional[str] = None, frames_dir: Optional[Path] = None) -> None:
    if output_path is None:
        if frames_dir:
            # 在 frames 目錄中輸出
            if custom_filename:
                safe_filename = sanitize_filename(custom_filename)
                output_path = frames_dir / f"{safe_filename}.srt"
            else:
                output_path = frames_dir / "subtitles.srt"
        else:
            # 使用原始邏輯
            if custom_filename:
                safe_filename = sanitize_filename(custom_filename)
                output_path = Path(f".output/{safe_filename}.srt")
            else:
                output_path = Path(".output/result.srt")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for index, (frame, text) in enumerate(results, 1):
            start = frame_to_timestamp(frame, fps)
            
            # 計算結束時間（假設每個字幕持續 1/fps 秒）
            # 從檔名中提取畫面編號
            if '_' in frame:
                parts = frame.split('_')
                number_part = parts[-1].split('.')[0]
            else:
                import re
                match = re.search(r'(\d+)', frame)
                number_part = match.group(1) if match else "1"
                
            try:
                current_frame_number = int(number_part)
                end_frame_number = current_frame_number + 1
                # 生成結束時間戳
                end_total_seconds = end_frame_number / fps
                end_h = int(end_total_seconds // 3600)
                end_m = int((end_total_seconds % 3600) // 60)
                end_s = int(end_total_seconds % 60)
                end_ms = int((end_total_seconds % 1) * 1000)
                end = f"{end_h:02}:{end_m:02}:{end_s:02},{end_ms:03}"
            except ValueError:
                # 如果解析失敗，使用下一秒作為結束時間
                end = frame_to_timestamp(f"dummy_{int(number_part)+1:04d}.png", fps)
                
            f.write(f"{index}\n{start} --> {end}\n{text}\n\n")
    
    print(f"SRT 檔案已輸出至: {output_path}")
