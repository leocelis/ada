import os
import sys

import texttable as tt

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.utils import get_domain
from ada.utils.scrapy_sites import get_all_sites
from ada.utils.scrapy_sites_links import get_links_count
from ada.utils.facebook_most_shared import get_fb_shares_by_domain
from ada.utils.twitter_most_retweeted import get_retweets_by_domain
from ada.utils.sharethis_stats import get_sharethis_stats_by_domain

sites = get_all_sites(category='rent')
count_limit = 100000
share_threshold = 0

# #################################
# LINKS COUNT
# #################################

# create table
tab = tt.Texttable()
headings = ['Domain', 'Links total']
tab.header(headings)

# iterate through each domain
rows = list()
for s in sites:
    site_url = s['site_url']
    # get total links
    count = get_links_count(site_url=site_url)

    # if it has at least one link
    if count:
        row = [get_domain(site_url), count]
        rows.append(row)

# add rows to the table
tab.add_rows(rows, header=False)

# print table
s = tab.draw()
print("\n\nTotal Links by Domain\n")
print(s)

# #################################
# FACEBOOK SHARES
# #################################
for s in sites:
    tab = tt.Texttable()
    rows = list()
    site_url = s['site_url']
    domain = get_domain(site_url)
    fbshares = get_fb_shares_by_domain(domain=domain, threshold=share_threshold, limit=count_limit)

    for fbs in fbshares:
        row = [fbs['site_link'], fbs['site_link_title'], fbs['fb_shares']]
        rows.append(row)

    if rows:
        headings = ['Link', 'Title', 'Shares']
        tab.header(headings)
        tab.add_rows(rows, header=False)
        s = tab.draw()
        print("\n\n{} - Facebook Shares Report\n".format(domain))
        print(s)

# #################################
# TWITTER RETWEETS
# #################################
for s in sites:
    tab = tt.Texttable()
    rows = list()
    site_url = s['site_url']
    domain = get_domain(site_url)
    tretweets = get_retweets_by_domain(domain=domain, threshold=share_threshold, limit=count_limit)

    for trt in tretweets:
        row = [trt['query'], trt['tweet'], trt['retweet_count']]
        rows.append(row)

    if rows:
        headings = ['Link', 'Tweet', 'Retweets']
        tab.header(headings)
        tab.add_rows(rows, header=False)
        s = tab.draw()
        print("\n\n{} - Twitter Retweets Report\n".format(domain))
        print(s)

# #################################
# SHARE THIS
# #################################
for s in sites:
    tab = tt.Texttable()
    rows = list()
    site_url = s['site_url']
    domain = get_domain(site_url)
    stotal = get_sharethis_stats_by_domain(domain=domain, threshold=share_threshold, limit=count_limit)

    for st in tretweets:
        row = [st['site_link'], st['total']]
        rows.append(row)

    if rows:
        headings = ['Link', 'Total Actions']
        tab.header(headings)
        tab.add_rows(rows, header=False)
        s = tab.draw()
        print("\n\n{} - ShareThis Total Actions Report\n".format(domain))
        print(s)
