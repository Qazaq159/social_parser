from tools import Twitter_account, save_to_csv_twitter, get_tweet_data

user = 'Your login'
email = 'Your email'
password = 'Your password'
number_of_posts = 40
account_to_parse = 'https://twitter.com/elonmusk'

browser = Twitter_account(user, password, email, visability=1)
browser.process(account_to_parse, number_of_posts)

data = browser.ready()
save_to_csv_twitter(data)  # saving it to data_twitter.csv
