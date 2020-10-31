import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.predictions.utils import get_words_shares
from ada.content_discovery.twitter_content import sync_tweets

# 1. Pull the top-shared words
top_shared_words = get_words_shares(limit=10)
print("Top-shared Words")
for w in top_shared_words:
    print(w['word'])

for w in top_shared_words:
    # 2. Get the top keywords from gtrends for a given industry
    # ASSUMPTION: if the keyword is raising, it is most likely to be shared
    # TODO: get top keywords from google trend https://pypi.org/project/pytrends/#api-methods
    # TODO: run a search and get the top 5 domains
    # TODO: run a search on tweets and get the domains

    # 3. Pull tweets for the keyword
    word = w['word']
    word = "marketing podcast"
    word = "podcast advertising"
    sync_tweets(keyword=word)
    exit()
