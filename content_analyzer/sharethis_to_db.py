import os
import sys

import ujson
from pygments import highlight, lexers, formatters

sys.path.append(os.path.dirname(os.getcwd()))
from ada.config import SHARETHIS_THRESHOLD

import requests

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.scrapy_sites_links import get_all_site_links
from ada.utils.sharethis_stats import check_link_stats, update_link_stats, save_link_stats
from ada.utils.scrapy_sites_links import get_site_links_by_category

# ShareThis API endpoint
sharethis_endpoint = 'https://count-server.sharethis.com/v2.0/get_counts'

# get all site links
# site_links = get_all_site_links(domain="leocelis.com")
# site_links = get_all_site_links()
site_links = get_site_links_by_category(category='fun')

for s in site_links:
    link = s["site_link"]

    try:
        payload = {'url': link}
        r = requests.get(sharethis_endpoint, params=payload, timeout=(5, 30))  # conn and response time
        j = r.json()

        if j.get('total', 0) >= SHARETHIS_THRESHOLD:
            print("\nSocial Share Count for {}".format(link))
            formatted_json = ujson.dumps(j, sort_keys=True, indent=4)
            colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
            print(colorful_json)

            # check for saved stats
            if check_link_stats(site_link=link):
                update_link_stats(link=link, t=j)
            else:
                save_link_stats(link, j)

        print(".", end="", flush=True)

    except requests.exceptions.RequestException as e:
        print(e)
