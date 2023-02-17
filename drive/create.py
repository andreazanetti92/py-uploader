from googleapiclient.errors import HttpError
from utility.logger import log_error_to_file, log_info_to_file
from .query import query_files

def create_folder(service, folder_name, parent_folder=None):
  try:
    # print(parent_folder)
    # if folder_name is not None:
    #   result=query_files(service=service, query=f"trashed=false and name contains '{folder_name}'")
    #   if result is None:
    file_metadata={
      'name': folder_name,
      'mimeType': 'application/vnd.google-apps.folder',
      'parents': [parent_folder]
    }
    item=service.files().create(body=file_metadata, fields='id, name').execute()
    if item is not None:
      log_info_to_file(f"Folder with NAME: {item.get('name')} and ID: {item.get('id')} was created successfully")
      return item
    else:
      log_error_to_file(f"Something wrong in the creation of the folder {folder_name}")
      return None
      # else:
      #   log_info_to_file(f"Folder with NAME: {folder_name} already exists")
    # else:
    #   log_error_to_file("You must provide a folder name in order to create it")
    #   return None
    return None
  except HttpError as error:
    log_error_to_file(error)
    print(f'An error occurred: {error}')