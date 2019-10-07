import os

import facebook
import pandas as pd
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.config import FACEBOOK_SHARES_THRESHOLD

APP_ID = os.environ.get('APP_ID')
APP_SECRET = os.environ.get('APP_SECRET')
API_VERSION = os.environ.get('API_VERSION')

graph = facebook.GraphAPI(version=API_VERSION)
token = graph.get_app_access_token(app_id=APP_ID, app_secret=APP_SECRET, offline=True)

filename = "links_extractor/links_clean.csv"
df = pd.read_csv(filename, index_col=None, encoding="ISO-8859-1")  # ignore index column

# for each link extract stats
for index, row in df.iterrows():
    link = row["link"]
    title_csv = row["title"]

    if title_csv and link:
        args = dict()
        args["access_token"] = token
        args["id"] = link
        method = "/"

        try:
            r = graph.request(method, args)
        except Exception as e:
            print("\nERROR: {}".format(str(e)))
            continue

        title = str(r.get('og_object', {}).get('title', ''))
        shares = int(r.get('share', {}).get('share_count', 0))
        shares_prettified = format(shares, "8,.0f")

        # print("Retrieving {}: {} ({})...".format(title, link, shares_prettified))
        print("\nFacebook shares ({}) {}...".format(link, shares))

        if title and shares >= FACEBOOK_SHARES_THRESHOLD:
            print("\n============================================================")
            print("\n{} ({}): {} shares on Facebook\n".format(title, link, shares_prettified))
            print("\nObject: {}".format(r))
            print("============================================================")
