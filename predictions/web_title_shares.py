"""
(c) leocelis.com

Steps

1. Get all the titles, from all the channels, with shares > threshold
3. Clean up: remove common words, find root words
4. Count words occurrences
5. Provide a new title
6. Add a value to each word
7. Sum all values
--
Words value:
For each word, add the share value
Truncate table, add for each word the shares total

TODO: add how efficient is the ml algo
"""
import os
import sys

import pandas as pd

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.utils import get_domain
from ada.content_analyzer.utils import get_all_sites, get_fb_shares_by_domain, get_retweets_by_domain, \
    get_sharethis_stats_by_domain, get_title_by_link

from ada.predictions.utils import clean_all

# config
share_threshold = 10  # Set shares threshold
count_limit = 10  # sample size

# get Ad Tech sites
sites = get_all_sites(category='adtech')

# channels
fb_df = pd.DataFrame()
tw_df = pd.DataFrame()
st_df = pd.DataFrame()

# get stats per link
for s in sites:
    site_url = s['site_url']
    domain = get_domain(site_url)
    print("Pulling stats for {}...".format(domain))

    # facebook
    fbshares = get_fb_shares_by_domain(domain=domain, threshold=share_threshold, limit=count_limit)
    fb_df_tmp = pd.DataFrame.from_dict(fbshares)
    fb_df = pd.concat([fb_df_tmp, fb_df])

    # twitter
    tretweets = get_retweets_by_domain(domain=domain, threshold=share_threshold, limit=count_limit)
    tw_df_tmp = pd.DataFrame.from_dict(tretweets)
    tw_df = pd.concat([tw_df_tmp, tw_df])
    break

    # sharethis
    # stotal = get_sharethis_stats_by_domain(domain=domain, threshold=share_threshold, limit=count_limit)
    # st_df_tmp = pd.DataFrame.from_dict(stotal)
    # st_df = pd.concat([st_df_tmp, st_df])

# facebook
# fb_df["site_link_title"] = fb_df["site_link_title"].apply(lambda x: clean_all(x))
# print(fb_df[['site_link_title', 'fb_shares']])

# twitter
tw_df["site_link_title"] = tw_df["query"].apply(lambda x: get_title_by_link(x))
tw_df["site_link_title"] = tw_df["site_link_title"].apply(lambda x: clean_all(x))
print(tw_df[['site_link_title', 'retweet_count']])
print()
print()
print()

# sharethis clean up
# st_df["site_link_title"] = st_df["site_link"].apply(lambda x: get_title_by_link(x))
# st_df["site_link_title"] = st_df["site_link_title"].apply(lambda x: clean_all(x))
# print(st_df[['site_link_title', 'total']])

# for each word, assign the value in a existing pandas
words_value = dict()

for index, row in tw_df.iterrows():
    for w in row["site_link_title"]:
        if w in words_value:
            words_value[w] += row["retweet_count"]
        else:
            words_value[w] = row["retweet_count"]

print(words_value)

# predict new titles based on words value
