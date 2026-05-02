import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def create_flow():
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=SCOPES
    )
    flow.redirect_uri = 'http://localhost:8000/oauth2callback'
    return flow


def get_drive_service(credentials):
    return build('drive', 'v3', credentials=credentials)


def list_files(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=10,
        fields="files(id, name)"
    ).execute()

    return results.get('files', [])


def download_file(service, file_id):
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)

    done = False
    while not done:
        _, done = downloader.next_chunk()

    try:
        return file.getvalue().decode('utf-8')
    except:
        return ""