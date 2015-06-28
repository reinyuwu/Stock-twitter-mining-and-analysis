__author__ = 'Yuhang'
# !!! Important
import twitter
import csv
from collections import defaultdict

# Autentication

CONSUMER_KEY = 'x6bKN4s8f71uR0kyJKex8MEDZ'
CONSUMER_SECRET = 'Ir5kK0AjIP6tbIh6jhrq9prWIH9et01N4MflIOljAcfB5B1S8K'
OAUTH_TOKEN = '2794519237-WJp2V9JRAc1cnRNqfTZhufEKgUzUUSFal1FzwVA'
OAUTH_TOKEN_SECRET = 'NdG6ZthcATVR60l1CtzlWTSKhehu0dFe2I60MmOtLxZcC'
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

# Start from a single stock for initiation
q = 'QLYS'
count = 100
search_results = twitter_api.search.tweets(q=q, count=count)
statuses = search_results['statuses']
for _ in range(5):
    print "Length of statuses", len(statuses)
    try:
        next_results = search_results['search_metadata']['next_results']
    except KeyError, e:  # No more results when next_results doesn't exist
        break
    kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])
    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']

# Mining the timeline of the author who has mentioned this word
black_list = ['StockDawgzz','Stockenheimer1','PennyStockingt','Stockaholics','StockRocketzz']
date_created_temp = []
num_ct = 0
writer = csv.writer(open('dict2.csv', 'wb'))
for status in statuses:
        screen_name2 = status['user']['screen_name']
        no_problem = 1
        if screen_name2 in black_list:
            no_problem = 0
        if no_problem is 1:
            user_timeline = twitter_api.statuses.user_timeline(screen_name=screen_name2)
            for tweet in user_timeline:
                text_content = tweet['text']
                text_content_without_space = text_content.split()
                content_list = []
                date_dic = defaultdict(list)
                for each_stock in text_content_without_space:
                   if each_stock.startswith('$'):
                       content_list.append(each_stock)
                if content_list:
                    content_list.insert(0, screen_name2)
                    date_dic[tweet['created_at']] = content_list
                    date_created_temp.append(tweet['created_at']) # blocking the naughters by exam if >=20 stock twiters in 2 hour.
                    writer = csv.writer(open('dict2.csv', 'ab'))  # a means not overwrite, w means overwrite (not used), b means 'windows platform' otherwise it add another empty line
                    num_ct = num_ct + 1
                    if (num_ct % 100) == 0:
                        print 'The stock spider has downloaded  %d twitters.' % num_ct
                    for key, value in date_dic.items():
                        writer.writerow([key, value])  # Process the data, collect all the name after $

print 'The number of stock twitter that the spider has downloaded is %d.' % num_ct
# Validate the affectiveness of the data (Yahoo Finance).
# Modeling and machine learning algorithm.
