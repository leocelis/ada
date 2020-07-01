"""
Google Trends categories: https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories

Run:
> pip3 install pytrends
Update the values in parameters
> python3 content_discovery/google_trends.py
"""
from pytrends.request import TrendReq

# parameters
category = 12
geo = 'US'
timeframe = 'today 1-m'
gprop = ''  # default to web searches
kw_list = ["Marketing", "Advertising"]  # keywords

# build payload
pytrends = TrendReq(hl='en-US', tz=360)
pytrends.build_payload(kw_list, cat=category, timeframe=timeframe, geo=geo, gprop=gprop)

# get related queries
r = pytrends.related_queries()
print(r)
