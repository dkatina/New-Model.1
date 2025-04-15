from flask import Blueprint

item_descs_bp = Blueprint("item_descs_bp", __name__)

from . import routes