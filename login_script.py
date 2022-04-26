import csv
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import selenium
from selenium.webdriver.common.by import By

driver = selenium.webdriver.Chrome('drivers/chromedriver')

driver.get('https://twitter.com/login')

sleep(2.5)
username = driver.find_element(by=By.XPATH, value='//input[@autocomplete="username"]')
username.send_keys('zat.tyme.su@gmail.com')
username.send_keys(Keys.RETURN)


def write_password(driver):
    password = driver.find_element(by=By.XPATH,
                                   value='//input[@autocomplete="current-password"]')
    password.send_keys('Twitter2022$')
    password.send_keys(Keys.RETURN)


sleep(0.5)
try:
    write_password(driver)
except:
    login = driver.find_element(by=By.XPATH,
                                value='//input[@autocomplete="on"]')
    login.send_keys('ferkin_kz')
    login.send_keys(Keys.RETURN)

    sleep(1)

    write_password(driver)
