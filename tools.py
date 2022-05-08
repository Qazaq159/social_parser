from selenium.webdriver.common.keys import Keys
import selenium
from selenium.webdriver.common.by import By
import csv
from time import sleep
from pyvirtualdisplay import Display
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

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
    head = post.find_element(By.XPATH, './/div[2]/div[2]/div[1]/div/div/div[1]/div[1]').text.split(
        '\n')  # in root div[2] tag get text of div[1],
    # which contains username and name of twitter account

    try:
        link = post.find_element(By.XPATH, './/div[2]/div[2]/div[2]/div[2]//a').get_attribute(
            'href')  # if there are content, get its link, if arent make it empty
    except:
        link = ''

    time = post.find_element(By.XPATH, './/div[2]/div[2]/div[1]/div/div/div[1]/a/time').get_attribute(
        'datetime')  # get from time tag value of datetime attribute

    bottom = post.find_element(By.XPATH,
                               './/div[2]/div[2]/div[2]')  # bottom - container which contains likes, retweets, replies as webelement
    text = post.find_element(By.XPATH, './/div[2]/div[2]/div[2]/div[1]').text  # getting text of tweet
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

def save_to_csv_instagram(data):
    with open('data_instagram.csv', 'w', newline='', encoding='utf-8') as f:
        header = ['link', 'post_type', 'num_of_comments', 'content_link', 'text', 'views', 'likes', 'date']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)



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
        password = self.driver.find_element(by=By.XPATH,
                                            value='//input[@autocomplete="current-password"]')  # finds password label by tag attributes
        password.send_keys(self.password)  # types password
        password.send_keys(Keys.RETURN)  # press ENTER to auhtorize


class Instagram_account:
    def __init__(self, username, password, visability=0):
        vdisplay = Display(visible=visability, size=(1024, 768))
        vdisplay.start()

        options = selenium.webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = selenium.webdriver.Chrome('drivers/chromedriver', options=options)
        self.driver.get('https://instagram.com')
        self.driver.maximize_window()

        sleep(2)

        user = self.driver.find_element(By.XPATH, '//input[@name="username"]')
        user.send_keys(username)

        passw = self.driver.find_element(By.XPATH, '//input[@name="password"]')
        passw.send_keys(password)

        passw.send_keys(Keys.ENTER)

        sleep(3)

        while True:
            try:
                press = self.driver.find_element(By.XPATH, '//button[text() = "Not Now"]')
                press.send_keys(Keys.ENTER)
            except NoSuchElementException:
                break

    def get_post_data(self, post):
        self.driver.get(post[0])
        sleep(0.5)

        try:
            content = self.driver.find_element(By.XPATH, '//div[@class="_97aPb   wKWK0"]//video').get_attribute('src')
        except:
            content = self.driver.find_element(By.XPATH, '//div[@class="_97aPb   wKWK0"]//img').get_attribute('src')

        try:
            text = self.driver.find_element(By.XPATH, '//div[@class="EtaWk "]//div[@class="MOdxS "]').text
        except:
            text = ''

        date = self.driver.find_element(By.XPATH, '//div["NnvRN"]//time').get_attribute('datetime')

        if 'video' in post[1].lower():
            row = self.driver.find_element(By.XPATH, '//section[@class="EDfFK ygqzn "]/div//span')
            row.click()

            views = row.text
            likes = self.driver.find_element(By.XPATH, '//section[@class="EDfFK ygqzn "]/div/div/div[4]').text
        else:
            try:
                row = self.driver.find_element(By.XPATH,
                                               '//section[@class="EDfFK ygqzn "]//div[contains(text(), "others")]//span').text.replace(
                    ',', '')
            except:
                row = self.driver.find_element(By.XPATH,
                                               '//section[@class="EDfFK ygqzn "]//div[contains(text(), "likes")]//span').text.replace(
                    ',', '')

            views = ''
            likes = int(row) + 1

        content = content.replace('blob:', '')

        return [content, text, views, likes, date]

    def process(self, account_link, number_of_posts):
        self.driver.get(account_link)
        sleep(2)

        self.posts_data = list()
        prev_h = self.driver.execute_script('return window.pageYOffset')
        body = self.driver.find_element(By.TAG_NAME, 'body')

        while len(self.posts_data) < number_of_posts:
            cards = self.driver.find_elements(By.XPATH, '//div[@class="Nnq7C weEfm"]//a[@tabindex="0"]')

            for card in cards[-24:]:
                link = card.get_attribute('href')

                try:
                    post_type = card.find_element(By.XPATH, './div[2]//*[name()="svg"]').get_attribute('aria-label')
                except NoSuchElementException:
                    post_type = 'Photo'

                webdriver.ActionChains(self.driver).move_to_element(card).perform()

                try:
                    comments = card.find_element(By.XPATH, '//div[@class="qn-0x"]/ul/li[2]/div//span').text
                except NoSuchElementException:
                    comments = ''

                try:
                    k = 0
                    for i in self.posts_data:
                        if link in i:
                            k += 1
                            break

                    if k == 0:
                        self.posts_data.append([link, post_type, comments])
                except:
                    if link not in self.posts_data:
                        self.posts_data.append([link, post_type, comments])

            body.send_keys(Keys.PAGE_DOWN)
            sleep(1)

            cur_h = self.driver.execute_script('return window.pageYOffset')
            if prev_h == cur_h:
                break

            prev_h = cur_h

    def ready(self):
        data = []
        for card in self.posts_data:
            try:
                data.append(card + self.get_post_data(card))
            except Exception as e:
                print(card[0], card[1], e)

        return data
