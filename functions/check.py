import os
import time
import requests
import openpyxl

from functions.config import config_data
from functions.log_dp import log_dispatcher

version = '0.1'


def check_port_con(port):
    url = f'http://127.0.0.1:{port}/'
    try:
        requests.get(url, timeout=1)
        msg = f'Подключение к порту {port} установлено'
        log_dispatcher.info(to_write=msg)
    except:
        msg = f'Подключение к порту {port} не удалось установить'
        log_dispatcher.info(to_print=msg, to_write=msg, msg_type='error')
    time.sleep(0.5)


def check_gmail():
    workbook = openpyxl.load_workbook('res/gmail.xlsx')
    worksheet = workbook['Sheet1']
    count_email = 0
    for cell in worksheet['A2:A' + str(worksheet.max_row)]:
        for row in cell:
            if row.value:
                count_email += 1

    return count_email


def check():
    log_dispatcher.info(to_print=f"Версия программы: {version}", msg_type='error')
    log_dispatcher.info(to_print=f"Проверка состояния...")
    time.sleep(0.5)

    if os.path.exists(config_data.get_photos_dir):
        msg = 'Путь в норме'
        log_dispatcher.info(to_print=msg, to_write=msg)
    else:
        msg = 'Путь не верный'
        log_dispatcher.info(to_print=msg,
                            to_write=f'EXCEPTION!!! File path is not correct!'
                                     f'\nSet path: {config_data.get_photos_dir} \n\n\n',
                            msg_type='error')

    time.sleep(0.5)
    try:
        count_email = check_gmail()
        msg = f'Кол-во почт в программе: {count_email}'
        log_dispatcher.info(to_print=msg, to_write=msg)
    except Exception as ex:
        log_dispatcher.info(to_write=f'\n\n\n{ex}')

    time.sleep(0.5)
    try:
        filename = 'res/session_names'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                content = f.read()
                num_lines = content.count('\n')
                msg = f'Кол-во имен в session_names: {num_lines + 1}'
                log_dispatcher.info(to_print=msg, to_write=msg)
        else:
            msg = f'Файл {filename} не найден.'
            log_dispatcher.info(to_print=msg, to_write=msg, msg_type='error')



    except:
        pass
    time.sleep(0.5)

    return count_email
