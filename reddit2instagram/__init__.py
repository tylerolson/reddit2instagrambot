import logging.config
import json
import os
import sys

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
sys.path.append(dir_path)

with open(dir_path + '/logging_config.json', 'r') as fp:
    logging.config.dictConfig(json.load(fp))

logger = logging.getLogger('main')
logger.debug('Logger config successfully loaded')
