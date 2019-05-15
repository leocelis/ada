import os
import sys
import ujson

from pygments import highlight, lexers, formatters

sys.path.append(os.path.dirname(os.getcwd()))
from ada.config import SHARETHIS_THRESHOLD

import requests

sys.path.append(os.path.dirname(os.getcwd()))
from ada.content_analyzer.utils import get_all_site_links, save_link_stats

# ShareThis API endpoint
sharethis_endpoint = 'https://count-server.sharethis.com/v2.0/get_counts'

# get all site links
# site_links = get_all_site_links(domain="chiefmartec.com")
site_links = get_all_site_links()

for s in site_links:
    link = s["site_link"]

    try:
        payload = {'url': link}
        r = requests.get(sharethis_endpoint, params=payload, timeout=(5, 30))  # conn and response time
        j = r.json()

        # print response
        print(".", end="", flush=True)
        if j.get('total', 0) >= SHARETHIS_THRESHOLD:
            print("\nSocial Share Count for {}".format(link))
            formatted_json = ujson.dumps(j, sort_keys=True, indent=4)
            colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
            print(colorful_json)
            # TODO: check if stats exist
            save_link_stats(link, j)

    except requests.exceptions.RequestException as e:
        print(e)
