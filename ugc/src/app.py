from flask import Flask
from flask_migrate import Migrate
from models.entity import db
from flasgger import Swagger
from api.v1.events import routers

template = {
    "swagger": "2.0",
    "info": {
        "title": "UGC service",
        "description": "Service for data analytics",
        "version": "1.0",
    },
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ugc_user:ugc_pass@localhost:5432/ugc"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(routers)
app.config["SWAGGER"] = {
    "title": "UGC service",
    "uiversion": 3,
    "specs_route": "/ugc/api/v1/openapi/",
}

swagger = Swagger(app, template=template)


if __name__ == '__main__':
    app.run(debug=True)

# cd ugc/src

# flask db init

# flask db migrate -m "Initial migration"

# flask db upgrade
