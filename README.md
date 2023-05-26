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

## Code

Here is the Python code:

```

import os
import moviepy.editor as mp
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv()

def upload_video_to_youtube(filename, title, description, tags, category):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE")

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_console()
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": category,
                "description": description,
                "title": title,
                "tags": tags
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=filename
    )
    response = request.execute()

    print(response)

def main():
    folder_path = input("Enter the path of the folder: ")

    video_files = [
        os.path.join(folder_path, f)
        for f in sorted(os.listdir(folder_path), key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
        if f.endswith('.mp4')
    ]

    clips = [mp.VideoFileClip(f) for f in video_files]
    final_clip = mp.concatenate_videoclips(clips)

    final_clip_path = os.path.join(folder_path, "final.mp4")
    final_clip.write_videofile(final_clip_path)

    upload_video_to_youtube(
        filename=final_clip_path,
        title=os.getenv("VIDEO_TITLE"),
        description=os.getenv("VIDEO_DESCRIPTION"),
        tags=os.getenv("VIDEO_TAGS").split(','),
        category=os.getenv("VIDEO_CATEGORY")
    )

if __name__ == '__main__':
    main()
```