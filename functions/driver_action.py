import time

from selenium.webdriver.common.by import By


def clicker(driver, xpath):
    element = driver.find_element(By.XPATH, xpath)
    element.click()


def sender(driver, xpath, key):
    element = driver.find_element(By.XPATH, xpath)
    element.clear()
    element.send_keys(key)


def timer(t_func, *args, **kwargs):
    for i in range(30):
        time.sleep(0.5)
        try:
            result = t_func(*args, **kwargs)
            break
        except Exception as e:
            # print(i)   #debug
            pass

    return result
