

# IF not already done, then install Snscrape by pasting: 'pip3 install
# git+https://github.com/JustAnotherArchivist/snscrape.git' in the terminal


import snscrape.modules.twitter as sntwitter
import pandas as pd
from tabulate import tabulate



"""
##################################################################################################################################
Scrape Tweets
##################################################################################################################################
"""


# Subject to search and scrape Twitter
tweet_subject = 'Carrie Underwood'

# Blank list to append Tweets
tweet_list = []
len(tweet_list)

# Scrape Tweets and append to blank list
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(tweet_subject).get_items()):
    if i > 100:
        break
    tweet_list.append([tweet.user, tweet.user.username, tweet.date, tweet.sourceLabel, tweet.rawContent, tweet.place])


# Create DataFrame of Tweets from list of Tweets
tweet_df = pd.DataFrame(tweet_list, columns=['User', 'Username', 'Date', 'Source Label', 'Content', 'Place'])
len(tweet_df)
print(tweet_df.columns)
print(tabulate(tweet_df.head(10), headers='firstrow', tablefmt='psql', numalign='right'))



"""
##################################################################################################################################
Sentiment Analysis
##################################################################################################################################
"""

# Validate data and check for nulls


