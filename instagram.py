from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import selenium
from time import sleep

driver = webdriver.Chrome('drivers/chromedriver')
driver.get('https://instagram.com')
sleep(1.5)

username = driver.find_element(By.XPATH, '//input[@name="username"]')
username.send_keys('yzhaksylykov11')

password = driver.find_element(By.XPATH, '//input[@name="password"]')
password.send_keys('Instagram2020')

password.send_keys(Keys.ENTER)

sleep(3)

while True:
    try:
        press = driver.find_element(By.XPATH, '//button[text() = "Not Now"]')
        press.send_keys(Keys.RETURN)
    except:
        break

driver.get('https://instagram.com/zuck')





