import os
import sys

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.scrapy_sites_links import get_all_site_links

links = get_all_site_links(domain="adweek.com", limit=1000)

# Initial dataset
for l in links:
    print(l['site_link'])

df = pd.DataFrame(links)

# # Remove empty values
df['site_link'].replace('', np.nan, inplace=True)
df.dropna(subset=['site_link'], inplace=True)

# # Drop duplicates, keep the first
df_no_dupes = df.drop_duplicates(subset="site_link", keep='first')


# Irrelevant observations
def is_irrelevant(link):
    if len(link.split("-")) < 5:
        return True
    return False


df_no_dupes['is_irrelevant'] = df['site_link'].apply(is_irrelevant)

# remove irrelevant rows
df_no_irrelevant = df_no_dupes[df_no_dupes.is_irrelevant == False]


# Data normalization
def extract_words(link):
    # remove trailing /
    if link.endswith('/'):
        link = link[:-1]

    # extract words
    c = link.split('/')
    w = c[len(c) - 1]
    ws = w.replace('-', ' ')

    return ws


# remove irrelevant rows
df_no_irrelevant['words'] = df_no_irrelevant['site_link'].apply(extract_words)

# Iterate DataFrame
for index, row in df_no_irrelevant.iterrows():
    print(row['words'])
