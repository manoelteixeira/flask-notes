# app/utils/app_logger.py
import logging
from os import path, makedirs
from sys import stdout
from flask.app import Flask

class AppLogger:
    """
    Create loggers 
    """
    
    def _get_level(self, level:str) -> int:
        logger_levels = {'notset':logging.NOTSET,
                  'debug':logging.DEBUG,
                  'info':logging.INFO,
                  'warning':logging.WARNING,
                  'error':logging.ERROR,
                  'critical':logging.CRITICAL}
        
        try:
            level = logger_levels[level]
            return level
        
        except KeyError:
            levels_list = ', '.join(list(logger_levels.keys()))
            raise ValueError(f'Invalid value for level.\nThe valid levels are: {levels_list}.')
    
    def __init__(self, log_to_file: bool = True, level: str = 'notset', app: Flask = None, format:str = None) -> None:
        
        self._log_to_file = log_to_file
        self._logs_path = None
        # Set ready state
        self._ready = True if log_to_file is False else False
        
        if app and log_to_file is True:
            self.init_app(app)
                        
        # Set default formatter
        if format is None:
            format = '[%(asctime)s]  %(name)s: [%(levelname)s] - %(message)s'
        self._formatter = logging.Formatter(format)
        
        # Set default logger level
        self._level = self._get_level(level)
    
    
    def init_app(self, app: Flask) -> None:
        """
        Initialize Loggers
        """
    
        if not path.isdir(app.instance_path):
            logging.warning('instance folder not found.')
        
        self._logs_path = path.join(app.instance_path,'App Logs')
        if not path.isdir(self._logs_path):
            makedirs(self._logs_path)    
        
        self._ready = True
    
    
    def new_logger(self, logger_name: str, logger_format: str = None, logger_level: str = None) -> logging.Logger:
        """ 
        Return a new Logger
        """
        
        formatter = logging.Formatter(logger_format) if logger_format is not None else self._formatter
        level = self._get_level(logger_level) if logger_level is not None else self._level
        
        logger = logging.getLogger(name=logger_name)
        logger.setLevel(level)
        # Stream Handler
        stream_handler =  logging.StreamHandler(stream=stdout)
        stream_handler.setFormatter(fmt=formatter)
        logger.addHandler(stream_handler)
        
        if self._ready is False: # In case AppLogger is not initialized
            return logger
            
        if self._log_to_file is True:
            filename = f"{logger_name.replace('.','-')}.log"
            logger_path = path.join(self._logs_path,filename)
            
            file_handler = logging.FileHandler(filename=logger_path)
            file_handler.setFormatter(fmt=formatter)
            logger.addHandler(file_handler)
        
        return logger
        
        
        
    
        