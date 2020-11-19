import os
import sys

from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api

sys.path.append(os.path.dirname(os.getcwd()))
from ada.rest_api.mailchimp import MailChimpReports, MailChimpMembers
from ada.rest_api.words import Words
from ada.rest_api.ga import GAReportsPages
from ada.rest_api.apistatus import APIStatus
from ada.rest_api.sharingscore import APISharingScore
from ada.config import ALLOWED_URLS

app = Flask(__name__)
api = Api(app)
CORS(app,
     send_wildcard=True,
     origins=ALLOWED_URLS,
     allow_headers=["Access-Control-Allow-Credentials"])


class HealthCheck(Resource):
    def get(self):
        return {'status': 'OK'}, 200


api.add_resource(HealthCheck, '/')
# MailChimp email stats
api.add_resource(MailChimpReports, '/mailchimp/<report>/<count>')

# MailChimp member stats
api.add_resource(MailChimpMembers, '/mailchimp/members/<report>')

# Google Analytics time on page
api.add_resource(GAReportsPages, '/ga/timeonpage/<count>')

# API Status
api.add_resource(APIStatus, '/api-status/<service>')

# Sharing Score API
api.add_resource(APISharingScore, '/sharing-score/<title>')

# Words API
api.add_resource(Words, '/words/<count>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc')
