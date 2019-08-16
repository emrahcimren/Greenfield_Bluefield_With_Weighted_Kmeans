'''
Creates the main logger as well as the handlers to capture the logs
'''

import pathlib
import logging


def set_logger(run_id):

    '''
    File to create loggers
    :param run_id: Unique id of time
    :param logging_file_path: Where to save the file
    :param file_name: Name of the file
    :return:
    '''

    logger = logging.getLogger()

    main_path = pathlib.Path('logs')
    file_name = '__run_log___' + run_id + '.log'
    debug_file_handler = logging.FileHandler(filename=main_path / 'debug' / file_name, mode='w')
    warning_file_handler = logging.FileHandler(filename=main_path / 'warning' / file_name, mode='w')

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s')

    debug_file_handler.setFormatter(formatter)
    warning_file_handler.setFormatter(formatter)

    logger.addHandler(debug_file_handler)
    logger.addHandler(warning_file_handler)

    logger.setLevel(logging.DEBUG)

    debug_file_handler.setLevel(logging.DEBUG)
    warning_file_handler.setLevel(logging.WARNING)
