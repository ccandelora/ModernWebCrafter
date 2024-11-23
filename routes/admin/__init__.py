from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import routes
from . import product_routes
