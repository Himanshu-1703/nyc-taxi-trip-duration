import logging
from pathlib import Path
import datetime as dt

def create_log_path(filename: str) -> str:
    current_date = dt.date.today()
    # create a logs folder in the root directory
    root_path = Path(__file__).parent.parent
    # create path for logs folder
    log_dir_path = root_path / 'logs'
    log_dir_path.mkdir(exist_ok=True)
    
    # create folder for a specific module
    module_log_path = log_dir_path / filename
    module_log_path.mkdir(exist_ok=True,parents=True)
    # convert the date to str
    current_date = current_date.strftime("%d-%m-%Y") # ! error at this point if not fixed
    # create log files based on current date
    log_file_name = module_log_path / (current_date + '.log')
    return log_file_name


class CustomLogger:
    def __init__(self,logger_name):
        pass
        

# if __name__ == "__main__":
#     print(create_log_path('test'))