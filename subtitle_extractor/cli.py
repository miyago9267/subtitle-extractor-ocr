import argparse
from pathlib import Path
from .frame_extractor import extract_frames
from .ocr_engine import ocr_frames
from .writer import write_txt, write_srt
from .utils import deduplicate_results

def main():
    parser = argparse.ArgumentParser(description="Extract subtitles from video frames using OCR.")
    parser.add_argument("video", type=str)
    parser.add_argument("--fps", type=float, default=1.0)
    parser.add_argument("--format", choices=["txt", "srt"], default="txt", help="Output format (txt or srt)")
    parser.add_argument("--lang", type=str, default="en,ch_tra,ja", help="Comma-separated language codes for OCR")
    parser.add_argument("--deduplicate", action="store_true", help="Remove duplicate subtitle entries")
    parser.add_argument("--auto-filename", action="store_true", help="Use subtitle content as filename (requires --deduplicate)")
    args = parser.parse_args()

    # 驗證參數依賴關係
    if args.auto_filename and not args.deduplicate:
        parser.error("--auto-filename requires --deduplicate to be enabled")

    frames_dir = extract_frames(args.video, args.fps)
    langs = [lang.strip() for lang in args.lang.split(",")]
    results = ocr_frames(frames_dir, langs)

    # 應用去重複功能
    if args.deduplicate:
        results = deduplicate_results(results)
        print(f"去重複後保留 {len(results)} 個字幕條目")

    # 決定檔案名稱
    custom_filename = None
    if args.auto_filename and results:
        # 使用第一個字幕內容作為檔案名稱
        first_subtitle = results[0][1] if results else "subtitle"
        custom_filename = first_subtitle

    # 輸出結果
    if args.format == "srt":
        write_srt(results, args.fps, custom_filename=custom_filename)
    else:
        write_txt(results, custom_filename=custom_filename)

if __name__ == "__main__":
    main()