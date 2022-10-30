

# IF not already done, then install Snscrape by pasting: 'pip3 install
# git+https://github.com/JustAnotherArchivist/snscrape.git' in the terminal


import snscrape.modules.twitter as sntwitter
import pandas as pd
from tabulate import tabulate
import seaborn as sns
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
import re
nltk.download('stopwords')
stemmer = nltk.SnowballStemmer("english")
from nltk.corpus import stopwords
import string
stopword = set(stopwords.words('english'))


"""
##################################################################################################################################
Scrape Tweets
##################################################################################################################################
"""

# Source: https://www.freecodecamp.org/news/python-web-scraping-tutorial/


def scrape_twitter(subject):
    # Blank list to append Tweets
    tweet_list = []

    # Scrape Tweets and append to blank list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(subject).get_items()):
        tweet_list.append([tweet.user.username, tweet.date, tweet.likeCount, tweet.rawContent, tweet.url])

    # Create DataFrame of Tweets from list of Tweets
    tweet_df = pd.DataFrame(tweet_list, columns=['Username', 'Date', 'Like Count', 'Content', 'Link'])
    print(len(tweet_df), 'Tweets')
    print(tabulate(tweet_df.head(10), headers='keys', tablefmt='psql', numalign='right'))
    
    return tweet_df


# Subject to search and scrape Twitter
tweet_subject = 'Elon Musk since:2022-010-01 until:2022-011-01'  # Text subject and date range
ama_voting = 'Favorite Female Country Artist #AMAs2022 since:2022-09-01 until:2022-011-01'
pca_voting = '#TheCountryArtist at #PCAs since:2022-09-01 until:2022-011-01'

df_musk = scrape_twitter(tweet_subject)
df_ama_voting = scrape_twitter(ama_voting)
df_pca_voting = scrape_twitter(pca_voting)


"""
##################################################################################################################################
Sentiment Analysis
##################################################################################################################################
"""


def word_cloud(df):
    text = ' '.join(i for i in df['Content'])
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(stopwords=stopwords, background_color='white').generate(text)
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


def sentiment_analysis(df):
    nltk.download('vader_lexicon')
    sentiments = SentimentIntensityAnalyzer()
    df['Positive'] = [sentiments.polarity_scores(i)['pos'] for i in df['Content']]
    df['Negative'] = [sentiments.polarity_scores(i)['neg'] for i in df['Content']]
    df['Neutral'] = [sentiments.polarity_scores(i)['neu'] for i in df['Content']]
    df_subset = df[['Content', 'Positive', 'Negative', 'Neutral']]
    print(df_subset.head())
    print(tabulate(df_subset.head(10), headers='keys', tablefmt='psql', numalign='right'))
    x = sum(df_subset['Positive'])
    y = sum(df_subset['Negative'])
    z = sum(df_subset['Neutral'])

    def sentiment_score(a, b, c):
        if (a > b) and (a > c):
            print('Positive 😊 ')
        elif (b > a) and (b > c):
            print('Negative 😠 ')
        else:
            print('Neutral 🙂 ')

    sentiment_score(x, y, z)


# Validate data and check for nulls
df_musk.isna().sum()

# Descriptive Statistics
df_musk.describe()


# def clean(text):
#     text = str(text).lower()
#     text = re.sub('\[.*?\]', '', text)
#     text = re.sub('https?://\S+|www\.\S+', '', text)
#     text = re.sub('<.*?>+', '', text)
#     text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
#     text = re.sub('\n', '', text)
#     text = re.sub('\w*\d\w*', '', text)
#     text = [word for word in text.split(' ') if word not in stopword]
#     text = " ".join(text)
#     text = [stemmer.stem(word) for word in text.split(' ')]
#     text = " ".join(text)
#     return text
#
#
# tweet_df['Content'] = tweet_df['Content'].apply(clean)


ama_voting_wc = word_cloud(df_ama_voting)
pca_voting_wc = word_cloud(df_pca_voting)
elon_musk_sentiment = sentiment_analysis(df_musk)
