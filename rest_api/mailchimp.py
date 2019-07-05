import ujson
from email_analyzer.utils import get_top_opens, get_top_open_rate
from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
CORS(app,
     origins="http://localhost:3000",
     allow_headers=["Access-Control-Allow-Credentials"])


class HealthCheck(Resource):
    def get(self):
        return {'status': 'OK'}, 200


class MailChimp(Resource):
    def get(self, report, count=10):
        if report == "emailopens":
            rows = get_top_opens(limit=count)

        if report == "openrate":
            rows = get_top_open_rate(limit=count)

        output = ujson.loads(ujson.dumps(rows))

        return output, 200


api.add_resource(HealthCheck, '/')
api.add_resource(MailChimp, '/mailchimp/<report>/<count>')

if __name__ == '__main__':
    app.run(debug=True)