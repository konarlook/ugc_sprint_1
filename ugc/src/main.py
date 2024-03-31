from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from api.v1.events import routers

SWAGGER_URL = "/ugc/api/openapi"
API_URL = "/static/api/v1/openapi.yaml"

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "UGC service",
    },
)


def create_app():
    flask_application = Flask(__name__)

    flask_application.register_blueprint(swagger_blueprint)
    flask_application.register_blueprint(routers)

    return flask_application


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
