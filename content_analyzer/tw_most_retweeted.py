import os

import sys

# add parent dir
sys.path.append(os.path.dirname(os.getcwd()))
from ada.content_analyzer.utils import get_all_site_links, check_retweet_exists, save_link_retweets, \
    update_link_retweets
from ada.content_discovery.twitter import search_tweets

# from ada.utils.scrapy_sites_links import get_site_links_by_category

links = dict()
# get all site links
site_links = get_all_site_links(domain="chiefmartec.com")
# site_links = get_all_site_links()
# site_links = get_site_links_by_category(category='adtech')

for s in site_links:
    link = s["site_link"]
    tweets = search_tweets(query=link, retweets=True, result_type='mixed')

    if tweets:
        for t in tweets:
            if not check_retweet_exists(tweet_id=t.get('id_str')):
                save_link_retweets(query=link, t=t)
            else:
                update_link_retweets(query=link, t=t)
