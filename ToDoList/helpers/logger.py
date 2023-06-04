import logging
from ToDoList import config

log = logging.getLogger()

if config.LOGGING_LEVEL.upper() == 'INFO':
    LEVEL = logging.INFO
elif config.LOGGING_LEVEL.upper() == 'DEBUG':
    LEVEL = logging.DEBUG
else:
    LEVEL = logging.NOTSET

logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=LEVEL
)
