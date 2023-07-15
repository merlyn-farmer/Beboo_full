import os

from selenium.webdriver.common.by import By


def parsing(driver):
    driver.get("https://beboo.ru/?realSuccess")

    def get_users():
        elements = driver.find_elements(By.CLASS_NAME, "user-link")
        page_users = ''
        for element in elements:
            href = element.get_attribute("href")
            page_users = page_users + href + '\n'
        return page_users

    first_page_users = get_users()
    page = 2
    with open('users_msk', "a+") as file:
        file.write(first_page_users)

        while True:
            driver.get(f"https://beboo.ru/?realSuccess=&page={page}")
            page += 1
            next_page_users = get_users()
            file.write(next_page_users)
