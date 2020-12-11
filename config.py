# coding: utf-8
import os


class LogDefine:
    """log定义"""
    interval_del_time = 60 * 60
    logpath = os.path.abspath(os.path.dirname(__file__)) + '/logs'
    request_log_file = logpath + '/{}_request.log'
    log_level = {
        0: 'DEBUG',
        1: 'WARING',
        2: 'ERROR'
    }


class Return_Statua_Code:
    """返回状态定义"""
    ok = 200
    error = 500


class Sql:
    """mysql连接配置"""
    host = '127.0.0.1'
    password = '1234qwer'
    port = 3306
    user = 'root'
    db = 'site'
    max_cached = 10


class RedisSql:
    host = '127.0.0.1'
    port = 6379
    db = 0


class QQwrydat:
    path = os.path.abspath(os.path.dirname(__file__)) + '/qqwry_lastest.dat'
