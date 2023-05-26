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
