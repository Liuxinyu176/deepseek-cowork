---
name: yt-dlp-wrapper
description: Universal video downloader wrapper for yt-dlp. Supports YouTube and many other sites.
description_cn: 通用视频下载工具 (yt-dlp 封装)，支持 YouTube、B站等多种视频网站。
license: MIT
type: standard
created_by: system
allowed-tools: download_video
---

# yt-dlp Wrapper

This skill wraps the powerful `yt-dlp` library to provide video downloading capabilities.

## Key Features
- **Auto Dependency Management**: Automatically detects and installs `yt-dlp` if it's missing in the current environment.
- **Universal Support**: Works with thousands of video sites supported by yt-dlp.
- **Smart Defaults**: Downloads the best available single format to avoid strict dependency on FFmpeg (though FFmpeg is recommended for best quality 1080p+ merges).

## Tools

### download_video
Downloads a video or playlist from a given URL.

**Parameters:**
- `url`: The link to the video or playlist.
- `output_dir` (optional): The folder to save the video. Defaults to a `downloads` folder in the current directory.

**Returns:**
- A status message indicating the filename and location of the downloaded file.
