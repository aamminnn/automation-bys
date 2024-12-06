import logging
import os
import datetime
import configparser
from counter import counter

config = configparser.ConfigParser()
with open("config.ini","r") as file_object:
    config.read_file(file_object)
instance_version = config.get('instance_setting','instance_version')
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
log_counter_filename = "./ignore/log_counter.txt"  #Formatted repo name
log_counter = counter(log_counter_filename)


class AutomationScriptLog:
    def __init__(self,log_folder) -> None:
        # log_file = f"{instance_version}_{current_date}_automation_script_{log_counter}.log"
        log_file = f"{current_date}_automation_script.log"
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        log_path = os.path.join(log_folder, log_file)

        self.logger = logging.getLogger('Automation_Script_Log')
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def create_folder_if_not_exists(self):
        if not os.path.exists(self.log_pa):
            os.mkdir(self.folder_path)
    
    def info(self, message):
        self.logger.info(message)
    
    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message, display:bool=False):
        self.logger.debug(message)
        if display:
            print(message)

logger = AutomationScriptLog(r'./logs')

# def logger(log_type, log_message):
#     current_date = datetime.datetime.now().strftime("%Y-%m-%d")
#     current_time = datetime.datetime.now().strftime("%H-%M-%S")
#     # Define the log file name format
#     log_filename = f"{version}_{current_date}_{current_time}.log"
#     #TODO: problem is when call, each time create new log object -> new log file everytime
#     log = AutomationScriptLog(r'./logs', log_filename)
#     if log_type == 'info': # For important message such as header
#         logger = log.info(log_message)
#     elif log_type == 'debug': # For normal log message
#         logger = log.debug(log_message)
#     elif log_type == 'warning':
#         logger = log.warning(log_message)
#     elif log_type == 'error':
#         logger = log.warning(log_message)
#     else:
#         print(f"There is no option {log_type}. Please use log_type info/debug/warning/error")
#     return logger


# logging.basicConfig(
#     filename=log_file_name,
#     level=logging.DEBUG,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# # Create a logger
# logger = logging.getLogger('Automation_Script_Output_Log')
# # Generate log entries
# logger.debug("This is a debug message")
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")