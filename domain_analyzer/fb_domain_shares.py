import os
import sys

import facebook

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.domain_stats import get_domains, update_domain_fb_shares

APP_ID = os.environ.get('APP_ID')
APP_SECRET = os.environ.get('APP_SECRET')
API_VERSION = os.environ.get('API_VERSION')

graph = facebook.GraphAPI(version=API_VERSION)
token = graph.get_app_access_token(app_id=APP_ID, app_secret=APP_SECRET, offline=True)

# get all sites
domains = get_domains()

for d in domains:
    domain = d["domain"]

    args = dict()
    args["access_token"] = token
    # https?
    args["id"] = "http://{}".format(domain)
    args["fields"] = "engagement,og_object"
    method = "/"

    try:
        print("Pulling FB stats for {}...\n".format(domain))
        r = graph.request(method, args)
    except Exception as e:
        print("\nERROR: {}".format(str(e)))
        continue

    site_link_title = str(r.get('og_object', {}).get('title', ''))
    fb_shares = int(r.get('engagement', {}).get('share_count', 0))

    if fb_shares >= 1:
        shares_prettified = format(fb_shares, "8,.0f")
        print("--> Saving {} ({}): {} shares on Facebook\n".format(site_link_title, domain, shares_prettified))
        update_domain_fb_shares(domain, r)
