import os
import sys

import ujson
from pygments import highlight, lexers, formatters

import requests

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils import get_domains

# ShareThis API endpoint
sharethis_endpoint = 'https://count-server.sharethis.com/v2.0/get_counts'

domains = get_domains()
for d in domains:
    try:
        print("Pulling status for {} ...\n".format(d))

        # send requests
        payload = {'url': d}
        r = requests.get(sharethis_endpoint, params=payload, timeout=(5, 30))  # conn and response time
        j = r.json()

        # print response
        print("\nSocial Share Count for {}".format(d))
        formatted_json = ujson.dumps(j, sort_keys=True, indent=4)
        colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        print(colorful_json)

    except requests.exceptions.RequestException as e:
        print(e)
