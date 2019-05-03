import os
import sys

import facebook

sys.path.append(os.path.dirname(os.getcwd()))
from ada.content_analyzer.utils import get_all_site_links, save_link_fb_shares

APP_ID = os.environ.get('APP_ID')
APP_SECRET = os.environ.get('APP_SECRET')
API_VERSION = os.environ.get('API_VERSION')

graph = facebook.GraphAPI(version=API_VERSION)
token = graph.get_app_access_token(app_id=APP_ID, app_secret=APP_SECRET, offline=True)

# get all site links
site_links = get_all_site_links()

for s in site_links:
    link = s["site_link"]

    args = dict()
    args["access_token"] = token
    args["id"] = link
    args["fields"] = "engagement"
    method = "/"

    try:
        print("Pulling FB stats for {}...\n".format(link))
        r = graph.request(method, args)
    except Exception as e:
        print("\nERROR: {}".format(str(e)))
        continue

    title = str(r.get('og_object', {}).get('title', ''))
    shares = int(r.get('share', {}).get('share_count', 0))

    print(r)

    if title and shares >= 1:
        shares_prettified = format(shares, "8,.0f")
        print("\n--> Saving {} ({}): {} shares on Facebook\n".format(title, link, shares_prettified))

        save_link_fb_shares(link, r)
