# Subtitle Extractor OCR

自用小工具
從影片中擷取字幕的工具，透過 FFmpeg 擷取畫面，再用 EasyOCR 辨識字幕。

## 安裝與執行

### 1. 安裝依賴

- Python 3.12
- Poetry

```bash
poetry install
```

### 2. 使用方法

```bash
poetry run subocr <影片路徑> [選項]
```

#### 常用選項

- `--fps`: 每秒擷取幾幀（預設：1.0）
- `--format`: 字幕輸出格式，支援 `txt` 或 `srt`（預設：txt）
- `--lang`: OCR 語言（預設：`en,ch_tra,ja`）
  筆記：`ch_tra`（繁體中文）只能與 `en` 搭配使用，不能與 `ja` 同時出現。

### 範例

```bash
poetry subocr input.mp4 --fps 0.5 --format subtitle.srt --lang en,ch_tra
```

## 專案結構

```tree
subtitle_extractor/
├── cli.py               # CLI 入口點
├── frame_extractor.py   # 負責擷取畫面
├── ocr_engine.py        # 使用 EasyOCR 執行辨識
├── writer.py            # 輸出 txt / srt 字幕檔
├── utils.py             # 共用工具，如時間格式轉換
```

## 測試

```bash
poetry run pytest
```

## LICENSE

MIT
