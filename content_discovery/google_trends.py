"""
1) Update the values in parameters
2) Run:
$ pip3 install pytrends
$ python3 content_discovery/google_trends.py
3) Check data/ folder
"""

import csv
import datetime
import os

import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.config import DATA_FOLDER
from pytrends.request import TrendReq

# G Trends params
category = 12  # "Business & Industrial" - https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories
geo = 'US'
timeframe = 'today 1-m'  # 30 days ago, try "today 5-y"
gprop = ''  # default to web searches
keyword = "Advertising"
kw_list = [keyword]  # keywords
pytrends = TrendReq(hl='en-US', tz=360)
pytrends.build_payload(kw_list, cat=category, timeframe=timeframe, geo=geo, gprop=gprop)

# CSV file params
d = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = "gtrends_{}_{}.csv".format(keyword, d)
file_location = "{}/{}".format(DATA_FOLDER, filename)

# Write to CSV file
with open(file_location, 'w') as csvfile:
    # write headers
    fieldnames = ["datetime", "category", "geo", "timeframe", "rising_keywords", "rising_related_topics", "suggestions",
                  "interest_state", "value"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # rising keywords
    print("\n\n=================================")
    print("Related queries - Rising keywords")
    print("=================================")
    r = pytrends.related_queries()
    # top = r[keyword]['top']
    rising = r[keyword].get('rising', None)
    print(rising)

    for index, row in rising.iterrows():
        csv_row = [d, category, geo, timeframe, row['query'], "", "", "", row['value']]

        row = {
            "datetime": d,
            "category": category,
            "geo": geo,
            "timeframe": timeframe,
            "rising_keywords": row['query'],
            "rising_related_topics": "",
            "suggestions": "",
            "interest_state": "",
            "value": row['value']
        }

        writer.writerow(row)

exit()

print("\n\n=================================")
print("Related topics:")
print("=================================")
r = pytrends.related_topics()
rising = r[keyword]['rising']
# print(type(r))
print(rising)

print("\n\n=================================")
print("Suggestions:")
print("=================================")
r = pytrends.suggestions(keyword)

for i in r:
    print(i.get('title', None))

print("\n\n=================================")
print("Geo:")
print("=================================")
r = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
d = r.to_dict().get(keyword)

if d:
    for k, v in d.items():
        print("{}: {}".format(k, v))
