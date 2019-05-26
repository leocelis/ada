import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.twitter import search_tweets
from ada.utils.domain_stats import get_domains, update_domain_retweets

# get all domains
domains = get_domains()

for d in domains:
    retweet_count = 0
    tblob = dict()
    domain = d["domain"]

    tweets = search_tweets(query=domain.lower(), retweets=True, result_type='mixed')
    if tweets:
        for t in tweets:
            retweet_count += int(t.get('retweet_count', 0))
            tblob.update(t)
            print("{} {} {}".format(t['id_str'], retweet_count, len(tblob)))

        if retweet_count:
            print("Updating {} ...".format(domain))
            update_domain_retweets(domain=domain, retweets=retweet_count, r=tblob)
