import os
from urllib.parse import urlparse

import pandas as pd
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.domain_analyzer.utils import check_link_exists, save_site_link

# csv file
file_location = "./links_extractor/links.csv"
dataset = pd.read_csv(file_location, index_col=None)  # ignore index column

# iterate through each link
for index, row in dataset.iterrows():
    print(".", end="", flush=True)
    parsed_uri = urlparse(row['link'])
    site_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    site_link = row['link']
    title = row['title']

    # save link
    if not check_link_exists(site_link):
        print("Adding {}\n".format(site_link))
        save_site_link(site_url, site_link, title)
