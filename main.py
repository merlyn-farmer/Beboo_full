import time
from datetime import timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from functions.check import check_gmail, check
from functions.config import config_data
from functions.log_dp import log_dispatcher
from functions.login_beboo import login_bebroo
from functions.model_profile import model_profile
from functions.set_sms_code import set_code
from functions.start_session import start_session
from pars_functions.pars import parsing
from spam_functions.spam import spam
from wbrowser.browser_api import update_profile_group, update_profile, delete


class BebrooReg:
    def __init__(self):
        self.is_peterburg = None
        self.port = None
        self.name_id = None
        self.profile_id = None
        self.group_ids = None
        self.session_name = None
        self.photos_folder = None
        self.reserve = None
        self.driver = None
        self.password = None
        self.email = None

        self.log_dispatcher = log_dispatcher
        self.log_dispatcher.info(to_write='########################### NEW SESSION ###########################')
        self.PHOTOS_DIR = config_data.get_photos_dir
        self.CITY = config_data.get_city
        self.GROUP_ID = config_data.get_group_id
        self.gmail_check = check_gmail()
        self.count_email = check()
        self.session_count = self.count_email

    def run_start_session(self):
        self.email, self.password, self.reserve, self.driver, self.photos_folder, self.session_name, self.group_ids, \
            self.profile_id, self.name_id, self.port = start_session(self.GROUP_ID)
        time.sleep(1)

    def run_login(self):
        self.is_peterburg = login_bebroo(driver=self.driver, email=self.email)
        time.sleep(1)

    def run_set_code(self):
        result_set = set_code(self.driver)  # if sms is set, returns False
        if result_set:  # in other words, if sms code not set
            result_set = set_code(self.driver)

        if result_set:
            raise Exception('SMS_no_coming')

        time.sleep(5)
        try:
            self.driver.find_element(By.XPATH, "//div[@id='popupBody']//a[contains(text(),'Продолжить')]").click()
        except Exception as ex:
            print(ex)
        time.sleep(1)
        age_box = self.driver.find_element(By.XPATH, "(//select[@id='inp_user_searcher_age'])[1]")
        select = Select(age_box)
        select.select_by_visible_text("35")
        time.sleep(1)
        self.driver.find_element(By.XPATH, "(//button[@type='submit'][contains(text(),'Найти')])[1]").click()
        time.sleep(1)

    def run_model_profile(self):
        model_profile(self.driver, self.photos_folder)
        time.sleep(1)

    def finalize_session(self):
        time.sleep(1)
        group_id = '904ffe25-f5d8-44f5-a922-02d89b42ddf0' if str(self.port) == '34999' \
            else '26707876-8d8f-4310-821b-bcfcdd287e84'
        update_profile(profile_id=self.profile_id, group_id=group_id, port=self.port,
                       session_rename=self.session_name + ' REGISTER')

        self.driver.quit()

    def __call__(self, *args, **kwargs):
        try:
            self.run_start_session()
            self.run_login()
            self.run_set_code()
            self.run_model_profile()
            self.finalize_session()
        except Exception as ex:
            print(f'critical exception: {ex}')


class BebrooPars(BebrooReg):
    def __init__(self):
        super().__init__()

    def start_parsing(self):
        parsing(self.driver)

    def __call__(self, *args, **kwargs):
        self.run_start_session()
        self.log_dispatcher.info(to_print='Начинаю регистрацию')
        self.run_login()
        self.log_dispatcher.info(to_print='Устанавливаю смс-код')
        self.run_set_code()
        self.log_dispatcher.info(to_print='Начинаю парсинг')
        self.start_parsing()


class BebrooSpam(BebrooReg):
    def __init__(self):
        super().__init__()

    def update_state(self):
        end_time = time.time()
        execution_time = end_time - start_time
        formatted_time = str(timedelta(seconds=execution_time))
        formatted_time_without_ms = formatted_time.split(".")[0]
        print("Время выполнения: ", formatted_time_without_ms)

        # Обновление состояния объекта

        self.driver.quit()
        time.sleep(12)
        delete(self.profile_id, self.port)  # Удаляем сессию

        self.__init__()

    def run_spam(self):
        res = spam(self.driver)
        if res:
            self.driver.quit()
        else:
            return

    def __call__(self, *args, **kwargs):
        while True:
            try:
                self.run_start_session()
                self.log_dispatcher.info(to_print='Начинаю регистрацию')
                self.run_login()
                self.log_dispatcher.info(to_print='Устанавливаю смс-код')
                self.run_set_code()
                self.log_dispatcher.info(to_print='Устанавливаю фото')
                self.run_model_profile()
                self.log_dispatcher.info(to_print='Начинаю спам')
                self.run_spam()
                self.update_state()
            except Exception as ex:
                self.update_state()


def run_process():
    global session
    global start_time

    start_time = time.time()
    try:
        if command == 'r':
            session = BebrooReg()
            for _ in range(session.count_email):
                session()

        elif command == 'p':
            session = BebrooPars()
            session()

        elif command == 's':
            session = BebrooSpam()
            session()
        else:
            input('Я не местный, доступные комманды: r, p, s.')
    except Exception as ex:
        log_dispatcher.info(to_print=ex, to_write=ex, msg_type='error')
        time.sleep(15)


if __name__ == '__main__':
    command = input('Введи нужный тебе режим работы.\n'
                    'Доступны: r - регистрация, p - парсинг профилей, s - спам в полученные профили\n')
    while True:
        run_process()
