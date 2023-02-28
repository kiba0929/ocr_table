import logging

logger = logging.getLogger('mylog')

def set_log():
    h = logging.FileHandler('log/development.log')
    h.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(message)s')
    h.setFormatter(fmt)
    logger.addHandler(h)