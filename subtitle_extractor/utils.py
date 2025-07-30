from typing import List, Tuple
import re

def frame_to_timestamp(frame_name: str, fps: float) -> str:
    """從檔案名稱提取畫面編號並轉換為時間戳"""
    # 提取檔案名稱中的數字部分
    # 支援新格式：subtitle_content_0001.png 和舊格式：frame_0001.png
    if '_' in frame_name:
        # 取最後一個 _ 後的數字部分
        parts = frame_name.split('_')
        number_part = parts[-1].split('.')[0]
    else:
        # 如果沒有 _，嘗試從檔名中提取數字
        import re
        match = re.search(r'(\d+)', frame_name)
        number_part = match.group(1) if match else "1"
    
    try:
        frame_number = int(number_part)
    except ValueError:
        frame_number = 1
        
    total_seconds = frame_number / fps
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    ms = int((total_seconds % 1) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def is_similar(a: str, b: str) -> bool:
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a, b).ratio() > 0.9

def deduplicate_results(results: List[Tuple[str, str]], similarity_threshold: float = 0.9) -> List[Tuple[str, str]]:
    """去除相似的字幕條目"""
    if not results:
        return results
    
    deduplicated = [results[0]]  # 保留第一個結果
    
    for frame, text in results[1:]:
        is_duplicate = False
        for _, existing_text in deduplicated:
            if is_similar_with_threshold(text, existing_text, similarity_threshold):
                is_duplicate = True
                break
        
        if not is_duplicate:
            deduplicated.append((frame, text))
    
    return deduplicated

def is_similar_with_threshold(a: str, b: str, threshold: float = 0.9) -> bool:
    """比較兩個字串的相似度"""
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a, b).ratio() > threshold

def sanitize_filename(text: str, max_length: int = 50) -> str:
    """將文本轉換為安全的檔案名稱"""
    # 移除或替換不安全的字符
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    # 移除多餘的空格和換行
    text = re.sub(r'\s+', '_', text.strip())
    # 限制長度
    if len(text) > max_length:
        text = text[:max_length]
    # 移除結尾的特殊字符
    text = text.rstrip('._-')
    
    return text if text else "subtitle"