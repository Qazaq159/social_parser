from tools import Instagram_account, save_to_csv_instagram

username = 'yzhaksylykov11'
password = ''
number_of_posts = 30
account_to_parse = 'https://www.instagram.com/zuck/'

browser = Instagram_account(username, password, visability=1)
browser.process(account_link=account_to_parse, number_of_posts=number_of_posts)

data = browser.ready()
save_to_csv_instagram(data) # saving it to data_instagram.csv
