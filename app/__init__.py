from flask import Flask
from app.extensions import ma, limiter, cache
from app.models import db
from app.blueprints.customers import customers_bp
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.item_descs import item_descs_bp
from app.blueprints.serial_items import serial_items_bp
from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL  = '/api/docs'
API_URL = '/static/swagger.yaml'

swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mechanic API"
    }
)

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    #initialize extension
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)



    #register blueprints
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(item_descs_bp, url_prefix="/item-descs")
    app.register_blueprint(serial_items_bp, url_prefix="/serial-items")
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

    return app