from objects import Twitter_account, save_to_csv, get_tweet_data
from selenium.webdriver.common.by import By
from time import sleep
from operator import itemgetter

user = 'ferkin_kz'
email = 'zat.tyme.su@gmail.com'
password = 'Twitter2022$'


browser = Twitter_account(user, password, email)

browser.driver.get('https://twitter.com/elonmusk')
sleep(2)

data = []
tweet_ids = set()
last_pos = browser.driver.execute_script('return window.pageYOffset;')
scrolling = True

while scrolling:
    if len(data) > 100:
        scrolling = False

    page_cards = browser.driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
    for card in page_cards[-40:]:
        tweet = get_tweet_data(card)

        if tweet:
            tweet_id = ''
            for i in tweet:
                tweet_id += str(i)

            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)

    scroll_attempt = 0
    while True:
        browser.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(2)

        cur_pos = browser.driver.execute_script('return window.pageYOffset;')
        if last_pos == cur_pos:
            scroll_attempt += 1

            if scroll_attempt >= 3:
                browser.driver.execute_script('window.scrollTo(0, -document.body.scrollHeight);')
            else:
                sleep(2)
        else:
            last_pos = cur_pos
            break

data.sort(key=itemgetter(0), reverse=True)

save_to_csv(data)