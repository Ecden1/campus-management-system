from flask import Blueprint
from app.controllers.home import home

home_bp = Blueprint('home', __name__, url_prefix='/')

home_bp.route('/')(home)