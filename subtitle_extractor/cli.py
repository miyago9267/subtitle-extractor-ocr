import argparse
from pathlib import Path
from .frame_extractor import extract_frames
from .ocr_engine import ocr_frames
from .writer import write_txt, write_srt

def main():
    parser = argparse.ArgumentParser(description="Extract subtitles from video frames using OCR.")
    parser.add_argument("video", type=str)
    parser.add_argument("--fps", type=float, default=1.0)
    parser.add_argument("--format", choices=["txt", "srt"], default="txt", help="Output format (txt or srt)")
    parser.add_argument("--lang", type=str, default="en,ch_tra,ja", help="Comma-separated language codes for OCR")
    args = parser.parse_args()

    frames_dir = extract_frames(args.video, args.fps)
    langs = [lang.strip() for lang in args.lang.split(",")]
    results = ocr_frames(frames_dir, langs)

    if args.format == "srt":
        write_srt(results, args.fps)
    else:
        write_txt(results)

if __name__ == "__main__":
    main()