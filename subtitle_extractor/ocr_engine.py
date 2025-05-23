import easyocr
from pathlib import Path
from typing import List, Tuple

def ocr_frames(frames_dir: Path, langs: List[str]) -> List[Tuple[str, str]]:
    reader = easyocr.Reader(langs)
    frames = sorted(frames_dir.glob("frame_*.png"))
    results = []
    for frame in frames:
        result = reader.readtext(str(frame), detail=0)
        if result:
            text = ' '.join(result)
            print(f"{frame.name}: {text}")
            results.append((frame.name, text))
    return results