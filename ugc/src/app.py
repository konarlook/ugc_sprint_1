from flask import Flask
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from api.v1.events import routers
from core.config import Config
from models.entity import db

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

    # конфигурация приложения
    flask_application.config.from_object(Config)

    # инициализация базы данных
    db.init_app(flask_application)

    # миграции
    Migrate(flask_application, db)

    # регистрация маршрутов
    flask_application.register_blueprint(routers)
    flask_application.register_blueprint(swagger_blueprint)

    return flask_application

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
