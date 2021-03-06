"""
Extract links from tweets
"""
import os
import sys
from urllib.parse import urlparse

import requests
from urlextract import URLExtract

sys.path.append(os.path.dirname(os.getcwd()))
from ada.content_analyzer.utils import get_top_tweets

tweets = get_top_tweets(retweet_threshold=10, limit=1000)
extractor = URLExtract()

for t in tweets:
    # extract links
    urls = extractor.find_urls(t['tweet'])

    # if there are links
    if urls:
        # take first only
        link = urls[0]

        # unwrap the link (redirect)
        unwrapped_link = requests.get(link).url

        # check if it is a retweet
        if 'twitter.com' not in unwrapped_link:
            # extract domain
            parsed_uri = urlparse(unwrapped_link)
            domain = parsed_uri.netloc

            print("Domain: {} - Link: {} - Retweets: {}".format(domain, unwrapped_link, t['retweet_count']))
