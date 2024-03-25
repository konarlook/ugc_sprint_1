from flask import Flask
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
app.register_blueprint(routers)
app.config["SWAGGER"] = {
    "title": "UGC service",
    "uiversion": 3,
    "specs_route": "/ugc/api/v1/openapi/",
}

swagger = Swagger(app, template=template)

if __name__ == "__main__":
    app.run(debug=True)
