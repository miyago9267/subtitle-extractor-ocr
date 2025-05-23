from pathlib import Path
from typing import List, Tuple
from .utils import frame_to_timestamp

def write_txt(results: List[Tuple[str, str]], output_path: Path = Path(".output/result.txt")) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for frame, text in results:
            f.write(f"{frame}: {text}\n")

def write_srt(results: List[Tuple[str, str]], fps: float, output_path: Path = Path(".output/result.srt")) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for index, (frame, text) in enumerate(results, 1):
            start = frame_to_timestamp(frame, fps)
            end_frame_number = int(frame.split('_')[-1].split('.')[0]) + 1
            end_frame = f"frame_{end_frame_number:04}.png"
            end = frame_to_timestamp(end_frame, fps)
            f.write(f"{index}\n{start} --> {end}\n{text}\n\n")
