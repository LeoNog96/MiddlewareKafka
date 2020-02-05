import os
import platform
import logging
import datetime

# KAFKA_SERVER = [os.environ.get('KAFKA_SERVER')]
KAFKA_SERVER = ['10.30.80.164:9092']

OS = platform.system()

DELIMITER = '/' if OS == 'Linux' else '\\'

PATH_PROJECT = os.path.abspath('.') + DELIMITER

RULES = PATH_PROJECT + 'configs'+DELIMITER+'rules.json'

date = datetime.datetime.now()

date = '{}_{}_{}'.format(date.day, date.month, date.year)

os.makedirs(os.path.dirname(PATH_PROJECT+'logs'+DELIMITER+'{}.log'.format(date)), exist_ok=True)

logging.basicConfig(
    filename=PATH_PROJECT+'logs'+DELIMITER+'{}.log'.format(date),
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

LOGGER = logging
