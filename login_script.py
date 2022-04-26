import csv
from time import sleep
from selenium.webdriver.common.keys import Keys
import selenium
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display

vdisplay = Display(visible=0, size=(1024, 768)) # if set visible value to 0, it will not show display
vdisplay.start()

option = selenium.webdriver.ChromeOptions().add_argument('headless')
driver = selenium.webdriver.Chrome('drivers/chromedriver', options=option)

driver.get('https://twitter.com/login')

sleep(2.5)
username = driver.find_element(by=By.XPATH, value='//input[@autocomplete="username"]')
username.send_keys('zat.tyme.su@gmail.com')
username.send_keys(Keys.RETURN)


def write_password(driver):
    sleep(1.5)
    password = driver.find_element(by=By.XPATH,
                                   value='//input[@autocomplete="current-password"]')
    password.send_keys('Twitter2022$')
    password.send_keys(Keys.RETURN)


try:
    write_password(driver)
    sleep(2)

    vdisplay.stop()
except:
    login = driver.find_element(by=By.XPATH,
                                value='//input[@autocomplete="on"]')
    login.send_keys('ferkin_kz')
    login.send_keys(Keys.RETURN)
    sleep(1)

    write_password(driver)
    sleep(2)

    vdisplay.stop()