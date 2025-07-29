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
- `--deduplicate`: 去除重複的字幕條目（可選）
- `--auto-filename`: 使用字幕內容作為檔案名稱（需要搭配 `--deduplicate` 使用）

### 範例

#### 基本使用
```bash
poetry run subocr input.mp4 --fps 0.5 --format srt --lang en,ch_tra
```

#### 使用去重複功能
```bash
poetry run subocr input.mp4 --fps 0.5 --format srt --lang en,ch_tra --deduplicate
```

#### 使用自動檔名功能（根據字幕內容命名）
```bash
poetry run subocr input.mp4 --fps 0.5 --format srt --lang en,ch_tra --deduplicate --auto-filename
```

## 專案結構

```tree
subtitle_extractor/
├── cli.py               # CLI 入口點，包含新的去重複和自動檔名功能
├── frame_extractor.py   # 負責擷取畫面
├── ocr_engine.py        # 使用 EasyOCR 執行辨識
├── writer.py            # 輸出 txt / srt 字幕檔，支援自訂檔名
├── utils.py             # 共用工具，如時間格式轉換、去重複邏輯、檔名處理
```

## 功能特色

- **影片畫面擷取**：使用 FFmpeg 從影片中擷取特定 FPS 的畫面
- **多語言 OCR**：支援英文、繁體中文、日文等語言辨識
- **多種輸出格式**：支援 TXT 和 SRT 字幕格式
- **去重複功能**：自動過濾相似的重複字幕條目
- **智慧檔名**：可根據字幕內容自動生成檔案名稱

## 測試

```bash
poetry run pytest
```

## LICENSE

MIT
