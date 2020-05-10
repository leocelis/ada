import os
import sys

import requests
from flask_restful import Resource

sys.path.append(os.path.dirname(os.getcwd()))
from ada.config import log
from ada.content_analyzer.utils import get_service

# MailChimp
from mailchimp3 import MailChimp


class APIStatus(Resource):
    def get(self, service=""):
        # test MailChimp API
        if service == "mailchimp":
            try:
                MAILCHIMP_API = os.environ.get('MAILCHIMP_API')
                headers = requests.utils.default_headers()
                client = MailChimp(mc_api=MAILCHIMP_API, timeout=60.0, request_headers=headers)
                client.lists.all(get_all=True, fields="lists.id")
                return {'status': 'OK'}, 200
            except Exception as e:
                log.error(str(e))

        # test GA API
        if service == "ga":
            try:
                # Define the auth scopes to request.
                scope = 'https://www.googleapis.com/auth/analytics.readonly'
                key_file_location = 'client_secrets.json'

                # Authenticate and construct service.
                service = get_service(api_name='analytics',
                                      api_version='v3',
                                      scopes=[scope],
                                      key_file_location=key_file_location)
                service.management().accounts().list().execute()
                return {'status': 'OK'}, 200

            except Exception as e:
                log.error(str(e))

        return {'status': 'ERROR'}, 500
