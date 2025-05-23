

import pytest
from pathlib import Path
from subtitle_extractor.ocr_engine import ocr_frames

@pytest.fixture
def sample_frame_dir(tmp_path):
    frame_dir = tmp_path / "frames"
    frame_dir.mkdir()
    dummy_image = frame_dir / "frame_0001.png"
    dummy_image.write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 100)
    return frame_dir

def test_ocr_returns_list(sample_frame_dir):
    langs = ["en"]
    results = ocr_frames(sample_frame_dir, langs)
    assert isinstance(results, list)
    for item in results:
        assert isinstance(item, tuple)
        assert isinstance(item[0], str)
        assert isinstance(item[1], str)