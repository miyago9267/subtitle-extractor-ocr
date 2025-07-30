import argparse
import os
from pathlib import Path
from .frame_extractor import extract_frames
from .ocr_engine import ocr_frames
from .writer import write_txt, write_srt
from .utils import deduplicate_results

def get_video_files(input_path: str) -> list[str]:
    """獲取影片檔案列表"""
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v'}
    
    path = Path(input_path)
    if path.is_file():
        return [str(path)]
    elif path.is_dir():
        video_files = []
        for file_path in path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in video_extensions:
                video_files.append(str(file_path))
        return sorted(video_files)
    else:
        raise ValueError(f"路徑不存在: {input_path}")

def process_single_video(video_path: str, args) -> None:
    """處理單個影片檔案"""
    print(f"\n正在處理: {video_path}")
    
    try:
        frames_dir = extract_frames(video_path, args.fps)
        langs = [lang.strip() for lang in args.lang.split(",")]
        
        # 傳遞字幕區域比例參數
        subtitle_region = getattr(args, 'subtitle_region', 0.3)
        results = ocr_frames(frames_dir, langs, subtitle_region)

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
        else:
            # 使用影片檔案名稱作為基礎檔名
            video_name = Path(video_path).stem
            custom_filename = video_name

        # 輸出結果（在每個 frames 目錄中）
        if args.format == "srt":
            write_srt(results, args.fps, custom_filename=custom_filename, frames_dir=frames_dir)
        else:
            write_txt(results, custom_filename=custom_filename, frames_dir=frames_dir)
            
        print(f"完成處理: {video_path}")
        
    except Exception as e:
        print(f"處理 {video_path} 時發生錯誤: {e}")

def main():
    parser = argparse.ArgumentParser(description="Extract subtitles from video frames using OCR.")
    parser.add_argument("video", type=str, help="影片檔案路徑或包含影片的資料夾路徑")
    parser.add_argument("--fps", type=float, default=1.0)
    parser.add_argument("--format", choices=["txt", "srt"], default="txt", help="Output format (txt or srt)")
    parser.add_argument("--lang", type=str, default="en,ch_tra,ja", help="Comma-separated language codes for OCR")
    parser.add_argument("--deduplicate", action="store_true", help="Remove duplicate subtitle entries")
    parser.add_argument("--auto-filename", action="store_true", help="Use subtitle content as filename (requires --deduplicate)")
    parser.add_argument("--subtitle-region", type=float, default=0.3, help="字幕區域比例，範圍0.1-1.0（預設0.3表示掃描下方30%%的區域）")
    args = parser.parse_args()

    # 驗證參數
    if args.auto_filename and not args.deduplicate:
        parser.error("--auto-filename requires --deduplicate to be enabled")
    
    if not (0.1 <= args.subtitle_region <= 1.0):
        parser.error("--subtitle-region must be between 0.1 and 1.0")

    # 獲取影片檔案列表
    try:
        video_files = get_video_files(args.video)
        if not video_files:
            print(f"在 {args.video} 中沒有找到任何影片檔案")
            return
        
        print(f"找到 {len(video_files)} 個影片檔案")
        
        # 處理每個影片檔案
        for video_file in video_files:
            process_single_video(video_file, args)
            
        print(f"\n全部完成！共處理了 {len(video_files)} 個影片檔案")
        
    except ValueError as e:
        print(f"錯誤: {e}")
    except Exception as e:
        print(f"發生未預期的錯誤: {e}")

if __name__ == "__main__":
    main()