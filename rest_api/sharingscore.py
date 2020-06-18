import os
import sys

from flask_restful import Resource

sys.path.append(os.path.dirname(os.getcwd()))
from ada.config import log


class APISharingScore(Resource):
    def get(self, title=""):
        try:
            return {'response': title, 'status': 'OK'}, 200

        except Exception as e:
            log.error(str(e))

        return {'status': 'ERROR'}, 500
