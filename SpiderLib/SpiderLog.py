#!/usr/local/python/bin
# coding=utf-8

__author__ = "tuantuan.lv <dangoakachan@foxmail.com>"
__status__ = "Development"

__all__ = ['set_logger', 'debug', 'info', 'warning', 'error',
        'critical', 'exception']

import os
import sys
import logging
import logging.handlers

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
                        FileTransferSpeed, FormatLabel, Percentage, \
                        ProgressBar, ReverseBar, RotatingMarker, \
                        SimpleProgress, Timer

widgets = [' ', Percentage(), ' ',
               Bar(marker='=',left=' [',right='] '),
               ' ', ETA(), ' ', '']
pbar = ProgressBar(widgets=widgets, maxval=500)


import Queue
log_Q = Queue.Queue()
def add_log(fun_log):
	log_Q.put(fun_log)
	log_Q.get()
def ex_log():
	while True:
		if log_Q.empty():
			break		
		else:
			log_Q.get()
log_level = {
		5:'DEBUG',
		4:'INFO',
		3:'WARNING',
		2:'ERROR',
		1:'CRITICAL',
		#0:'EXCEPTION'
	}


COLOR_RED='\033[1;31m'
COLOR_GREEN='\033[1;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[1;34m'
COLOR_PURPLE='\033[1;35m'
COLOR_CYAN='\033[1;36m'
COLOR_GRAY='\033[1;37m'
COLOR_WHITE='\033[1;38m'
COLOR_RESET='\033[1;0m'


LOG_COLORS = {
        'DEBUG': '%s',
        'INFO': COLOR_GREEN + '%s' + COLOR_RESET,
        'WARNING': COLOR_YELLOW + '%s' + COLOR_RESET,
        'ERROR': COLOR_RED + '%s' + COLOR_RESET,
        'CRITICAL': COLOR_RED + '%s' + COLOR_RESET,
        'EXCEPTION': COLOR_RED + '%s' + COLOR_RESET,
        }


g_logger = None

class ColoredFormatter(logging.Formatter):

    def __init__(self, fmt = None, datefmt = None):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)

        return LOG_COLORS.get(level_name, '%s') % msg

def add_handler(cls, level, fmt, colorful, **kwargs):
    global g_logger

    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.DEBUG)

    handler = cls(**kwargs)
    handler.setLevel(level)

    if colorful:
        formatter = ColoredFormatter(fmt)
    else:
        formatter = logging.Formatter(fmt)

    handler.setFormatter(formatter)
    g_logger.addHandler(handler)

    return handler

def add_streamhandler(level, fmt):
    return add_handler(logging.StreamHandler, level, fmt, True)

def add_filehandler(level, fmt, filename , mode, backup_count, limit, when):
    kwargs = {}

    if filename is None:
        filename = getattr(sys.modules['__main__'], '__file__', 'log.py')
        filename = os.path.basename(filename.replace('.py', '.log'))
        filename = os.path.join('/tmp', filename)

    kwargs['filename'] = filename

    if backup_count == 0:
        cls = logging.FileHandler
        kwargs['mode' ] = mode
    elif when is None:
        cls = logging.handlers.RotatingFileHandler
        kwargs['maxBytes'] = limit
        kwargs['backupCount'] = backup_count
        kwargs['mode' ] = mode
    else:
        cls = logging.handlers.TimedRotatingFileHandler
        kwargs['when'] = when
        kwargs['interval'] = limit
        kwargs['backupCount'] = backup_count

    return add_handler(cls, level, fmt, False, **kwargs)

def init_logger():
    global g_logger

    if g_logger is None:
        g_logger = logging.getLogger()
    else:
        logging.shutdown()
        g_logger.handlers = []

    g_logger.setLevel(logging.DEBUG)

def set_logger(filename = None, mode = 'a', level='ERROR:DEBUG',
        fmt = '[%(levelname)s] %(asctime)s %(message)s',
        backup_count = 5, limit = 20480, when = None):
    level = level.split(':')

    if len(level) == 1:
        s_level = f_level = level[0]
    else:
        s_level = level[0]
        f_level = level[1]

    init_logger()
    add_streamhandler(s_level, fmt)
    add_filehandler(f_level, fmt, 'log/'+filename, mode, backup_count, limit, when)
 
    import_log_funcs()

def import_log_funcs():
    global g_logger

    curr_mod = sys.modules[__name__]
    log_funcs = ['debug', 'info', 'warning', 'error', 'critical',
            'exception']

    for func_name in log_funcs:
        func = getattr(g_logger, func_name)
        setattr(curr_mod, func_name, func)


#set_logger(level='DEBUG:DEBUG')

#log.debug('hello, world')
#log.info('hello, world')
#log.error('hello, world')
#log.critical('hello, world')
