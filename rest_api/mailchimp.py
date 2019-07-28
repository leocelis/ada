import os
import sys

import ujson
from flask import request
from flask_restful import Resource

sys.path.append(os.path.dirname(os.getcwd()))
from ada.config import log
from ada.email_analyzer.utils import get_top_opens, get_top_open_rate, get_members_by_country, get_engagement_by_country


class MailChimpReports(Resource):
    def get(self, report, count=10):
        rows = dict()

        # TODO: do this with more style
        try:
            if report == "emailopens":
                rows = get_top_opens(limit=count)

            if report == "openrate":
                rows = get_top_open_rate(limit=count)
        except Exception as e:
            log.error(str(e))

            return {'status': 'ERROR'}, 500

        remote_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        log.info("Request from {}".format(remote_address))
        output = ujson.loads(ujson.dumps(rows))

        return output, 200


class MailChimpMembers(Resource):
    def get(self, report):
        rows = dict()

        try:
            if report == "members_by_country":
                rows = get_members_by_country()

            if report == "engagement_by_country":
                rows = get_engagement_by_country()

        except Exception as e:
            log.error(str(e))

            return {'status': 'ERROR'}, 500

        remote_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        log.info("Request from {}".format(remote_address))
        output = ujson.loads(ujson.dumps(rows))

        return output, 200
