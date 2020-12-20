import os
import sys
from urllib.parse import urlparse

import pandas as pd

sys.path.append(os.path.dirname(os.getcwd()))
from ada.domain_analyzer.utils import check_link_exists, save_site_link
from ada.utils.utils import is_content_valid, get_allowed_domains

# allowed domains
a_d = get_allowed_domains()

# csv file
file_location = "./links_extractor/adtech.csv"
dataset = pd.read_csv(file_location, index_col=None)  # ignore index column

# iterate through each link
for index, row in dataset.iterrows():
    print(".", end="", flush=True)
    parsed_uri = urlparse(row['link'])
    site_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    site_link = row['link']
    # print("Site link: {}".format(site_link))
    title = row['title']

    # allowed domain
    allowed_link = False
    for d in a_d:
        # print("Domain: {}".format(d))
        if d in site_link:
            allowed_link = True
            break

    # save link
    if allowed_link and is_content_valid(site_link, title) and not check_link_exists(site_link):
        print("Adding {}\n".format(site_link))
        save_site_link(site_url, site_link, title)
