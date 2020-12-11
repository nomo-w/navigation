# coding: utf-8


from flask import Flask, request, redirect
from db.main_domain import MainDomain
from db.routedb import Route
from db.sheng import Sheng
from db.peizhi import PeiZhi
from flask_cors import CORS
from util import api
from util import log
import random
import json


app = Flask('web')
CORS(app, supports_credentials=True)
app.secret_key = 'ABCAz47j22AA#R~X@H!jLwf/A'
log.init()


# --------------------------------------------------------
# 路由跳转
# --------------------------------------------------------
@app.route('/nav/<site>')
@api.handle_api_zsq('/nav/', 'get')
def get_route(site):
    if site == 'main':
        with MainDomain() as db:
            domains = db.get_domain()
            if domains:
                domain = random.choice(domains)
                if domain[:4] == 'http':
                    return redirect(domain)
                return redirect(f'http://{domain}')
            else:
                return api.handle_httpresponse('未找到!', -1)
    with Route() as db:
        jumpto = db.get_route(site)
    if jumpto is None:
        return api.handle_httpresponse('未找到!', -1)
    if api.handle_ip(request.headers.get("X-Real-IP")):
        with MainDomain() as db:
            domains = db.get_domain()
            if domains:
                domain = random.choice(domains)
                if domain[:4] == 'http':
                    return redirect(domain)
                return redirect(f'http://{domain}')
    return redirect(jumpto)


# --------------------------------------------------------
# 更新配置
# --------------------------------------------------------
@app.route('/api/update_main', methods=['POST'])
@api.handle_api_zsq('/api/update_main', 'post')
def update_main():
    data = request.data.decode()
    data = json.loads(data)
    domains = data['domains']
    domains = domains.split(',')
    need_display_main, need_display_logo = data['need_display_main'], data['need_display_logo']
    need_switch = data['need_switch']
    if need_switch == '1':
        switch_area, switch_time_start, switch_time_end = data['switch_area'], data['switch_time_start'], data['switch_time_end']
        switch_area = switch_area.split(',')
    else:
        switch_area, switch_time_start, switch_time_end = [], '', ''
    with PeiZhi() as db:
        resp = db.update_peizhi(domains, need_display_main, need_display_logo, need_switch, switch_area, switch_time_start, switch_time_end)
    return api.handle_httpresponse('ok', 0)


# --------------------------------------------------------
# 获取配置/地区
# --------------------------------------------------------
@app.route("/api/get_config")
@api.handle_api_zsq('/api/get_config', 'GET')
def get_config():
    type_ = request.args['t']
    if type_ == 'area':
        # 获取地区
        with Sheng() as db:
            data = db.get_sheng()
    elif type_ == 'config':
        # 获取配置
        with PeiZhi() as db:
            data = db.get_peizhi()
        with MainDomain() as db:
            domains = db.get_domain()
        with Sheng() as db:
            shengs = db.get_need_switch_id()
        data['domains'] = domains
        data['area'] = shengs
    elif type_ == 'simple':
        with PeiZhi() as db:
            data = db.get_simple()
    return api.handle_httpresponse(data, 0)


# Main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, threaded=True)
