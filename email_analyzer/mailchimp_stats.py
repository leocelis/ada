import os
import ujson

from mailchimp3 import MailChimp
from pygments import highlight, lexers, formatters

import requests

MAILCHIMP_API = os.environ.get('MAILCHIMP_API')
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID')
MAILCHIMP_CAMPAIGN_ID = os.environ.get('MAILCHIMP_CAMPAIGN_ID')
headers = requests.utils.default_headers()
client = MailChimp(mc_api=MAILCHIMP_API, timeout=30.0, request_headers=headers)

# get all reports for a given list
r = client.reports.all(get_all=True)  # True will pull all the reports
reports = r.get('reports', list())

for item in reports:
    if item.get('list_id') == MAILCHIMP_LIST_ID:
        del item['_links']
        item_json = j = ujson.dumps(item, sort_keys=True, indent=4)
        item_json_pretty = highlight(item_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        # print(item_json_pretty) # remove to print everything

        print('"{}" | {} subs | {} opens | {}% open rate'.format(
            item.get('subject_line'),
            item.get('emails_sent', 0),
            item.get('opens', {}).get('unique_opens'),
            round(item.get('opens', {}).get('open_rate', 0) * 100, 2)
        ))


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
