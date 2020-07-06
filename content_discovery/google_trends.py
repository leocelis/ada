"""
Google Trends categories: https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories

Run:
> pip3 install pytrends
Update the values in parameters
$ python3 content_discovery/google_trends.py
"""
from pytrends.request import TrendReq

# parameters
category = 25  # "Advertising & Marketing"
geo = 'US'
timeframe = 'today 1-m'  # 30 days ago, try "today 5-y"
gprop = ''  # default to web searches
keyword = "Advertising"
kw_list = ["Advertising"]  # keywords

# build payload
pytrends = TrendReq(hl='en-US', tz=360)
pytrends.build_payload(kw_list, cat=category, timeframe=timeframe, geo=geo, gprop=gprop)

# get related queries
print("\n\n=================================")
print("Related queries:")
print("=================================")
r = pytrends.related_queries()
print(type(r))
print(r)
print("\n\n=================================")
print("Related topics:")
print("=================================")
r = pytrends.related_topics()
print(type(r))
print(r)
print("\n\n=================================")
print("Suggestions:")
print("=================================")
r = pytrends.suggestions(keyword)
print(type(r))
print(r)
