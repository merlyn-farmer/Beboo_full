import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

russian_female_names_ru = ['Александра', 'Алена', 'Алина', 'Алиса', 'Алла', 'Анастасия', 'Ангелина', 'Анна', 'Арина',
                           'Валентина', 'Валерия', 'Варвара', 'Вера', 'Вероника', 'Виктория', 'Галина', 'Дарья', 'Ева',
                           'Евгения', 'Екатерина', 'Елена', 'Елизавета', 'Жанна', 'Злата', 'Инна', 'Ирина', 'Карина',
                           'Кира', 'Кристина', 'Ксения', 'Лариса', 'Лидия', 'Любовь', 'Людмила', 'Маргарита', 'Марина',
                           'Мария', 'Мила', 'Милана', 'Милена', 'Надежда', 'Наталья', 'Нина', 'Оксана', 'Олеся',
                           'Ольга', 'Полина', 'Раиса', 'Светлана', 'София', 'Тамара', 'Татьяна', 'Ульяна', 'Юлия',
                           'Яна', 'Ярослава', 'Агата', 'Агнесса', 'Алевтина', 'Алима', 'Алла', 'Альбина', 'Амалия',
                           'Анисья', 'Ариадна', 'Валентина', 'Валерия', 'Василиса', 'Вера', 'Вероника', 'Влада',
                           'Владислава', 'Галина', 'Дарина', 'Диана', 'Дина', 'Евгения', 'Екатерина', 'Елена',
                           'Елизавета', 'Жанна', 'Зарина', 'Зоя', 'Инга', 'Инесса', 'Ия', 'Камилла', 'Каролина',
                           'Кира', 'Клавдия', 'Кристина', 'Леся', 'Майя', 'Маргарита', 'Марина', 'Мирослава',
                           'Надежда', 'Наталья', 'Оксана', 'Ольга', 'Полина', 'Роза']


def login_bebroo(driver, email):
    driver.get('https://beboo.ru/')
    time.sleep(5)
    driver.find_element(By.XPATH, "(//input[@id='reg-name'])[1]").send_keys(random.choice(russian_female_names_ru))
    driver.find_element(By.XPATH, "(//a[contains(text(),'девушка')])[1]").click()
    time.sleep(1)
    day_box = driver.find_element(By.XPATH, "(//select[@id='select-day'])[1]")
    select = Select(day_box)
    select.select_by_visible_text("01")
    time.sleep(1)
    month_box = driver.find_element(By.XPATH, "(//select[@id='mon_select'])[1]")
    select = Select(month_box)
    select.select_by_visible_text("Января")
    time.sleep(2)
    year_box = driver.find_element(By.XPATH, "(//select[@id='select-year'])[1]")
    select = Select(year_box)
    select.select_by_visible_text("2003")
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[@id='reg-email']").send_keys(email)
    time.sleep(2)
    country_box = driver.find_element(By.XPATH, "//select[@id='country_select']")
    select = Select(country_box)
    select.select_by_visible_text("Россия")
    time.sleep(2)
    is_peterburg = random.choice([True, False])

    def set_peterburg():
        region_box = driver.find_element(By.XPATH, "(//select[@id='region_select'])[1]")
        select = Select(region_box)
        select.select_by_visible_text("Ленинградская область")
        time.sleep(1)
        town_box = driver.find_element(By.XPATH, "//select[@id='town_select']")
        select = Select(town_box)
        select.select_by_visible_text("Санкт-Петербург")
        time.sleep(1)

    def set_msk():
        region_box = driver.find_element(By.XPATH, "(//select[@id='region_select'])[1]")
        select = Select(region_box)
        select.select_by_visible_text("Московская область")
        time.sleep(1)
        town_box = driver.find_element(By.XPATH, "//select[@id='town_select']")
        select = Select(town_box)
        select.select_by_visible_text("Москва")
        time.sleep(1)

    if is_peterburg:
        try:
            set_peterburg()
        except:
            time.sleep(2)
            set_msk()
    else:
        try:
            set_msk()
        except:
            time.sleep(2)
            set_peterburg()

    driver.find_element(By.XPATH, "//input[@id='reg-password']").send_keys("PankiXoi228")
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[contains(text(),'Зарегистрироваться!')]").click()
    time.sleep(2)

    return is_peterburg
