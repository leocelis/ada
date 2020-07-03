import os
import sys

from flask_restful import Resource

sys.path.append(os.path.dirname(os.getcwd()))
from ada.config import log
from ada.scoring.sharing_score import get_sharing_score


class APISharingScore(Resource):
    def get(self, title=""):
        try:
            score = get_sharing_score(title)
            return {'score': score, 'status': 'OK'}, 200

        except Exception as e:
            log.error(str(e))

        return {'status': 'ERROR'}, 500
