import asyncio

from api.v1.events import routers as event_routers
from api.v1.feedback import router as feedback_routers
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from helpers.kafka_init import KafkaInit, get_kafka_init
from helpers.mongo_init import MongoDBInit, get_mongodb_init

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


async def init_mongodb(mongodb_init_app: MongoDBInit = get_mongodb_init()):
    await mongodb_init_app.create_collections()


def create_app():
    flask_application = Flask(__name__)

    asyncio.run(init_mongodb())

    flask_application.register_blueprint(swagger_blueprint)
    flask_application.register_blueprint(event_routers)
    flask_application.register_blueprint(feedback_routers)

    init_kafka()

    return flask_application


app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
