import os
import sys
import traceback

import pandas as pd

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.utils import get_domain
from ada.content_analyzer.utils import get_all_sites, get_shares_by_domain

from ada.predictions.utils import clean_text, words_shares, word_shares_upsert, words_weight, word_weight_upsert

# config
share_threshold = 0  # min shares
# category = "adtech"

# get websites by category
# sites = get_all_sites(category=category)
sites = get_all_sites()

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
df["link_title"] = df["link_title"].apply(lambda x: clean_text(x))

# calculate weight by word
ww = words_weight(df)

# save results
for k, v in ww.items():
    # if the word is more than 2 characters
    if len(k) >= 2:
        word_weight_upsert(k, v)

# calculate shares by word
wv = words_shares(df)

# save results
for k, v in wv.items():
    # if the word is more than 2 characters
    if len(k) >= 2:
        word_shares_upsert(k, v)
