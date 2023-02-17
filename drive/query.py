from googleapiclient.errors import HttpError

from utility.logger import log_error_to_file, log_info_to_file

def query_files(service, query):
  ## GET FILES WITH QUERY
  print(query)
  try:
    files= list()
    page_token=None
    response=None
    while True:
      # q=f"name contains {filename} and trashed=false and mimetype='application/vnd.google-apps.folder'",
      response=service.files().list(q=query,
                                    fields='nextPageToken, '
                                          'files(id, name)',
                                    pageToken=page_token).execute()
      for file in response.get('files', []):
        # Process change
        log_info_to_file(F'Found file: {file.get("name")}, {file.get("id")}')
        print(F'File found: {file.get("name")}, {file.get("id")}')
      #files=response.get('files', [])
      files.extend(response.get('files', []))
      page_token = response.get('nextPageToken', None)
      if page_token is None:
        break
    if len(files) > 0:
      return files
    else:
      return None
  except HttpError as error:
    log_error_to_file(error)
    print(f'An error occurred: {error}')