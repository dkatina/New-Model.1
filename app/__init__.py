from flask import Flask
from app.extensions import ma, limiter, cache
from app.models import db
from app.blueprints.customers import customers_bp
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp

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

    return app