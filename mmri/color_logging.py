import logging
import copy
from colorful import colorstr

logger = logging.getLogger(__name__)

class ColoredFormatter(logging.Formatter):
    # A variant of code found at http://stackoverflow.com/questions/384076/how-can-i-make-the-python-logging-output-to-be-colored
    LEVELCOLOR = {
        # 'DEBUG': 'BLUE',
        # 'INFO': 'BLACK',
        'WARNING': 'YELLOW',
        'SUCCESS': 'GREEN',
        'ERROR': 'RED',
        'CRITICAL': 'RED_BG',
        }

    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self, record):
        record = copy.copy(record)
        levelname = record.levelname
        if levelname in self.LEVELCOLOR:
            record.levelname = colorstr(levelname,self.LEVELCOLOR[levelname])
            record.name = colorstr(record.name,'BOLD')
            record.msg = colorstr(record.msg,self.LEVELCOLOR[levelname])
        return logging.Formatter.format(self, record)

if __name__=='__main__':
    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setFormatter(
        ColoredFormatter('%(name)s: %(message)s (%(filename)s:%(lineno)d)'))
    logger.addHandler(console)
    fh = logging.FileHandler('/tmp/test.log','w')
    fh.setFormatter(logging.Formatter('%(name)s: %(message)s'))
    logger.addHandler(fh)

    logger.debug('debug')
    logger.info('info')
    logger.warning('Warning')
    logger.error('ERROR')
    logger.critical('CRITICAL!!!')
