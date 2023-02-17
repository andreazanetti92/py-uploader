import os
from datetime import datetime

PATH_TO_LOG_ERROR='/_script/log-err.html'
PATH_TO_LOG_INFO='/_script/log-info.html'
TEST_LOGGING='/_script/test-logging.txt'

formatted_today=datetime.now().strftime("%Y%d%m_%H:%M:%S")

def log_error_to_file(error):
  if error is not None:
    with open(PATH_TO_LOG_ERROR, 'a') as f:
      f.write(f"{formatted_today}: ERROR OCCURED: {error} \n")

def log_info_to_file(info):
  if info is not None:
    with open(PATH_TO_LOG_INFO, 'a') as f:
      f.write(f"{formatted_today}: INFO: {info} \n")