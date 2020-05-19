import os
import sys

import requests
from mailchimp3 import MailChimp

sys.path.append(os.path.dirname(os.getcwd()))

MAILCHIMP_API = os.environ.get('MAILCHIMP_API')
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID')
MAILCHIMP_CAMPAIGN_ID = os.environ.get('MAILCHIMP_CAMPAIGN_ID')
headers = requests.utils.default_headers()
client = MailChimp(mc_api=MAILCHIMP_API, timeout=60.0, request_headers=headers)

r = client.lists.members.all(MAILCHIMP_LIST_ID, get_all=True)
items = r.get('members', list())

for item in items:
    email_address = item['email_address']
    rating = item['member_rating']
    avg_open_rate = item['stats']['avg_open_rate']

    print("==========================")
    if rating <= 1 and avg_open_rate == 0:
        print("---> Zombie! <---")
    print("Email: {}".format(email_address))
    print("Rating: {}".format(rating))
    print("Avg. open rate: {}".format(avg_open_rate))
    print("==========================\n\n")
