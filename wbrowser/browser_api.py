import random
import re
import string
import time

import pandas as pd
import requests
import json
from selenium import webdriver

from functions.log_dp import log_dispatcher
from wbrowser.proxy_preference import check_proxy


def create_driver(session, port):
    """create driver"""
    mla_url = f'http://127.0.0.1:{port}/api/v1/profile/start?automation=true&profileId=' + session
    resp = requests.get(mla_url)
    json = resp.json()
    options = webdriver.ChromeOptions()
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")
    options.add_argument("--auto-open-devtools-for-tabs")
    driver = webdriver.Remote(command_executor=json['value'], options=options)
    return driver


def update_profile_proxy(profile_id, proxy_type, proxy_host, proxy_port, proxy_username, proxy_password, port):
    """update profile proxy"""
    url = f'http://localhost:{port}/api/v2/profile/' + profile_id
    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "network": {
            "proxy": {
                "type": proxy_type,
                "host": proxy_host,
                "port": proxy_port,
                "username": proxy_username,
                "password": proxy_password
            }
        }
    }
    r = requests.post(url, json.dumps(data), headers=header)
    log_dispatcher.info(to_write=r.status_code)


def update_profile_group(profile_id, port, group_id):
    """Update profile group"""
    url = f'http://localhost:{port}/api/v2/profile/' + profile_id
    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "group": group_id,
    }
    r = requests.post(url, json.dumps(data), headers=header)
    log_dispatcher.info(to_write=r.status_code)


def update_profile_geo(profile_id, latitude, longitude, port):
    """update profile geo"""
    url = f'http://localhost:{port}/api/v2/profile/' + profile_id

    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "geolocation": {
            "mode": "ALLOW",
            "fillBasedOnExternalIp": False,
            "lat": latitude,
            "lng": longitude,
            "accuracy": "100"
        },
        "mediaDevices": {
            "mode": "REAL"
        },
    }
    r = requests.post(url, json=data, headers=header)
    log_dispatcher.info(to_write=r.status_code)


def create_profile(session_name, port):
    """create profile"""
    x = {
        "name": f"{session_name}",
        "browser": "mimic",
        "os": "win",
        "enableLock": True,
        "startUrl": f"https://beboo.ru/",
        "extensions": {
            "enable": True,
            "names": ["capmonster.crx"]
        }

    }

    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    url = f"http://localhost:{port}/api/v2/profile"
    req = requests.post(url, data=json.dumps(x), headers=header)

    return json.loads(req.content).get("uuid")


def list_profiles(port):
    """list all profiles"""
    url = f"http://localhost:{port}/api/v2/profile"
    resp = requests.get(url)
    resp_json = json.loads(resp.content)
    return resp_json


def get_profile_name(session, port):
    """get profile name"""
    data = list_profiles(port)
    df = pd.DataFrame(data)
    locked = df.loc[df['uuid'] == session]
    session_name = locked["name"]
    session_name = session_name.to_list()
    session_name = session_name[0]
    pattern = r'[' + string.punctuation + ']'
    session_name = re.sub(pattern, "", session_name)
    return session_name


def update_profile(port, profile_id, session_rename, group_id):
    url = f'http://localhost:{port}/api/v2/profile/' + profile_id
    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    x = {
        "group": group_id,
        "name": session_rename
    }
    reqs = requests.post(url, json.dumps(x), headers=header)
    log_dispatcher.info(to_write=reqs.status_code)


def stick(name_id):
    proxy_url = "@proxy.soax.com:5000"
    package_id = '76853'
    package_login = 'o9wWEwXm7NH5RG2W'
    url = 'http://checker.soax.com/api/ipinfo'

    def get_proxy_path():
        rand_ips = 'ru'
        proxy_path_url = f'package-{package_id}-country-{rand_ips}-sessionid-{name_id}-sessionlength-160'
        return proxy_path_url

    proxy_path_url = get_proxy_path()
    full_url = f"http://{proxy_path_url}:{package_login}{proxy_url}"

    if not check_proxy(full_url):

        for i in range(4):
            pattern = r'A-\d+$'

            if re.search(pattern, name_id):
                name_id = name_id[:-1] + str(int(name_id[-1]) + 1)
            else:
                name_id += 'A-1'

            get_proxy_path()
            full_url = f"http://{proxy_path_url}:{package_login}{proxy_url}"

            if check_proxy(full_url):
                break
            msg = 'Ошибка создания проски -_-'
            log_dispatcher.info(to_print=msg, to_write=msg, msg_type='error')
            time.sleep(1)

            if i == 3:
                msg = 'Не удалось создать прокси'
                log_dispatcher.info(to_print=msg, to_write=msg, msg_type='error')
                raise ValueError('Proxys is not a valid')

    requests.get(url, proxies={'http': full_url, 'https': full_url})

    return proxy_path_url


def delete(session, port):
    url = f'http://localhost.multiloginapp.com:{port}/api/v2/profile/' + session
    headers = {'accept': 'application/json'}

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print('Профиль успешно удален.')
    else:
        print('Ошибка при удалении профиля. Код ошибки:', response.status_code)
