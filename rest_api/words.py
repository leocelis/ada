import os
import sys
import ujson

from flask import request
from flask_restful import Resource

sys.path.append(os.path.dirname(os.getcwd()))
from ada.config import log
from ada.predictions.utils import get_words_shares


class Words(Resource):
    def get(self, count=10):
        try:
            rows = get_words_shares(limit=count)
        except Exception as e:
            log.error(str(e))

            return {'status': 'ERROR'}, 500

        remote_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        log.info("Request from {}".format(remote_address))
        output = ujson.loads(ujson.dumps(rows))

        return output, 200