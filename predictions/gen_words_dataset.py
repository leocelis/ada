import os
import sys
import traceback

import pandas as pd

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.utils import get_domain
from ada.content_analyzer.utils import get_all_sites, get_shares_by_domain

from ada.predictions.utils import clean_all, words_value, word_shares_upsert

# config
share_threshold = 10  # min shares
category = "adtech"

# get websites by category
sites = get_all_sites(category=category)

# for each site
df = pd.DataFrame()
for s in sites:
    try:
        site_url = s['site_url']
        domain = get_domain(site_url)  # extract domain

        print("Domain: {}".format(domain))

        # get link total shares
        shares = get_shares_by_domain(domain=domain, threshold=share_threshold)
        df_tmp = pd.DataFrame.from_dict(shares)
        df = pd.concat([df_tmp, df])
    except  Exception as e:
        print("type error: " + str(e))
        print(traceback.format_exc())

# separate titles in words
df["link_title"] = df["link_title"].apply(lambda x: clean_all(x))

# calculate shares by word
wv = words_value(df, "fb_shares")

# save results
for k, v in wv.items():
    word_shares_upsert(k, v)
