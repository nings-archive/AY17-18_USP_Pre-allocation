#! /usr/bin/env python3
import credentials
import time, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

QUIT_DELAY = 2 # secs to wait before quitting if login unavailable
SITE_URL = 'https://myaces.nus.edu.sg/preallocation/loginWCT.jsp'
XPATH_ID = "//td//input[@name='ID']"
XPATH_PIN = "//td//input[@name='pin']"
XPATH_CHECKBOX = "//td//input[@name='readInformation']"
XPATH_LOGIN_BTN = "//td//input[@name='Submit']"

class Browser:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def try_login(self, *, nusnet_id, password):
        self.open_url(self.url)
        self.add_id_pw_checkbox(nusnet_id=nusnet_id, password=password)
        login_btn = self.driver.find_element_by_xpath(XPATH_LOGIN_BTN)
        time_now = datetime.datetime.now().strftime('%H:%M:%S')
        if not self.is_btn_enabled(login_btn):
            print("[{}] Unavailable. Retrying in {}s.".format(time_now, QUIT_DELAY))
            time.sleep(QUIT_DELAY)
        else:
            print("[{}] LOG IN SUCESSFUL, PREALLOCATIONS ARE OPEN".format(time_now))
            login_btn.click()
            while True:
                time.sleep(1)

    def open_url(self, url):
        self.driver.get(url)

    def is_btn_enabled(self, btn):
        return btn.is_enabled()

    def add_id_pw_checkbox(self, *, nusnet_id, password):
        self.enter_id(nusnet_id)
        self.enter_pw(password)
        self.click_checkbox()

    def enter_id(self, _id):
        input_id = self.driver.find_element_by_xpath(XPATH_ID)
        input_id.send_keys(_id)

    def enter_pw(self, _pw):
        input_pw = self.driver.find_element_by_xpath(XPATH_PIN)
        input_pw.send_keys(_pw)

    def click_checkbox(self):
        input_checkbox = self.driver.find_element_by_xpath(XPATH_CHECKBOX)
        input_checkbox.click()

if __name__ == '__main__':
    browser = Browser(SITE_URL)
    while True:
        browser.try_login(nusnet_id=credentials.LOGIN, password=credentials.PASSWORD)
