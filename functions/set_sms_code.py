import time

from selenium.webdriver.common.by import By

from functions.buy_phone_num import five_sim_buy, five_sim_check
from functions.driver_action import timer, sender


def set_code(driver):
    number, num_id = five_sim_buy()
    time.sleep(1)

    driver.find_element(By.XPATH, "//input[@placeholder='Введите номер телефона']").send_keys(number)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(),'Получить код')]").click()
    time.sleep(1)

    for _ in range(4):
        time.sleep(15)
        sms_code = five_sim_check(num_id=num_id)
        if sms_code:
            timer(sender, driver, "//input[@placeholder='Код из смс']", str(sms_code))
            return False
    else:
        return True