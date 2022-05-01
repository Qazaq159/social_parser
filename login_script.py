import csv
from time import sleep
from selenium.webdriver.common.keys import Keys
import selenium
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display

def write_password(driver, password_):
    sleep(1.5)
    password = driver.find_element(by=By.XPATH,
                                   value='//input[@autocomplete="current-password"]')
    password.send_keys(password_)
    password.send_keys(Keys.RETURN)


vdisplay = Display(visible=1, size=(1024, 768)) # if set visible value to 0, it will not show display
vdisplay.start()

option = selenium.webdriver.ChromeOptions().add_argument('headless')
driver = selenium.webdriver.Chrome('drivers/chromedriver', options=option)
driver.get('https://twitter.com/login')

user = 'ferkin_kz'
email = 'zat.tyme.su@gmail.com'
password = 'Twitter2022$'

sleep(2.5)
username = driver.find_element(by=By.XPATH, value='//input[@autocomplete="username"]')
username.send_keys(email)
username.send_keys(Keys.RETURN)

try:
    write_password(driver, password)
    sleep(2)

except:
    login = driver.find_element(by=By.XPATH,
                                value='//input[@autocomplete="on"]')
    login.send_keys(user)
    login.send_keys(Keys.RETURN)
    sleep(1)

    write_password(driver, password)
    sleep(2)

driver.get('https://twitter.com/elonmusk')
sleep(1.5)

posts = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')



