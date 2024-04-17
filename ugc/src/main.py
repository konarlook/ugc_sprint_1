import logging
import os

import logstash
import sentry_sdk
from api.v1.events import routers
from dotenv import load_dotenv
from flask import Flask, request
from flask_swagger_ui import get_swaggerui_blueprint
from helpers.kafka_init import KafkaInit, get_kafka_init
from sentry_sdk.integrations.flask import FlaskIntegration

load_dotenv()


SWAGGER_URL = "/ugc/api/openapi"
API_URL = "/static/api/v1/openapi.yaml"

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "UGC service",
    },
)

def init_kafka(kafka_init_app: KafkaInit = get_kafka_init()):
    kafka_init_app.create_topics()

def create_app():
    flask_application = Flask(__name__)

    flask_application.register_blueprint(swagger_blueprint)
    flask_application.register_blueprint(routers)

    init_kafka()

    return flask_application

app = create_app()

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    enable_tracing=True,
    integrations=[
        FlaskIntegration(
            transaction_style="url",
        ),
    ],
)

logstash_handler = logstash.LogstashHandler('logstash', 5044, version=1)

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get('X-Request-Id')
        return True

app.logger.addFilter(RequestIdFilter())
app.logger.addHandler(logstash_handler)

@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is requred')

if __name__ == "__main__":
    app.run(debug=False)