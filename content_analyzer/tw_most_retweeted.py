import os
import sys

# add parent dir
sys.path.append(os.path.dirname(os.getcwd()))
from ada.content_analyzer.utils import save_link_retweets, check_retweet_exists, \
    update_link_retweets, get_site_links_by_category, get_all_site_links
from ada.utils.twitter import search_tweets

links = dict()
# get all site links
# site_links = get_all_site_links(domain="leocelis.com")
# site_links = get_all_site_links()
site_links = get_site_links_by_category(category='adtech')

for s in site_links:
    link = s["site_link"]
    tweets = search_tweets(query=link, retweets=True, result_type='mixed')

    if tweets:
        for t in tweets:
            if not check_retweet_exists(tweet_id=t.get('id_str')):
                save_link_retweets(query=link, t=t)
            else:
                update_link_retweets(query=link, t=t)
