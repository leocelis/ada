import os
import sys

import ujson
from mailchimp3 import MailChimp
from pygments import highlight, lexers, formatters

import requests

sys.path.append(os.path.dirname(os.getcwd()))

MAILCHIMP_API = os.environ.get('MAILCHIMP_API')
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID')
MAILCHIMP_CAMPAIGN_ID = os.environ.get('MAILCHIMP_CAMPAIGN_ID')
headers = requests.utils.default_headers()
client = MailChimp(mc_api=MAILCHIMP_API, timeout=60.0, request_headers=headers)

r = client.lists.members.all(MAILCHIMP_LIST_ID, get_all=True)
# r = client.lists.members.all(MAILCHIMP_LIST_ID, count=10) # just 10 members
items = r.get('members', list())

for item in items:
    city = item.get('merge_fields', {}).get('FCITY', 'Not specified')
    name = item.get('merge_fields', {}).get('FNAME', 'Not specified')
    rating = item.get('member_rating', 0)

    # only subscribers with city
    if item.get('status') != "unsubscribed" and city:
        print("\nName: {}"
              "\nCity: {}"
              "\nRating: {}"
              "\nStats:".format(name,
                                city,
                                rating))

        stats = item.get('stats', {})
        item_json = ujson.dumps(stats, sort_keys=True, indent=4)
        item_json_pretty = highlight(item_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        print(item_json_pretty)
