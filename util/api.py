# coding: utf-8

from db.peizhi import PeiZhi
from functools import wraps
from db.sheng import Sheng
from flask import request
from qqwry import QQwry
from config import *

import traceback
import requests
import time
import json

# 屏蔽https告警
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def handle_httpresponse(data, status=-1, other={}):
    '''
    处理返回结果
    :param data: 数据
    :param status: 返回状态 0(成功) -1(不成功)
    :param other: 其他需要加入的数据
    :return: json格式的数据
    '''
    return_dic = {'data': data, 'status': Return_Statua_Code.error}
    if status == 0:
        return_dic['status'] = Return_Statua_Code.ok
    if other:
        for i in other:
            return_dic[i] = other[i]
    return json.dumps(return_dic)


# --------------------------------------------------------
# 装饰器
# --------------------------------------------------------
def handle_api_zsq(api_path, method):
    # 处理http response装饰器
    def zsq(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if method == 'get':
                _ = f'{request.headers.get("X-Real-IP")} {method.upper()} => {api_path}{list(kwargs.values())[0]} : 【{request.args}】'
            else:
                _ = f'{request.headers.get("X-Real-IP")} {method.upper()} => {api_path} : ' \
                    f'【{request.args if method == "GET" else request.form if method == "POST" else request.data}】'
            print(_, 0, 'request', LogDefine.request_log_file.format(time.strftime("%Y-%m-%d", time.localtime())))
            try:
                resp = func(*args, **kwargs)
            except KeyError:
                # traceback.print_exc()
                resp = handle_httpresponse('参数错误!')
            except Exception as e:
                # traceback.print_exc()
                er = ";".join(traceback.format_exc().split("\n"))
                print(f'服务器错误, 错误原因 [{er}]!!!', 2, '服务器错误')
                resp = handle_httpresponse(f'服务器错误, 错误原因 [{e}]')
            return resp
        return inner
    return zsq


def my_requests(url, method, params=None, headers=None, need_json_resp=True,
                verify=False, need_json_params=False, need_proxies=False, proxies=None, need_content=False):
        '''
        发送requests的请求
        :param url: 目标url
        :param headers: 请求头
        :param params: 请求参数
        :param method: 请求方法
        :param is_json: 是否返回json数据
        :param verify: ssl验证
        :param need_handle_resp: 是否需要处理数据
        :return: 返回响应参数
        '''
        try:
            data = {'url': url, 'verify': verify, 'timeout': (10, 10)}
            if params is not None:
                data['params' if method == 'get' else 'data'] = json.dumps(params) if need_json_params else params
            if need_proxies:
                data['proxies'] = proxies
            if headers is not None:
                data['headers'] = headers

            if method == 'get':
                resp = requests.get(**data)
            elif method == 'post':
                resp = requests.post(**data)

            if resp.status_code is not 200:
                print(f'请求 [{url}] 失败. 返回状态码 [{resp.status_code}]. 失败原因 [{resp.reason}]', 2, '发送网络请求错误')
                return None
            return resp.json() if need_json_resp else resp.content if need_content else resp.text
        except Exception as e:
            # traceback.print_exception()
            print(f'请求 [{url}] 失败. 失败原因 [{e}]', 2, '发送网络请求错误')
            return None


def handle_ip(ip):
    q = QQwry()
    q.load_file(QQwrydat.path)
    _ = q.lookup(ip)
    with PeiZhi() as db:
        data = db.get_peizhi()
    if data['need_switch'] == 1:
        now = time.strftime("%H:%M", time.localtime())
        if now >= data['switch_time_start'] and now <= data['switch_time_end']:
            with Sheng() as db:
                for i in db.get_need_switch():
                    if i in _[0]:
                        return True
    return False
