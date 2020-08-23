import os
import sys

import facebook

sys.path.append(os.path.dirname(os.getcwd()))
# from ada.content_analyzer.utils import save_link_fb_shares, check_link_exists, update_link_fb_shares, \
#    get_all_site_links
from ada.content_analyzer.utils import check_link_exists, update_link_fb_shares, \
    save_link_fb_shares, get_all_site_links

# from ada.utils.scrapy_sites_links import get_site_links_by_category

APP_ID = os.environ.get('APP_ID')
APP_SECRET = os.environ.get('APP_SECRET')
API_VERSION = os.environ.get('API_VERSION')

graph = facebook.GraphAPI(version=API_VERSION)
token = graph.get_app_access_token(app_id=APP_ID, app_secret=APP_SECRET, offline=True)

# get all site links
# site_links = get_all_site_links(domain="rd.com", keyword="jokes")
# site_links = get_all_site_links(domain="leocelis.com")
site_links = get_all_site_links()
# site_links = get_all_site_links(domain="buzzghana.com")
# site_links = get_site_links_by_category(category='adtech')

for s in site_links:
    link = s["site_link"]

    args = dict()
    args["access_token"] = token
    args["id"] = link
    args["fields"] = "engagement,og_object"
    method = "/"

    try:
        print("Pulling FB stats for {}...\n".format(link))
        r = graph.request(method, args)
    except Exception as e:
        print("\nERROR: {}".format(str(e)))
        continue

    site_link_title = str(r.get('og_object', {}).get('title', ''))
    fb_shares = int(r.get('engagement', {}).get('share_count', 0))

    if site_link_title and fb_shares >= 1:
        shares_prettified = format(fb_shares, "8,.0f")
        print("--> Saving {} ({}): {} shares on Facebook\n".format(site_link_title, link, shares_prettified))

        # if it exists update shares
        if check_link_exists(link):
            update_link_fb_shares(link, r)
        else:
            save_link_fb_shares(link, r)
