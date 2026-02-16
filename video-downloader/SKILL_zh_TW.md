---
name: youtube-downloader
description: 下載具備可自訂畫質與格式選項的 YouTube 影片。當使用者要求下載、儲存或擷取 YouTube 影片時使用。支援多種畫質設定（最佳、1080p、720p、480p、360p）、多種格式（mp4、webm、mkv），以及僅限音訊的 MP3 下載。
---

# YouTube 影片下載器 (YouTube Video Downloader)

下載 YouTube 影片並具備對畫質與格式設定的完整控制權。

## 快速開始

下載影片最簡單的方式：

```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

這將以最佳可用畫質下載 MP4 格式影片至 `/mnt/user-data/outputs/`。

## 選項說明

### 畫質設定 (Quality Settings)

使用 `-q` 或 `--quality` 指定影片畫質：

- `best` (預設)：可用的最高畫質
- `1080p`：Full HD
- `720p`：HD
- `480p`：標準畫質 (SD)
- `360p`：低畫質
- `worst`：可用的最低畫質

範例：
```bash
python scripts/download_video.py "網址" -q 720p
```

### 格式選項 (Format Options)

使用 `-f` 或 `--format` 指定輸出格式（僅限影片下載）：

- `mp4` (預設)：相容性最高
- `webm`：現代格式
- `mkv`：Matroska 封裝格式

範例：
```bash
python scripts/download_video.py "網址" -f webm
```

### 僅限音訊 (Audio Only)

使用 `-a` 或 `--audio-only` 僅下載 MP3 格式的音訊：

```bash
python scripts/download_video.py "網址" -a
```

### 自訂輸出目錄

使用 `-o` 或 `--output` 指定不同的輸出目錄：

```bash
python scripts/download_video.py "網址" -o /path/to/directory
```

## 完整範例

1. 以 1080p 下載 MP4 格式影片：
```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -q 1080p
```

2. 僅下載 MP3 格式音訊：
```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -a
```

3. 以 720p 下載 WebM 格式至自訂目錄：
```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -q 720p -f webm -o /custom/path
```

## 運作原理

此技能使用 `yt-dlp`，這是一款強大的 YouTube 下載工具，具備以下功能：
- 若環境中不存在，會自動進行安裝。
- 下載前先獲取影片資訊。
- 根據您的條件選擇最佳可用串流。
- 必要時合併影片與音訊串流。
- 支援廣泛的 YouTube 影片格式。

## 重要注意事項

- 預設情況下，下載內容儲存至 `/mnt/user-data/outputs/`。
- 影片檔名會根據影片標題自動生成。
- 腳本會自動處理 `yt-dlp` 的安裝作業。
- 僅支援單一影片下載（預設跳過播放清單 [Playlists]）。
- 高畫質影片下載時間較長，且佔用較多磁碟空間。
