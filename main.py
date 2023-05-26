import json
import os
import moviepy.editor as mp
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from dotenv import load_dotenv


def authenticate_youtube_api():
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE")
    CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")

    # If the credentials file doesn't exist, run the console flow and save the credentials
    if not os.path.exists(CREDENTIALS_FILE):
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        credentials = flow.run_console()
        # Save the refresh token for the next run
        with open(CREDENTIALS_FILE, 'w') as token:
            token.write(json.dumps({
                "client_id": flow.client_config['client_id'],
                "client_secret": flow.client_config['client_secret'],
                "refresh_token": credentials.refresh_token,
                "token_uri": flow.client_config['token_uri'],
                "scopes": SCOPES
            }))
    else:
        credentials = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)

    return credentials


def upload_video_to_youtube(credentials, filename, title, description, tags, category):
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'

    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    media_file = MediaFileUpload(filename, chunksize=-1, resumable=True, mimetype='video/*')

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "description": description,
                "title": title,
                "tags": tags
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=media_file
    )
    response = request.execute()

    print(response)


def main():
    load_dotenv()

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    credentials = authenticate_youtube_api()

    folder_path = input("Enter the path of the folder: ")
    video_title = input("Enter the title of the video: ")

    output_folder = os.path.join(folder_path, "output")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    final_clip_path = os.path.join(output_folder, f"{video_title}.mp4")

    # Check if final_clip_path exists, if not, join the video files
    if not os.path.exists(final_clip_path):
        video_files = [
            os.path.join(folder_path, f)
            for f in sorted(os.listdir(folder_path), key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
            if f.endswith('.mp4')
        ]

        clips = [mp.VideoFileClip(f) for f in video_files]
        final_clip = mp.concatenate_videoclips(clips)

        final_clip.write_videofile(final_clip_path)

    upload_video_to_youtube(
        credentials=credentials,
        filename=final_clip_path,
        title=video_title,
        description=os.getenv("VIDEO_DESCRIPTION"),
        tags=os.getenv("VIDEO_TAGS").split(','),
        category=os.getenv("VIDEO_CATEGORY")
    )


if __name__ == '__main__':
    main()
