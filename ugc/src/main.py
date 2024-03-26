from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from api.v1.events import routers

app = Flask(__name__)

SWAGGER_URL = "/ugc/api/openapi"
API_URL = "/static/api/v1/openapi.yaml"

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "UGC service",
    },
)

app.register_blueprint(swagger_blueprint)
app.register_blueprint(routers)

if __name__ == "__main__":
    app.run(debug=True)
