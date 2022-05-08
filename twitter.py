from tools import Twitter_account, save_to_csv, get_tweet_data
from selenium.webdriver.common.by import By
from time import sleep
from operator import itemgetter
from selenium.webdriver.common.keys import Keys

user = 'your username'
email = 'your email'
password = 'your password'

browser = Twitter_account(user, password, email, visability=1)

browser.driver.get('https://twitter.com/elonmusk')
sleep(2)

data = []
tweet_ids = set()

body = browser.driver.find_element(By.TAG_NAME, 'body')
prev_h = browser.driver.execute_script('return window.pageYOffset')  # saves initial position of webpage

while True:
    if len(data) > 100:  # 100 is number of tweets which we needed
        break

    sleep(2)

    page_cards = browser.driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')  # takes list of tweets
    for card in page_cards[-10:]:
        tweet = get_tweet_data(card)  # getting its info

        '''
        Saving only unique tweets
        '''
        if tweet:
            tweet_id = tweet[0]

            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                tweet.pop(0)
                data.append(tweet)

    for i in range(4):
        body.send_keys(Keys.PAGE_DOWN)  # page down to take another part of tweets

    new_h = browser.driver.execute_script("return window.pageYOffset;")

    if new_h == prev_h:
        for i in range(4):
            body.send_keys(Keys.PAGE_UP)  # page up to prevent unloading of tweets on webpage
        sleep(1)

    else:
        prev_h = new_h  # if tweets loaded continue

data.sort(key=itemgetter(0), reverse=True)  # sortire tweets by datetime

save_to_csv(data)  # saving it to data_twitter.csv
