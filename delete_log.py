from datetime import timedelta, date
from config import LogDefine
from util.log import init
import time
import os


def timer_zsq(func):
    def inner(*args, **kwargs):
        day = time.strftime("%Y-%m-%d", time.localtime())
        while True:
            today = time.strftime("%Y-%m-%d", time.localtime())
            if day != today:
                func(*args, **kwargs)
                day = today
            time.sleep(LogDefine.interval_del_time)
    return inner


@timer_zsq
def del_old_log_file():
    today = time.strftime("%Y-%m-%d", time.localtime())
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
    lp = LogDefine.logpath
    for f in os.listdir(lp):
        if today not in f and yesterday not in f:
            print(f'删除日志文件 [{lp}/{f}]', 0, '删除日志')
            os.remove(f'{lp}/{f}')


if __name__ == '__main__':
    init()
    del_old_log_file()
