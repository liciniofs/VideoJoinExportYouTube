# YouTube Video Uploader

This Python script automatically joins all .mp4 videos from a specified folder, sorts them by date/time, and uploads the final video to YouTube.

## Prerequisites

Make sure to have these packages installed. If not, you can install them via pip:

- `moviepy`
- `google-api-python-client`
- `google-auth-oauthlib`
- `python-dotenv`

Also, you'll need to set up a project in the Google Developers Console, enable the YouTube Data API v3, and download your client_secret.json credentials file. More details can be found in the [YouTube API Python Quickstart guide](https://developers.google.com/youtube/v3/quickstart/python).

## Usage

1. Create a `.env` file in the same directory as your Python script. Replace the placeholders with your actual values:

```
CLIENT_SECRET_FILE=your_client_secret_file_path
VIDEO_TITLE=your_video_title
VIDEO_DESCRIPTION=your_video_description
VIDEO_TAGS=tag1,tag2
VIDEO_CATEGORY=your_video_category
```

2. Run the script with Python and follow the prompts:

```
python your_script.py
```

When prompted, enter the path to the folder that contains the videos you want to join and upload.