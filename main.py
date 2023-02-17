# BUILT-IN
from __future__ import print_function
import os.path
import sys
import json
from dotenv import load_dotenv
import argparse
from datetime import date, datetime

# THIRD-PARTY
import google.oauth2
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# from googleapiclient.http import MediaFileUpload

# CUSTOM PACKAGES
from drive.upload import upload_file, upload_file_to_folderID
from drive.list import get_files, list_root, list_children
from drive.query import query_files
from drive.create import create_folder
from utility.logger import log_error_to_file, log_info_to_file

# GLOBALS
SCOPES = ['https://www.googleapis.com/auth/drive.appdata',
          'https://www.googleapis.com/auth/drive.appfolder',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.metadata',
          'https://www.googleapis.com/auth/drive.file']

load_dotenv()  # load .env file
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')

# ## GET ARGS
# ARG_1=sys.argv[1]
print('\n\n')

def main():
    creds = None
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject='admin@yourdomain.com')
    # if not creds or not creds.valid:
    #   if creds and creds.expired and creds.refresh_token:
    #     creds.refresh(Request())
    #   else:
    #     creds = service_account.Credentials.from_service_account_file(
    #       SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject='admin@yourdomain.com')
    #   creds_b64=creds
    #   creds_to_json=''
    #   json.dump(creds, creds_to_json)
    #   print(creds_to_json)
    #   # with open(SERVICE_ACCOUNT_FILE, 'w') as keys_file:
    #     # keys_file.write(creds_to_json)

    try:
        service = build('drive', 'v3', credentials=creds)
        # files_to_upload=[
        #   '/_backup/images/20230118-010302_incremental_images_zipped.zip',
        #   '/_backup/images/20230118-130344_incremental_images_zipped.zip',
        #   ''
        #   ]
        # ## Multiple files upload
        # for item in files_to_upload:
        #   # mime_type application/zip
        #   upload_file(service, item, 'application/zip')
        # Single file upload
        # upload_file(service=service, file_to_upload='/_backup/images/20230119-131231_incremental_images_zipped.zip', mime_type='text/plain')

        # get_files(service)
        # files=query_files(service=service, query="name contains 'images'")
        # files=query_files(service=service, query="")
        # for file in files:
        #   print(F'File NAME: {file.get("name")} - File ID: {file.get("id")}')
        # query_files(service, query=f"name contains {}")

        # APP LOGIC
        # GLOBALS
        MIME_TYPE_ZIP = 'application/zip'
        MIME_TYPE_GOOGLE_FOLDER = 'application/vnd.google-apps.folder'  
        FILEPATH_TO_UPLOAD = ''
        FOLDER_TO_CREATE = ''
        TODAY_DATE = datetime.now().strftime("%Y%m%d")
        GDRIVE_ID_BACKUP_FOLDER_BEST = 'COMPANY_NAME_1_SUBFOLDER' # ROOT > COMPANY_NAME_1_SUBFOLDER > TODAY_DATE_FOLDER
        GDRIVE_ID_BACKUP_FOLDER_TOPCARD = 'COMPANY_NAME_2_SUBFOLDER' # ROOT > COMPANY_NAME_2_SUBFOLDER > TODAY_DATE_FOLDER
        GDRIVE_ID_BACKUP_FOLDER = ''

        if len(sys.argv) == 0:
            print('You must pass args:\n1. -p (--filepath) A /path/to/file/to/upload (non-required)\n2. -c (--create-folder) A string as "substring_to_search"\n')
            log_error_to_file(
                'You must pass args: 1. A /path/to/file/to/upload 2. A string as "substring_to_search" ')
            return
        parser = argparse.ArgumentParser(
            prog='py-uploader',
            description='A python script to upload file to Goolge Drive',
            epilog='Script developed by Zanetti Andrea'
        )

        parser.add_argument('-p', '--filepath', help='a path to file to upload', type=str, dest='filepath')
        # parser.add_argument('-i', '--folderId', help='The ID\'s folder on Google Drive where to upload the file', type=str)
        parser.add_argument('-c', '--create-folder', help='the name of the folder to create', type=str, dest='create_folder')
        parser.add_argument('-g', '--get-file', help='the name of the file to create', type=str, dest='get_file')
        parser.add_argument('-n', '--company-name', help='the name of the company in which upload folder', type=str, dest='company_name', required=True)
        parser.add_argument('list', help='the name of the company in which upload folder', nargs='?' )
        parser.add_argument('children', help='List children on the company folder', nargs='?')
        args = parser.parse_args()

        if args.company_name:
            print("args.company_name")
            if args.company_name == "topcard":
                GDRIVE_ID_BACKUP_FOLDER = GDRIVE_ID_BACKUP_FOLDER_TOPCARD
            if args.company_name == "bestcampings":
                GDRIVE_ID_BACKUP_FOLDER = GDRIVE_ID_BACKUP_FOLDER_BEST
        if args.filepath:
            if os.path.exists(args.filepath):
                FILEPATH_TO_UPLOAD = args.filepath
                # REMEMBER TO ADD INTO THE QUERY "... {FOLDER_ID_OF_BACKUP_BESTCAMPINGS} in parents ..."
                # query=f"'{GDRIVE_ID_BACKUP_FOLDER}' in parents and name contains '{TODAY_DATE}' and trashed=false and mimeType='{MIME_TYPE_GOOGLE_FOLDER}'"
                query_result=query_files(service=service, 
                                     query=f"'{GDRIVE_ID_BACKUP_FOLDER}' in parents and name contains '{TODAY_DATE}' and trashed=false and mimeType='{MIME_TYPE_GOOGLE_FOLDER}'")
                print(query_result)
                if query_result is not None and len(query_result) > 0:
                    print()
                    print("\n Se esiste il folder TODAY \n")
                    print("\n" + GDRIVE_ID_BACKUP_FOLDER + "\n")
                    TODAY_FOLDER_ID=query_result[0].get('id')
                    print("TODAY_FOLDER_ID: " + TODAY_FOLDER_ID)
                    upload_file_to_folderID(service=service, file_to_upload=FILEPATH_TO_UPLOAD, mime_type=MIME_TYPE_ZIP, folder_id=TODAY_FOLDER_ID)
                    return
                else:
                    print("\n Se NON esiste il folder TODAY \n")
                    print(GDRIVE_ID_BACKUP_FOLDER)
                    result = create_folder(service=service, folder_name=TODAY_DATE, parent_folder=GDRIVE_ID_BACKUP_FOLDER)
                    if result is not None:
                        print("\n Se è stato creato il folder TODAY \n")
                        print("\n" + result + '\n')
                        GDRIVE_ID_BACKUP_FOLDER=result.get('id')
                        upload_file_to_folderID(service=service, file_to_upload=FILEPATH_TO_UPLOAD, mime_type=MIME_TYPE_ZIP, folder_id=GDRIVE_ID_BACKUP_FOLDER)
                    else:
                        log_error_to_file(f"Something wrong occur when creating the folder with name {TODAY_DATE}")
            else:
                log_error_to_file(f"Folder with path {args.filepath} does not exists")
        if args.create_folder:
            print("\n FROM args.create_folder")
            FOLDER_TO_CREATE = args.create_folder
            create_folder(service=service, folder_name=FOLDER_TO_CREATE, parent_folder=GDRIVE_ID_BACKUP_FOLDER)
        if args.get_file:
            # TODO
            FILE_TO_SEARCH = args.get_file
        if args.list:
            if args.company_name == "root":
                list_root(service)
            elif args.children:
                files=[]
                # query=f"trashed=false and '{GDRIVE_ID_BACKUP_FOLDER}' in parents and name contains '{TODAY_DATE}' and mimeType='{MIME_TYPE_GOOGLE_FOLDER}'"
                children=query_files(service=service, 
                                     query=f"'{GDRIVE_ID_BACKUP_FOLDER}' in parents and name contains '{TODAY_DATE}' and trashed=false and mimeType='{MIME_TYPE_GOOGLE_FOLDER}'")
                print(children)
                for son in children:
                    files.append(query_files(service=service, query=f"trashed=false and '{son.get('id')}' in parents"))
                if len(files) > 0:
                    print(files)
                    print("Files Found: ")
                    for item in files:
                        print(f"FILE NAME: {item.get('name')} - FILE ID: {item.get('id')}")
                else:
                    print("No files found")
            get_files(service=service, trashed=False, parents_id=GDRIVE_ID_BACKUP_FOLDER, folder_name=None)

    except HttpError as error:
        log_error_to_file(error)
        print(f'An error occurred: {error}')

if __name__ == "__main__":
    main()
