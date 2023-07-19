import time

from functions.check import check_port_con
from functions.scan_data import scan_photos_id, scan_name_id, parse_line, parse_gmail, group_id_list
from wbrowser.browser_api import stick, create_profile, update_profile_proxy, create_driver, update_profile_group


def new_session(session_name, proxy_host, proxy_port, proxy_type, proxy_username, proxy_password,
                port, group_ids):
    """Creating new session"""
    profile_id = create_profile(session_name=session_name, port=port)  # error with proxy
    time.sleep(2)
    update_profile_proxy(profile_id=str(profile_id), proxy_port=proxy_port, proxy_username=proxy_username,
                         proxy_host=proxy_host,
                         proxy_password=proxy_password, proxy_type=proxy_type, port=str(port))
    time.sleep(2)

    driver = create_driver(profile_id, port)
    time.sleep(1)
    update_profile_group(profile_id=str(profile_id), port=port, group_id=group_ids)

    return driver, profile_id


def start_session(group_id):
    session_name = parse_line("res/session_names")
    photos_folder = scan_photos_id(session_name)
    name_id = scan_name_id(session_name)

    if name_id[0] == 'B':
        port = 34999
    elif name_id[0] == 'A':
        port = 35000
    else:
        raise ValueError('cant configurate port')

    check_port_con(port)

    email, password, reserve = parse_gmail("res/gmail.xlsx")

    group_ids = group_id_list(group_id, port)
    print(f'name_id = {name_id}')
    proxy_path_url = stick(name_id)

    proxy_host = "proxy.soax.com"
    proxy_type = "SOCKS"
    proxy_username = proxy_path_url
    proxy_password = "o9wWEwXm7NH5RG2W"
    proxy_port = "5000"

    driver, profile_id = new_session(session_name, proxy_host, proxy_port, proxy_type, proxy_username, proxy_password,
                                     port, group_ids)
    return email, password, reserve, driver, photos_folder, session_name, group_ids, profile_id, name_id, port
