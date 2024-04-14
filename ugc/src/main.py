from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from api.v1.events import routers as event_routers
from helpers.kafka_init import get_kafka_init, KafkaInit

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
    flask_application.register_blueprint(event_routers)
    # flask_application.register_blueprint(feedback_routers)

    init_kafka()

    return flask_application


app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
