# -*- coding: UTF-8 -*-
import logging,time,os
cur_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(os.path.dirname(cur_path), 'logs')

if not os.path.exists(log_path):
    os.mkdir(log_path)

class Log():
    def __init__(self):
        self.log_name = os.path.join(log_path, '%s.log' % time.strftime('%Y_%m_%d'))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')

    def __console(self, level, message):
        # fh = logging.FileHandler(self.log_name, 'a')   # 追加模式这个是python2的
        fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')  # 这个是 python3 的
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.debug(message)
        elif level == 'error':
            self.logger.error(message)

        # 这两行代码是为了避免日志输出重复问题,如果只有年月日就能去掉重复
        self.logger.removeHandler(fh)
        self.logger.removeHandler(ch)
        fh.close()

    def info(self, message):
        self.__console('info', message)

    def debug(self, message):
        self.__console('debug', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)

if __name__ == '__main__':
    log = Log()
    log.info('---测试开始---')
    log.info('---操作步骤1,2,3---')
    log.warning('---测试结束---')


