import json
import os
import re

import pandas as pd

from functions.log_dp import log_dispatcher


def scan_photos_id(session_name):
    result = re.search(r"/(.+?)/", session_name)
    if result:
        photo_id = result.group(1)
        return photo_id


def scan_name_id(session_name):
    result = re.search(r"(.+?)/", session_name)
    if result:
        name_id = result.group(1)
        return name_id


def parse_gmail(file):
    """Parse excel to get gmail account"""
    df = pd.read_excel(file)
    row = df.iloc[0]
    email, password, reserve = row

    parsed_df = df.iloc[1:]

    parsed_df.to_excel(file, index=False)
    return email, password, reserve


def parse_line(file):
    """Deprecated*, used to parse first line of text file"""
    with open(file, "r", encoding="UTF-8") as f:
        list = f.readlines()
        line = list[0].strip()

    with open(file, "w", encoding="UTF-8") as f:
        new_list = list[1:]
        content = "".join(new_list)
        f.write(content)

    return line


def group_id_list(group_id, port):
    if not os.path.exists('config_browser.txt'):
        group_port_mapping = {
            # "t_spam": {
            #     "34999": "",
            #     "35000": ""
            # },
            "merlyn": {
                "34999": "7506a15d-cca9-4ebd-be36-addf2bd53a52",
                "35000": "584811b7-246c-457a-961a-7344262a90f2"
            },
            "david": {
                "34999": "7506a15d-cca9-4ebd-be36-addf2bd53a52",
                "35000": "584811b7-246c-457a-961a-7344262a90f2"
            },
            "FA001": {
                "34999": "a9c92733-f9a5-45d3-8b9b-494541b236d9",
                "35000": "4bc1480b-6b74-464b-83be-082fc71f7bd3"
            },
            "FA002": {
                "34999": "3d4663c9-d23b-484e-8946-b052c436386d",
                "35000": "5baf834e-6f78-4f4d-a262-0cb5ee366df2"
            },
            "FA003": {
                "34999": "263503bf-473f-4bd7-aa07-4b30b90b567b",
                "35000": "c264d602-8df3-4123-962c-f8fcdbdd06eb"
            },
            "FA004": {
                "34999": "9b0e1cf3-0b73-469a-9ec8-51c2ece19721",
                "35000": "8bb79dbf-8b23-426c-bfa2-13394b043095"
            },
            "FA005": {
                "34999": "3e2d5f12-6b00-4203-abde-4d0559d1ec36",
                "35000": "0a79e12e-188f-441b-8919-52edc44a097f"
            },
            "FA006": {
                "34999": "4eb3cf01-3baf-4b1d-9597-bf68a4eb44a2",
                "35000": "2da42aed-49f7-4125-b572-a5c67fb41a97"
            },
            "FA007": {
                "34999": "19663c6d-bdd2-4437-a28d-426f524b9084",
                "35000": "5f82e9d6-3c0d-433d-90f4-68168f003cb6"
            },
            "FA008": {
                "34999": "109058f5-4bee-4351-a6bc-dac0be5db846",
                "35000": "43b12eec-791f-4c90-86ae-0deaf02d87bd"
            },
            "FA009": {
                "34999": 'c644e8b3-1388-4c1c-83e9-b62246761c0f',
                "35000": 'c644e8b3-1388-4c1c-83e9-b62246761c0f'
            }
        }

    else:
        log_dispatcher.info(to_write='use config_browser')
        with open('config_browser.txt', mode='r') as file:
            group_port_mapping = json.load(file)

    log_dispatcher.info(to_write=f'group_id in group_port_mapping: {group_id in group_port_mapping}\n'
                                 f'port in group_port_mapping[group_id]: {str(port) in group_port_mapping[group_id]}')
    if group_id in group_port_mapping and str(port) in group_port_mapping[group_id]:
        g_id = group_port_mapping[group_id][str(port)]
    else:
        g_id = "00000000-0000-0000-0000-000000000000"
        log_dispatcher.info(to_print='Выбраная группа - нераспределено')
    return g_id