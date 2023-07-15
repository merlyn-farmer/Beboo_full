import os.path
import shutil
import tempfile
import time

from selenium.webdriver.common.by import By


def spam(driver):
    i = 0
    while True:
        try:
            user_link = get_user()
            driver.get(user_link)
            error_buttons = driver.find_elements(By.ID, 'error-information-button')
            if error_buttons:
                print('Proxy error...')
                while error_buttons:
                    print('Proxy error...')
                    time.sleep(7)
                    driver.get(user_link)
                    time.sleep(3)
                    error_buttons = driver.find_elements(By.ID, 'error-information-button')

            driver.find_element(By.XPATH, "//a[contains(text(),'Написать')]").click()
            time.sleep(1)
            try:
                driver.find_element(By.XPATH, "//textarea[@id='sendmessage']").send_keys('Приветики) '
                                                                                         'Желаешь развлечься ?) '
                                                                                         'телеграмчик - @pozaracom ,'
                                                                                         ' буду ждать с подарком)')
                time.sleep(0.5)
                driver.find_element(By.XPATH, "//span[contains(text(),'Отправить')]").click()
            except:
                is_limit = driver.find_elements(By.XPATH, "//b[contains(text(),'снять ограничения')]")
                if is_limit:
                    return True
            i += 1
            print(i)
        except:
            return False


def get_user() -> str:
    filenames = ['users', 'users_msk', 'users_piter']
    filename = None
    for file in filenames:
        if os.path.isfile(file):
            filename = file
            break

    if filename is None:
        raise FileNotFoundError('Файл с пользователями не найден')

    with open(filename, "r") as file:
        first_line = file.readline().strip()

    temp_filename = tempfile.NamedTemporaryFile(delete=False).name

    with open(filename, "r") as input_file, open(temp_filename, "w") as output_file:
        next(input_file)
        for line in input_file:
            output_file.write(line)

    shutil.move(temp_filename, filename)

    return first_line
