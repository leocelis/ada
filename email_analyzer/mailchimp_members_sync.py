import os
import sys

from mailchimp3 import MailChimp

import requests

sys.path.append(os.path.dirname(os.getcwd()))
from ada.email_analyzer.utils import save_member, check_member_exists, update_member

MAILCHIMP_API = os.environ.get('MAILCHIMP_API')
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID')
MAILCHIMP_CAMPAIGN_ID = os.environ.get('MAILCHIMP_CAMPAIGN_ID')
headers = requests.utils.default_headers()
client = MailChimp(mc_api=MAILCHIMP_API, timeout=60.0, request_headers=headers)

r = client.lists.members.all(MAILCHIMP_LIST_ID, get_all=True)
items = r.get('members', list())

for item in items:
    # only subscribers
    if item.get('status') != "unsubscribed":
        email = item.get('email_address')

        if not check_member_exists(email):
            save_member(item)
        else:
            update_member(email, item)
