"""
(c) leocelis.com

Add positive/negative sentiment to each link

Positive = >0
Negative = <0
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



# update summary table
for key, value in links_shares.items():
    # get the title
    title = get_title_by_link(link=key)
    if title:
        link_shares_update_or_insert(key, title, value)
