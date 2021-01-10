"""
(c) leocelis.com

1. Get all the links and titles
2. Get all the twitter shares
3. Get all the sharethis shares
4. Get all the facebook shares
5. Creates an empty dict
6. Sum all the shares by link
7. Save in report_links_shares table
"""
import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.content_analyzer.utils import get_all_sites, get_fb_shares_by_domain, get_retweets_by_domain, \
    get_sharethis_stats_by_domain, get_title_by_link, link_shares_update_or_insert
from ada.utils.utils import get_domain, clean_link
from ada.config import SUMMARY_THRESHOLD

# store links and shares
links_shares = dict()

# get all the sites
# sites = get_all_sites(category='adtech')
sites = get_all_sites()
for s in sites:
    print(".", end="", flush=True)
    d = get_domain(s['site_url'])

    # get all the links and facebook shares per link
    fbshares = get_fb_shares_by_domain(domain=d, threshold=SUMMARY_THRESHOLD, limit=0)
    for f in fbshares:
        print(".", end="", flush=True)
        l = clean_link(f['site_link'])
        if l in links_shares:
            links_shares[l] += int(f.get('fb_shares', 0))
        else:
            links_shares[l] = int(f.get('fb_shares', 0))

    # twitter retweets
    tretweets = get_retweets_by_domain(domain=d, threshold=SUMMARY_THRESHOLD, limit=0)
    for t in tretweets:
        print(".", end="", flush=True)
        l = clean_link(t['query'])
        if l in links_shares:
            links_shares[l] += t.get('retweet_count', 0)
        else:
            links_shares[l] = t.get('retweet_count', 0)

    # sharethis
    sharethis = get_sharethis_stats_by_domain(domain=d, threshold=SUMMARY_THRESHOLD, limit=0)
    for st in sharethis:
        print(".", end="", flush=True)
        l = clean_link(st['site_link'])

        # replace None with 0
        twitter = 0 if not s.get('twitter') else s.get('twitter')
        linkedin = 0 if not s.get('linkedin') else s.get('linkedin')

        if l in links_shares:

            links_shares[l] += linkedin + twitter
        else:
            links_shares[l] = linkedin + twitter

# update summary table
for key, value in links_shares.items():
    # get the title
    title = get_title_by_link(link=key)
    if title:
        link_shares_update_or_insert(key, title, value)
