import os
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import UselessFileDetector

from functions.driver_action import timer


def get_photos_path(photos_dir):
    folder_path = photos_dir
    # Проверяем, существует ли папка
    if not os.path.exists(folder_path):
        raise Exception(f"Folder not found ")
    # Получаем список файлов из нужной папки с расширением .jpg
    jpg_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.jpg')]
    # Если список пустой, значит не было найдено файлов
    if not jpg_files:
        return None
    return jpg_files


def fold_names(photos_dir, photos_folder):
    # validator = 'One' if photos_folder[1] == '-' else 'Two'
    # log_dispatcher.info(to_write=f'validator: {validator}')

    first_pattern = r'^[A-Za-z]-[A-Za-z]+$'
    second_pattern = r'^[A-Za-z][0-9]+$'
    subfolder = None

    def filter_two_letter(item):
        if 'MV-Instagram MAN' in item:
            return False
        else:
            return True

    subfolders = []
    for item in os.listdir(photos_dir):
        item_path = os.path.join(photos_dir, item)
        prefix = ""
        for char in photos_folder:
            if char.isdigit():
                break
            prefix += char
        if os.path.isdir(item_path) and item.startswith(prefix):
            subfolders.append(item)

    # log_dispatcher.info(to_write=f'subfolders with out filters: {str(subfolders)}')

    subfolders = [item for item in subfolders if filter_two_letter(item)]

    if len(subfolders) == 1:
        return subfolders[0]
    elif len(subfolders) == 2:
        for i in subfolders:
            if re.match(first_pattern, i) and re.match(second_pattern, photos_folder):
                return i

    for item in subfolders:
        # log_dispatcher.info(to_write=item)

        if photos_folder == item.split()[0]:
            subfolder = item
            break
    return subfolder


def photos_fold(driver, photos_dir, photos_folder):
    time.sleep(1)
    driver.file_detector = UselessFileDetector()
    base_fold = fold_names(photos_dir, photos_folder)
    full_folder = fold_names(photos_dir + "\\" + base_fold, photos_folder)

    for true_photo_fold in full_folder:
        if true_photo_fold.startswith(photos_folder):
            print('break')
            break

    photos_path = get_photos_path(photos_dir + "\\" + base_fold + '\\' + full_folder)
    return photos_path


def model_profile(driver, photos_folder):
    photos_dir = 'G:\\.shortcut-targets-by-id\\1iputwP1o-lZbnCzYTKlxuWiyf8XK13me\\Dating\\Photo base'
    driver.file_detector = UselessFileDetector()
    time.sleep(3)
    all_photos = photos_fold(driver, photos_dir, photos_folder)

    for i in all_photos:
        driver.get('https://beboo.ru/profile/photo')
        time.sleep(1)

        timer(driver.find_element, By.XPATH, "//input[@title='Выберите файлы для загрузки']").send_keys(i)

        time.sleep(5)
        timer(driver.find_element, By.XPATH, "//span[contains(text(),'Готово')]").click()
        time.sleep(2)