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
from ada.content_analyzer.utils import get_all_sites, get_fb_shares_by_domain
from ada.utils.utils import get_domain

# get all the sites
sites = get_all_sites(category='adtech')

for s in sites:
    d = get_domain(s['site_url'])

    # get links and Facebook shares
    fbshares = get_fb_shares_by_domain(domain=d, threshold=0)

    for f in fbshares:
        # check if it is the same link, and increase the shares
        # {'site_link': 'https://neilpatel.com/privacy/', 'site_link_title': 'Privacy Policy', 'fb_shares': 1}
        # add last_updated with NOW() in the summary table
        print(f)
        exit()

        # twitter - use the links extract from the most retweetd tweets found by keywords
        # for the same link in different tweets, sum up the retweets

        # sharethis

        # sum up all the columns, and create a new total_shares column
