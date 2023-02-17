from googleapiclient.errors import HttpError

from utility.logger import log_error_to_file, log_info_to_file

def list_root(service):
  ## GET FILES FROM ROOT GDRIVE
  try:
    results = service.files().list(
      fields="files(id, name)"
    ).execute()
    
    items = results.get('files', [])

    if not items:
      log_info_to_file("No File was found")
      print('No files found')
      return

    print('Files: ')
    for item in items:
      log_info_to_file(u'{0} ({1})'.format(item['name'], item['id']))
      print(u'{0} ({1})'.format(item['name'], item['id'])) 
    return items
  except HttpError as error:
    log_error_to_file(error)
    print(f'An error occurred: {error}')
    
def list_children(service, parent_id):
  files=[]
  page_token = None
  while True:
    try:
      param={}
      if page_token:
        param['pageToken'] = page_token
      children = service.children().list(
        folderId=parent_id).execute()
      files.append(children.get('items', []))
      page_token = children.get('nextPageToken')
      if not page_token:
        break
    except HttpError as error:
      log_error_to_file(f"Unable to list children in parent_folder with ID: {parent_id}. ERROR: {error}")
  if len(files) > 0:
    return files
  else:
    log_info_to_file(f"No children were found in parent folder with ID {parent_id}")
    return None

def get_files(service, trashed=False, parents_id=None, folder_name=None):
  ## GET FILES FROM ROOT GDRIVE
  try:
    q=f"trashed={trashed}"
    if parents_id is not None:
      q+=f" and '{parents_id}' in parents"
    if folder_name is not None:
      q+=f" and name contains '{folder_name}'"
    results = service.files().list(
      q=q,
      fields="files(id, name)"
    ).execute()
    
    items = results.get('files', [])

    if not items:
      log_info_to_file("No File was found")
      print('No files found')
      return

    print('Files: ')
    for item in items:
      log_info_to_file(u'{0} ({1})'.format(item['name'], item['id']))
      print(u'{0} ({1})'.format(item['name'], item['id'])) 
    return items
  except HttpError as error:
    log_error_to_file(error)
    print(f'An error occurred: {error}')
