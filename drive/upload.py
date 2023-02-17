import os
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from utility.logger import log_error_to_file, log_info_to_file

# mime_type application/zip
def upload_file(service, file_to_upload, mime_type):
  """Upload file to google drive's root dir
  """
  ## UPLOAD A FILE TO ROOT GDRIVE
  try:
    # file_to_upload='backup_crontab.txt'
    fileName=''
    if file_to_upload is not None and os.path.exists(file_to_upload):
      fileName=file_to_upload.rsplit('/', 1)
      file_metadata={'name': fileName[1]}
      media=MediaFileUpload(file_to_upload, mimetype=mime_type)
      item=service.files().create(body=file_metadata, media_body=media, fields='id,name').execute()
      if item is not None:
        log_info_to_file(f"File {item.get('name')} successfully uploaded to root folder")
      else:
        log_error_to_file(f"Something went wrong on uploading file: {file_to_upload} to root folder")
    else:
      log_error_to_file(f"Unable to find the specified file to upload: {file_to_upload}")
  except HttpError as error:
    log_error_to_file(error)

def upload_file_to_folderID(service, file_to_upload: str, mime_type: str, folder_id: str):
  """Upload files to a folder by folder ID
  """
  try:
    if file_to_upload is not None and os.path.exists(file_to_upload) and folder_id is not None:
      fileName=file_to_upload.rsplit('/', 1)
      file_metadata={
        'name': fileName[1], 
        'parents': [folder_id]
        }
      media=MediaFileUpload(file_to_upload, mimetype=mime_type)
      item=service.files().create(
        body=file_metadata,
        media_body=media, 
        fields='id,name'
        ).execute()
      
      if item is not None:
        log_info_to_file(f"File {item.get('name')} successfully uploaded to folder with ID {folder_id}")
        return item
      else:
        log_error_to_file(f"Something went wrong on uploading file: {file_to_upload} to {folder_id}")
        return None
    elif file_to_upload is None or not os.path.exists(file_to_upload):
        log_error_to_file(f"Unable to find the specified file to upload: {file_to_upload}")
        return None
    elif folder_id is None:
      log_error_to_file(f"Unable to find the folder by the ID provided: {folder_id}")
      return None
  except HttpError as error:
    log_error_to_file(error)