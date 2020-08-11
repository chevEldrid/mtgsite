from __future__ import print_function
import pickle
import datetime
import os
import io
import shutil
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

# article_pull.py checks a provided Drive folder for changes past a stored date.
# If the most recent changes are recorded - great. Exit
# if not, iterate through the list of files until you reach the one that IS accounted for and break.

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
DRIVE_FOLDER_ID = '1O5NRN2jiGKICcNrdJYIohAmG20uq9esw'

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    #loads last accessed date from file, or leaves blank
    try:
        print("made it here")
        with open ("changelog.txt", "r") as f:
            for line in f:
                prevDate = datetime.datetime.strptime(line[0:26], "%Y-%m-%d %H:%M:%S")
                #for google b/c reasons
                prevDate = str(prevDate).replace(" ","T") 
                print("previous date found!")
    except IOError:
        prevDate = datetime.datetime.now()
        print("changelog not found, setting to current time")

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API - get file names and ids from the DRIVE_FOLDER of all files after the last recorded datetime
    results = service.files().list(q="'{0}' in parents and trashed=false and modifiedTime > '{1}'".format(DRIVE_FOLDER_ID, prevDate),
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    # Check if most recent file is present in our _posts directory...
    #if it is - great! We're up to date.
    #if not, check all files (?) 
    if not items:
        print('No files found posted after your last check!')
        exit(0)
    else:
        print('New Files Found! Downloading...')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            file_id = item['id']
            request = service.files().get_media(fileId=file_id)
            fh = io.FileIO(item['name'], 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download {0}".format(int(status.progress() * 100)))
            #move to correct directory
            #file_name = "{0}.md".format(item['name'])
            shutil.move(item['name'], '../_posts')
        print("files downloaded successfully!")




    # set time of completion, save to disk
    f = open("changelog.txt", "w+")
    f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    f.close()

if __name__ == '__main__':
    main()