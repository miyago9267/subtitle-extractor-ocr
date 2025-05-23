def frame_to_timestamp(frame_name: str, fps: float) -> str:
    frame_number = int(frame_name.split('_')[-1].split('.')[0])
    total_seconds = frame_number / fps
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    ms = int((total_seconds % 1) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def is_similar(a: str, b: str) -> bool:
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a, b).ratio() > 0.9