from flask import Blueprint

serial_items_bp = Blueprint("serial_items_bp", __name__)

from . import routes