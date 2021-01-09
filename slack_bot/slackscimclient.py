"""
Slack SCIM Client

Documentation: https://api.slack.com/scim

Prerequisites:
- Slack Plus plan or Slack Enterprise Grid
- API token created with Test Token Generator: https://api.slack.com/custom-integrations/legacy-tokens

"""
import json

import requests


class SlackSCIMClient(object):
    def __init__(self,
                 token,
                 version="1",
                 conn_timeout=2,
                 req_timeout=10,
                 page_results=25):
        self._token = token
        self._version = version
        self._conn_timeout = conn_timeout
        self._req_timeout = req_timeout
        self._timeout = (self._conn_timeout, self._req_timeout)
        self._url = "https://api.slack.com/scim/v{}/".format(self._version)
        self._page_results = page_results

    def find_user(self, name=None):
        name = str(name).lower()
        users_found = list()
        users_list = self.get_users()

        for user in users_list:
            if 'nickName' in user:
                if name in user['nickName']:
                    users_found.append(user)

        return users_found

    def get_users(self):
        """
        Users list

        :return:
        """
        method = "Users"
        return self.request(method=method, verb="GET")

    def request(self, method, verb, params=None):
        url = self._url + method
        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer {}'.format(self._token)}
        params = params or dict()

        try:
            if verb == "GET":
                params['startIndex'] = 1
                params['count'] = self._page_results
                results = list()
                done = False

                while not done:
                    # connection and request timeouts
                    r = requests.get(url,
                                     timeout=self._timeout,
                                     headers=headers,
                                     params=params)

                    response = json.loads(r.text)
                    resources = response['Resources']

                    if len(resources) > 0:
                        for resource in resources:
                            results.append(resource)

                        params['startIndex'] += response['itemsPerPage']
                    else:
                        done = True

                return results

        except requests.exceptions.RequestException as e:
            return e
