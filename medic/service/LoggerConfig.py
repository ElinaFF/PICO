import logging
import coloredlogs
from datetime import datetime
import inspect
import os
import threading
import traceback
from functools import wraps

log_filename = None  # Global variable for log filename

def log_exceptions(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Log the exception or handle it as needed
                thread_name = threading.current_thread().name
                logger.error(f"Error in thread {thread_name}: {e}\n{traceback.format_exc()}")
                raise # Re-raise the exception to preserve the original
        return wrapper
    return decorator

def set_log_filename(filename: str="MetaboDashBoard.log", add_date: bool=True, level=logging.DEBUG):
    """Sets th elog filename with an optional date suffix.

    Args:
        filename (str, optional): The base filename for the log. Defaults to "MetaboDashBoard.log".
        add_date (bool, optional): If True, adds the current date to the filename. Defaults to True.
    """
    global log_filename

    if add_date:
        date_str = datetime.now().strftime("%Y-%m-%d")
        if filename.lower().endswith(".log"):
            log_filename = filename.replace(".log", f"_{date_str}.log")
        else:
            log_filename = f"{filename}_{date_str}.log"
    else:
        log_filename = filename
        
    # Ensure the Logs directory exists
    logs_directory = get_logs_directory()
    log_filename = os.path.join(logs_directory, log_filename)
    
     # Add "-----------------------" in the log file to start the current session
    with open(log_filename, 'a') as log_file:
        if threading.current_thread() is threading.main_thread():
            log_file.write(f"\n{'----- New start (' + threading.current_thread().name + ') ':-<80}\n")
        else:
            log_file.write(f"      New thread ({threading.current_thread().name})\n")
    
    return init_logger(level=level)
        
def init_logger(module_name: str=None, level=logging.DEBUG):
    """"MetaboDashBoard.log"

    Args:
        module_name (str, optional): The name of the module for the logger. Defaults to "".
        level (int, optional): The logging level. Defaults to logging.DEBUG.
            Levels (from high to low): logging.CRITICAL logging.ERROR
                                       logging.WARNING logging.INFO logging.DEBUG

    Returns:
        logging.Logger: The configured logger instance
    """
    global log_filename
    if log_filename is None:
        raise ValueError("The log filename must be initialized app.")

    # Get the calling module's name
    if module_name is None:
        frame = inspect.currentframe().f_back
        module_name = inspect.getmodule(frame).__name__

    # Create a logger
    logger = logging.getLogger(module_name)
    logger.setLevel(level)

     # Clear existing handlers to ensure the logger is re-configured each time
    logger.handlers = []
    
    # Create a handler to write logs to a file
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)

    # Create a handler to write logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # Configure colored logs for the console
    coloredlogs.install(level=level, logger=logger, stream=console_handler.stream)
    # coloredlogs.install(fmt='%(asctime)s,%(msecs)03d %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s')

    # Create a formatter and add it to the handlers
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logs_directory():
    """
    Returns the path to the 'Logs' directory within the 'Documents' directory if it exists,
    otherwise within the user's home directory.
    """
    home_directory = os.path.expanduser("~")
    logs_directory = os.path.join(home_directory, ".medic", "logs")
    
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)
        
    if not os.path.exists(logs_directory):
        logs_directory = os.getcwd()
    
    return logs_directory

