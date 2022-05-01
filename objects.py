from selenium.webdriver.common.keys import Keys
import selenium
from selenium.webdriver.common.by import By
import csv
from time import sleep
from pyvirtualdisplay import Display


def save_to_csv(data):
    with open('data_twitter.csv', 'w', newline='', encoding='utf-8') as f:
        header = ['date', 'username', 'name', 'text', 'content', 'reply', 'retweet', 'like']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def get_tweet_data(post):
    head = post.find_element(By.XPATH, './/div[2]/div[2]/div[1]/div/div/div[1]/div[1]').text.split('\n')

    try:
        link = post.find_element(By.XPATH, './/div[2]/div[2]/div[2]/div[2]//a').get_attribute('href')
    except:
        link = ''

    try:
        time = post.find_element(By.XPATH, './/div[2]/div[2]/div[1]/div/div/div[1]/a/time').get_attribute(
            'datetime')
    except:
        time = ''

    bottom = post.find_element(By.XPATH, './/div[2]/div[2]/div[2]')
    text = post.find_element(By.XPATH, './/div[2]/div[2]/div[2]/div[1]').text
    nickname = head[1]
    name = head[0]
    reply = bottom.find_element(By.XPATH, './/div[@data-testid="reply"]').get_attribute('aria-label')

    try:
        retweet = bottom.find_element(By.XPATH, './/div[@data-testid="retweet"]').get_attribute('aria-label')
    except:
        retweet = bottom.find_element(By.XPATH, './/div[@data-testid="unretweet"]').get_attribute("aria-label")

    try:
        like = bottom.find_element(By.XPATH, './/div[@data-testid="unlike"]').get_attribute('aria-label')
    except:
        like = bottom.find_element(By.XPATH, './/div[@data-testid="like"]').get_attribute('aria-label')

    return (time, nickname, name, text, link, reply, retweet, like)


class Twitter_account:
    def __init__(self, nickname, password, email):
        self.email = email
        self.nickname = nickname
        self.password = password

        vdisplay = Display(visible=1, size=(1024, 768))  # if set visible value to 0, it will not show display
        vdisplay.start()

        options = selenium.webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = selenium.webdriver.Chrome('drivers/chromedriver', options=options)
        self.driver.get('https://twitter.com/login')
        self.driver.maximize_window()

        sleep(2)

        username = self.driver.find_element(by=By.XPATH, value='//input[@autocomplete="username"]')
        username.send_keys(self.email)
        username.send_keys(Keys.RETURN)

        sleep(2)

        try:
            self.write_password()
            sleep(2)
        except:
            login = self.driver.find_element(by=By.XPATH, value='//input[@autocomplete="on"]')
            login.send_keys(self.nickname)
            login.send_keys(Keys.RETURN)

            sleep(1)

            self.write_password()

            sleep(2)

    def write_password(self):
        sleep(1.5)
        password = self.driver.find_element(by=By.XPATH, value='//input[@autocomplete="current-password"]')
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
