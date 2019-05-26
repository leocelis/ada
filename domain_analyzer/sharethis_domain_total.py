import os
import sys

import requests

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.domain_stats import get_domains, update_domain_sharethis_total

# ShareThis API endpoint
sharethis_endpoint = 'https://count-server.sharethis.com/v2.0/get_counts'

# get all domains
domains = get_domains()

for d in domains:
    domain = d["domain"]

    try:
        payload = {'url': domain.lower()}
        r = requests.get(sharethis_endpoint, params=payload, timeout=(5, 30))  # conn and response time
        j = r.json()

        if j.get('total', 0) >= 1:
            print("\nSaving ShareThis stats for {}...".format(domain))

            update_domain_sharethis_total(domain=domain, r=j)

        print(".", end="", flush=True)

    except requests.exceptions.RequestException as e:
        print(e)
