import ujson
from email_analyzer.utils import get_top_opens, get_top_open_rate
from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
CORS(app,
     origins=["http://localhost:3000", "https://dashboard.leocelis.com"],
     allow_headers=["Access-Control-Allow-Credentials"])


class HealthCheck(Resource):
    def get(self):
        return {'status': 'OK'}, 200


class MailChimp(Resource):
    def get(self, report, count=10):
        # TODO: do this with more style
        try:
            if report == "emailopens":
                rows = get_top_opens(limit=count)

            if report == "openrate":
                rows = get_top_open_rate(limit=count)
        except Exception as e:
            return {'error': str(e)}, 500

        output = ujson.loads(ujson.dumps(rows))

        return output, 200


api.add_resource(HealthCheck, '/')
api.add_resource(MailChimp, '/mailchimp/<report>/<count>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc')
