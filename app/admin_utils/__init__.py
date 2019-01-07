from flask import Blueprint

# setup admin routes that are outside of Flask-Admin
bp = Blueprint('admin_utils', __name__)

from app.admin_utils import routes
