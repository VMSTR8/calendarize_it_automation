from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from secrets import DRIVER_PATH, PROFILE_PATH, LOGIN, PASSWORD, RDWN_ADMIN


class RedDawnSite:

    def __init__(self):

        self.rdwn = RDWN_ADMIN
        self.login = LOGIN
        self.password = PASSWORD
        self.profile = webdriver.FirefoxProfile(PROFILE_PATH)
        self.options = Options()

        while True:
            user_input = str(input('Should I open browser? (y/n): '))
            if user_input.lower() not in ('y', 'n'):
                print(f'{user_input} — incorrect input. You should type "y for YES or "n" for NO')
            elif user_input.lower() == 'y':
                self.driver = webdriver.Firefox(firefox_profile=self.profile, executable_path=DRIVER_PATH)
                break
            else:
                self.options.headless = True
                self.driver = webdriver.Firefox(
                    options=self.options, firefox_profile=self.profile, executable_path=DRIVER_PATH)
                break


class AddNewEvent(RedDawnSite):

    def go_to_calendar(self):
        self.driver.get(self.rdwn)
        self.driver.find_element_by_class_name('dashicons-calendarize-it').click()
        self.driver.find_element_by_class_name('page-title-action').click()

    def expand_and_add_taxonomy(self, organization):
        sleep(5)
        # Постоянная ссылка
        self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]/div/div/div['
                                          '1]/div/div[1]/div[2]/div[2]/div/div[3]/div[3]/h2/button').click()

        # Организаторы
        self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]/div/div/div['
                                          '1]/div/div[1]/div[2]/div[2]/div/div[3]/div[4]/h2/button').click()


        # Изображение записи
        self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]/div/div/div['
                                          '1]/div/div[1]/div[2]/div[2]/div/div[3]/div[6]/h2/button').click()

        # Отрывок
        self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]/div/div/div['
                                          '1]/div/div[1]/div[2]/div[2]/div/div[3]/div[7]/h2/button').click()

    def add_title(self, title):
        sleep(5)
        self.driver.find_element_by_class_name('editor-post-title__input').send_keys(title)

    def close_session(self):
        self.driver.quit()
