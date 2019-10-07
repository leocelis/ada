import os

import pandas as pd
import sys
import texttable as tt

sys.path.append(os.path.dirname(os.getcwd()))
from ada.content_analyzer.utils import get_domains

# get all domains
domains = get_domains()

# create table
tab = tt.Texttable()
headings = ['Domain', 'Value (Dollar)', 'Facebook Shares', 'Tweets', 'Retweets', 'ShareThis']
tab.header(headings)

# iterate through each domain
rows = list()
for d in domains:
    domain = d['domain']
    dollar = 0
    if d['value_dollar']:
        dollar = '${:,.2f}'.format(d['value_dollar'])
    fbshares = d['facebook_shares']
    tweets = d['twitter_tweets']
    retweets = d['twitter_retweets']
    sharethis = d['sharethis_total']

    row = [domain, dollar, fbshares, tweets, retweets, sharethis]
    rows.append(row)

# add rows to the table
tab.add_rows(rows, header=False)

# print table
s = tab.draw()
print(s)

# save csv
df = pd.DataFrame.from_dict(domains)
del df["twitter_object"]
del df["fb_object"]
del df["sharethis_object"]
df.to_csv("reports/domains_stats.csv")
