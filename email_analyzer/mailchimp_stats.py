"""
mailchimp3 - https://pypi.org/project/mailchimp3/
"""
import os
import ujson

from mailchimp3 import MailChimp
from pygments import highlight, lexers, formatters

import requests

MAILCHIMP_API = os.environ.get('MAILCHIMP_API')
headers = requests.utils.default_headers()
client = MailChimp(mc_api=MAILCHIMP_API, timeout=30.0, request_headers=headers)
list_id = "c0a990c819"  # the art of the ad tech
campaign_id = "fbd62dbc6e"  # the art of the ad tech

# # get campaigns
# r = client.campaigns.all(get_all=False)
# o = ujson.dumps(r, sort_keys=True, indent=4)
# j = highlight(o, lexers.JsonLexer(), formatters.TerminalFormatter())
# print(j)

# search campaigns
# r = client.search_campaigns.get(query="ad tech", get_all=True)
# o = ujson.dumps(r, sort_keys=True, indent=4)
# j = highlight(o, lexers.JsonLexer(), formatters.TerminalFormatter())
# print(j)

# get clicks report
# r = client.reports.click_details.all(campaign_id=campaign_id, get_all=False)
# o = ujson.dumps(r, sort_keys=True, indent=4)
# j = highlight(o, lexers.JsonLexer(), formatters.TerminalFormatter())
# print(j)

# get reports for a campaign
# r = client.reports.get(campaign_id=campaign_id, get_all=True)
# o = ujson.dumps(r, sort_keys=True, indent=4)
# j = highlight(o, lexers.JsonLexer(), formatters.TerminalFormatter())
# print(j)

# get all reports
r = client.reports.all(get_all=False)
reports = r.get('reports', list())
# j = ujson.dumps(r, sort_keys=True, indent=4)
for item in reports:
    # only interested list
    if item.get('list_id') == list_id:
        del item['_links']
        item_json = j = ujson.dumps(item, sort_keys=True, indent=4)
        item_json_pretty = highlight(item_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        print(item_json_pretty)

# r = client.reports.all(get_all=True)
# o = ujson.dumps(r, sort_keys=True, indent=4)
# j = highlight(o, lexers.JsonLexer(), formatters.TerminalFormatter())
# print(j)
