import easyocr
import re
import cv2
import numpy as np
import os
from pathlib import Path
from typing import List, Tuple
from .utils import sanitize_filename

def crop_subtitle_region(image_path: str, region_ratio: float = 0.3) -> np.ndarray:
    """
    裁切圖片的字幕區域（通常在畫面下方）
    
    Args:
        image_path: 圖片檔案路徑
        region_ratio: 保留畫面下方的比例（0.3 表示保留下方30%的區域）
    
    Returns:
        裁切後的圖片陣列
    """
    # 讀取圖片
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"無法讀取圖片: {image_path}")
    
    height, width = image.shape[:2]
    
    # 計算裁切區域（保留下方的部分）
    start_y = int(height * (1 - region_ratio))
    cropped_image = image[start_y:height, 0:width]
    
    return cropped_image

def is_meaningful_text(text: str) -> bool:
    """檢查文字是否有意義（不只是雜訊或符號）"""
    if not text or not text.strip():
        return False
    
    # 移除空白字符
    clean_text = text.strip()
    
    # 如果長度太短（少於2個字符），可能是雜訊
    if len(clean_text) < 2:
        return False
    
    # 檢查是否只包含特殊符號或數字
    # 至少要有一個字母或中文字符
    if not re.search(r'[a-zA-Z\u4e00-\u9fff\u3400-\u4dbf]', clean_text):
        return False
    
    # 檢查是否只是重複的字符（如 "..." 或 "---"）
    if len(set(clean_text)) <= 2 and len(clean_text) > 3:
        return False
    
    return True

def ocr_frames(frames_dir: Path, langs: List[str], subtitle_region_ratio: float = 0.3) -> List[Tuple[str, str]]:
    """
    對畫面進行 OCR 處理，只掃描字幕可能出現的區域
    自動清除沒有字幕的圖片，並將有字幕的圖片重新命名為字幕內容
    
    Args:
        frames_dir: 畫面檔案目錄
        langs: OCR 語言列表
        subtitle_region_ratio: 字幕區域比例（0.3 表示掃描下方30%的區域）
    """
    reader = easyocr.Reader(langs)
    frames = sorted(frames_dir.glob("frame_*.png"))
    results = []
    renamed_files = []
    
    print(f"開始 OCR 處理，共 {len(frames)} 個畫面")
    print(f"僅掃描畫面下方 {subtitle_region_ratio*100:.0f}% 的區域")
    
    for i, frame in enumerate(frames, 1):
        try:
            # 裁切字幕區域
            cropped_image = crop_subtitle_region(str(frame), subtitle_region_ratio)
            
            # 對裁切後的圖片進行 OCR
            result = reader.readtext(cropped_image, detail=0)
            
            # 檢查是否有文字內容
            if result:
                # 合併所有文字並檢查是否有意義
                text_content = ' '.join(result).strip()
                
                if is_meaningful_text(text_content):
                    print(f"[{i}/{len(frames)}] {frame.name}: {text_content}")
                    
                    # 生成新的檔案名稱
                    safe_text = sanitize_filename(text_content, max_length=80)
                    new_frame_name = f"{safe_text}_{i:04d}.png"
                    new_frame_path = frames_dir / new_frame_name
                    
                    # 重新命名圖片檔案
                    try:
                        frame.rename(new_frame_path)
                        renamed_files.append((new_frame_name, text_content))
                        results.append((new_frame_name, text_content))
                        print(f"    → 重新命名為: {new_frame_name}")
                    except Exception as rename_error:
                        print(f"    × 重新命名失敗: {rename_error}")
                        results.append((frame.name, text_content))
                else:
                    print(f"[{i}/{len(frames)}] {frame.name}: 跳過（無意義文字：{text_content}）")
                    # 刪除無意義的圖片
                    try:
                        frame.unlink()
                        print(f"    → 已刪除無意義圖片")
                    except Exception as delete_error:
                        print(f"    × 刪除失敗: {delete_error}")
            else:
                print(f"[{i}/{len(frames)}] {frame.name}: 跳過（無文字內容）")
                # 刪除沒有文字的圖片
                try:
                    frame.unlink()
                    print(f"    → 已刪除無文字圖片")
                except Exception as delete_error:
                    print(f"    × 刪除失敗: {delete_error}")
                
        except Exception as e:
            print(f"[{i}/{len(frames)}] {frame.name}: 處理錯誤 - {e}")
            continue
    
    print(f"OCR 完成，從 {len(frames)} 個畫面中提取到 {len(results)} 個有效字幕")
    print(f"重新命名了 {len(renamed_files)} 個圖片檔案")
    print(f"刪除了 {len(frames) - len(results)} 個無效圖片")
    
    return results