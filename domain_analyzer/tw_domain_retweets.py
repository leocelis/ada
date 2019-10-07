import os

import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.content_discovery.twitter import search_tweets
from ada.content_analyzer.utils import get_domains, update_domain_retweets

# get all domains
domains = get_domains()

for d in domains:
    tweets_count = 0
    retweet_count = 0
    tblob = dict()
    domain = d["domain"]

    tweets = search_tweets(query=domain.lower(), retweets=True, result_type='mixed', threshold=False)
    if tweets:
        for t in tweets:
            tweets_count += 1
            retweet_count += int(t.get('retweet_count', 0))
            tblob.update(t)
            print("{}: Retweets: {} Tweets: {}".format(t['id_str'], retweet_count, tweets_count))

        if retweet_count:
            print("Updating {} ...".format(domain))
            update_domain_retweets(domain=domain, tweets=tweets_count, retweets=retweet_count, r=tblob)
