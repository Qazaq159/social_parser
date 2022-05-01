from selenium.webdriver.common.keys import Keys
import selenium
from selenium.webdriver.common.by import By
import csv
from time import sleep
from pyvirtualdisplay import Display

'''
function "save_to_csv": 
    saves multi-dimensional data variable as .csv file(table)
'''


def save_to_csv(data):
    with open('data_twitter.csv', 'w', newline='', encoding='utf-8') as f:
        header = ['date', 'username', 'name', 'text', 'content', 'reply', 'retweet', 'like']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


'''
function "get_tweet_data":
    gets tweet informations:
        date - str,
        nickname - str (username of twitter account or retweeted tweet author)
        name - str (name of twitter account or retweeted tweet author )
        text - str,
        link - str (link of content, example: youtube video, etc),
        reply - str,
        retweet - str,
        like - str
'''


def get_tweet_data(post):
    head = post.find_element(By.XPATH, './/div[2]/div[2]/div[1]/div/div/div[1]/div[1]').text.split('\n')  # in root div[2] tag get text of div[1],
                                                                                                          # which contains username and name of twitter account

    try:
        link = post.find_element(By.XPATH, './/div[2]/div[2]/div[2]/div[2]//a').get_attribute('href')     # if there are content, get its link, if arent make it empty
    except:
        link = ''

    time = post.find_element(By.XPATH, './/div[2]/div[2]/div[1]/div/div/div[1]/a/time').get_attribute('datetime') # get from time tag value of datetime attribute

    bottom = post.find_element(By.XPATH, './/div[2]/div[2]/div[2]') # bottom - container which contains likes, retweets, replies as webelement
    text = post.find_element(By.XPATH, './/div[2]/div[2]/div[2]/div[1]').text # getting text of tweet
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

    tweet = (nickname, name, text, link, reply, retweet, like)
    id = ''
    for i in tweet:
        id += i

    return [id, time, nickname, name, text, link, reply, retweet, like]


class Twitter_account:
    '''
    When define Twitter_account class, it initially authorizes in twitter by given account info.
    '''
    def __init__(self, nickname, password, email, visability=0):
        self.email = email
        self.nickname = nickname
        self.password = password

        vdisplay = Display(visible=visability, size=(1024, 768))  # if set visible value to 0, it will not show display
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


        '''
        Causes of requiring typing username for safety regulations, I planned to type username, then password. If not type password.
        '''
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
        password = self.driver.find_element(by=By.XPATH, value='//input[@autocomplete="current-password"]') # finds password label by tag attributes
        password.send_keys(self.password) # types password
        password.send_keys(Keys.RETURN) # press ENTER to auhtorize
