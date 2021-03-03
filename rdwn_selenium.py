from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from transliterate import translit

from secrets import DRIVER_PATH, PROFILE_PATH, RDWN_ADMIN
from xpath import *


class RedDawnSite:

    def __init__(self):

        self.rdwn = RDWN_ADMIN
        self.profile = webdriver.FirefoxProfile(PROFILE_PATH)
        self.options = Options()

        while True:
            user_input = str(input('Should I open browser? (y/n): ') or 'y')
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

        self.wait = WebDriverWait(self.driver, 10)


class AddNewEvent(RedDawnSite):

    def go_to_calendar(self):
        self.driver.get(self.rdwn)
        self.driver.find_element_by_class_name('dashicons-calendarize-it').click()
        self.driver.find_element_by_class_name('page-title-action').click()
        print('Go to calendar: done.')

    def expand_and_add_taxonomy(self, permanent_link, organization, description):
        # Постоянная ссылка
        self.wait.until(EC.presence_of_element_located((By.XPATH, XPATH_ENTIRE_EVENT_BLOCK)))
        try:
            self.driver.find_element_by_class_name('components-text-control__input').click()
        except NoSuchElementException:
            self.driver.find_element_by_xpath(XPATH_PERMANENT_LINK).click()
            self.driver.find_element_by_class_name('components-text-control__input').click()

        self.driver.find_element_by_class_name('components-text-control__input').send_keys(Keys.CONTROL, 'a')
        self.driver.find_element_by_class_name('components-text-control__input').send_keys(Keys.DELETE)

        self.driver.find_element_by_class_name('components-text-control__input').send_keys(
            translit(permanent_link, 'ru', reversed=True))
        print('Add permanent link: done.')

        # Организаторы
        try:
            self.driver.find_element_by_class_name('editor-post-taxonomies__hierarchical-terms-filter').send_keys(
                organization)
            self.driver.find_element_by_xpath(XPATH_ORGANIZATION_CHECKBOX).click()
        except NoSuchElementException:
            self.driver.find_element_by_xpath(XPATH_ORGANIZATION_LINK).click()

            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, XPATH_ORGANIZATION_CLASS)))
            self.driver.find_element_by_class_name(
                'editor-post-taxonomies__hierarchical-terms-filter').send_keys(organization)

            self.driver.find_element_by_xpath(XPATH_ORGANIZATION_CHECKBOX).click()
        print('Organizers checkbox: clicked.')

        # Изображение записи
        self.driver.find_element_by_xpath(XPATH_IMG_LINK).click()

        # Отрывок
        try:
            self.driver.find_element_by_class_name('components-textarea-control__input').send_keys(description)
        except NoSuchElementException:
            self.driver.find_element_by_xpath(XPATH_DESCRIPTION_LINK).click()
            self.driver.find_element_by_class_name('components-textarea-control__input').send_keys(description)
        print('Add description: done.')

    def add_title(self, title):
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'editor-post-title__input')))
        self.driver.find_element_by_class_name('editor-post-title__input').send_keys(f'[Игра] {title}')
        print('Add title: done.')

    def add_date(self, date_start, date_end, time_start, time_end, color):
        sleep(5)
        date_end_split = date_end.split('-')
        for date in self.driver.find_elements_by_class_name('fc-day'):
            if date.get_attribute('data-date') == date_start:
                date.click()

        self.driver.find_element_by_class_name('fc_allday').click()

        self.driver.find_element_by_class_name('fc_start_time').send_keys(time_start)

        self.driver.find_element_by_class_name('fc_end').click()
        for check_date in self.driver.find_elements_by_class_name('xdsoft_date'):
            if int(check_date.get_attribute('data-date')) == int(date_end_split[2]) and int(
                    check_date.get_attribute('data-month')) == int(date_end_split[1]) - 1 and int(
                check_date.get_attribute('data-year')) == int(date_end_split[0]):
                check_date.click()
                break
        self.driver.find_element_by_class_name('fc_end_time').send_keys(time_end)

        print('Entered data into date fields.')

        self.driver.find_element_by_xpath(XPATH_COLOR_TAB).click()

        self.driver.find_element_by_class_name('fc_color').click()
        self.driver.find_element_by_class_name('fc_color').send_keys(Keys.CONTROL, 'a')
        self.driver.find_element_by_class_name('fc_color').send_keys(Keys.DELETE)

        self.driver.find_element_by_class_name('fc_color').send_keys(color)
        print('Color selected successfully')
        self.driver.find_element_by_class_name('fc-dg-ok').click()

        print('Add date: done.')

    def save(self):
        self.driver.find_element_by_xpath(XPATH_PUBLISH_BUTTON).click()
        self.driver.find_element_by_xpath(XPATH_PUBLISH_SUBMIT_BUTTON).click()
        print('Everything saved!')

    def next_add(self):
        sleep(5)
        self.driver.back()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'page-title-action')))
        self.driver.find_element_by_class_name('page-title-action').click()

    def close_session(self):
        self.driver.quit()
        print('Session closed.')
