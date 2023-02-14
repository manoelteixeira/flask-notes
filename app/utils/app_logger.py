# app/utils/app_logger.py
import logging
from os import path
from sys import stdout


_logger_levels = {'notset':logging.NOTSET,
                  'debug':logging.DEBUG,
                  'info':logging.INFO,
                  'warning':logging.WARNING,
                  'error':logging.ERROR,
                  'critical':logging.CRITICAL}

def app_logger(logger_name:str , output_filename: str = None, format: str = None, level: str = None) -> logging.Logger:
    """
    Create and configure a Logger
    """
    
    # Logger instance
    logger = logging.getLogger(name=logger_name)
    
    # Set logger output format
    if format:
        output_format = format
    else:
        output_format = '[%(asctime)s]  %(name)s: [%(levelname)s] - %(message)s'
    
    output_formatter = logging.Formatter(output_format)
    
    # Set Stream Handler
    stream_handler = logging.StreamHandler(stream=stdout)
    stream_handler.setFormatter(fmt=output_formatter)
    logger.addHandler(hdlr=stream_handler)
    
    # Set File Handler if output file was given
    if output_filename:
        filename = output_filename if output_filename[-4:] == '.log' else f'{output_filename}.log'
        instance_dir = path.join(path.abspath(path.curdir), 'instance')
        if path.isdir(instance_dir):
            output_path = path.join(instance_dir, filename)
        else:
            output_path = filename
        
        file_handler = logging.FileHandler(filename=output_path)
        file_handler.setFormatter(fmt=output_formatter)
        logger.addHandler(file_handler)
        
    # Set logger level
    if level is None:
        logger.setLevel(_logger_levels.get('notset'))
    elif level in _logger_levels.keys():
        logger.setLevel(_logger_levels.get(level))        
    else:
        levels = ', '.join(list(_logger_levels.keys()))
        raise ValueError(f'Invalid value for level.\nThe valid levels are: {levels}.')
    
    return logger