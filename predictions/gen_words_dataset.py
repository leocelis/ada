import os
import sys
import traceback

import pandas as pd

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.utils import get_domain
from ada.content_analyzer.utils import get_all_sites, get_fb_shares_by_domain, get_retweets_by_domain, \
    get_title_by_link, get_sharethis_stats_by_domain

from ada.predictions.utils import clean_all, words_value, word_shares_upsert

# config
share_threshold = 10  # min shares
# count_limit = 0  # max rows
category = "adtech"

# get websites by category
sites = get_all_sites(category=category)

# channels
fb_df = pd.DataFrame()
tw_df = pd.DataFrame()
st_df = pd.DataFrame()

# iterate each website
for s in sites:
    try:
        site_url = s['site_url']
        domain = get_domain(site_url)  # extract domain

        # Facebook: get link shares
        # fbshares = get_fb_shares_by_domain(domain=domain, threshold=share_threshold, limit=count_limit)
        fbshares = get_fb_shares_by_domain(domain=domain, threshold=share_threshold)
        fb_df_tmp = pd.DataFrame.from_dict(fbshares)
        fb_df = pd.concat([fb_df_tmp, fb_df])

        # Twitter: get link retweets
        # tretweets = get_retweets_by_domain(domain=domain, threshold=share_threshold, limit=count_limit)
        tretweets = get_retweets_by_domain(domain=domain, threshold=share_threshold)
        tw_df_tmp = pd.DataFrame.from_dict(tretweets)
        tw_df = pd.concat([tw_df_tmp, tw_df])

        # ShareThis: get link stats
        # stotal = get_sharethis_stats_by_domain(domain=domain, threshold=share_threshold, limit=count_limit)
        stotal = get_sharethis_stats_by_domain(domain=domain, threshold=share_threshold)
        st_df_tmp = pd.DataFrame.from_dict(stotal)
        st_df = pd.concat([st_df_tmp, st_df])
    except  Exception as e:
        print("type error: " + str(e))
        print(traceback.format_exc())

# facebook
fb_df["site_link_title"] = fb_df["site_link_title"].apply(lambda x: clean_all(x))

# twitter
tw_df["site_link_title"] = tw_df["query"].apply(lambda x: get_title_by_link(x))
tw_df["site_link_title"] = tw_df["site_link_title"].apply(lambda x: clean_all(x))

# sharethis clean up
st_df["site_link_title"] = st_df["site_link"].apply(lambda x: get_title_by_link(x))
st_df["site_link_title"] = st_df["site_link_title"].apply(lambda x: clean_all(x))

# Words value = social shares per word
wv = dict()
wv = words_value(wv, fb_df, "fb_shares")
wv = words_value(wv, tw_df, "retweet_count")
wv = words_value(wv, st_df, "total")

# save results
for k, v in wv.items():
    word_shares_upsert(k, v)
