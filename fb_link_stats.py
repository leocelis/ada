"""
Set env vars:

export APP_ID=<app_id>
export APP_SECRET=<app_secret>
export API_VERSION=<api_version>
"""
import os

import facebook
import pandas as pd

APP_ID = os.environ.get('APP_ID')
APP_SECRET = os.environ.get('APP_SECRET')
API_VERSION = os.environ.get('API_VERSION')

graph = facebook.GraphAPI(version=API_VERSION)
token = graph.get_app_access_token(app_id=APP_ID, app_secret=APP_SECRET, offline=True)

# TODO: clean up links

filename = "links_extractor/links.csv"
df = pd.read_csv(filename, index_col=None, encoding="ISO-8859-1")  # ignore index column

# for each link extract stats
for index, row in df.iterrows():
    link = row["link"]

    args = dict()
    args["access_token"] = token
    args["id"] = link
    method = "/"
    r = graph.request(method, args)

    title = str(r.get('og_object', {}).get('title'))
    shares = int(r.get('share', {}).get('share_count'))
    shares_prettified = format(shares, "8,.0f")

    print("{} ({}): {} shares on Facebook\n".format(title, link, shares_prettified))

    # TODO: where to save the data?
