#!/usr/bin/env python
#coding=utf-8

import logging
import logging.config
import logging.handlers

# Color escape string
COLOR_RED='\033[1;31m'
COLOR_GREEN='\033[1;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[1;34m'
COLOR_PURPLE='\033[1;35m'
COLOR_CYAN='\033[1;36m'
COLOR_GRAY='\033[1;37m'
COLOR_WHITE='\033[1;38m'
COLOR_RESET='\033[1;0m'

# Define log color
LOG_COLORS = {
        1: '%s',
        2: COLOR_GREEN + '%s' + COLOR_RESET,
        3: COLOR_YELLOW + '%s' + COLOR_RESET,
        4: COLOR_RED + '%s' + COLOR_RESET,
        5: COLOR_RED + '%s' + COLOR_RESET,
        6: COLOR_RED + '%s' + COLOR_RESET,
        }


class SpiderLog(object):
    '''日志处理模块
    '''
    def __init__(self):
        logging.config.fileConfig('Logging.conf')
    def get_logger(self, logger_name):
        return logging.getLogger(logger_name)
    def log_msg(self, log_level, str_msg, logger):
        LOG_COL_MSG = LOG_COLORS.get(log_level, '%s') % str_msg
        LEVEL_MSG = {
                1:logger.debug(LOG_COL_MSG),
                2:logger.info(LOG_COL_MSG),
                3:logger.warn(LOG_COL_MSG),
                4:logger.error(LOG_COL_MSG),
                5:logger.critical(LOG_COL_MSG),
                }
        LEVEL_MSG.get(log_level)


if __name__=='__main__':
    log = SpiderLog()
    logger = log.get_logger('Spider')
    log.log_msg(1,'debug msg', logger)
    log.log_msg(2,'info msg', logger)
    log.log_msg(3,'warn msg', logger)
    log.log_msg(4,'error msg', logger)
    log.log_msg(5,'critical msg', logger)
    logger2 = log.get_logger('Spider.App')
    log.log_msg(1,'debug msg', logger2)
    log.log_msg(2,'info msg', logger2)
    log.log_msg(3,'warn msg', logger2)
    log.log_msg(4,'error msg', logger2)
    log.log_msg(5,'critical msg', logger2) 
