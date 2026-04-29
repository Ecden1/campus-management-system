from flask import Blueprint
from app.controllers.status import index, update_status

status_bp = Blueprint('status', __name__, url_prefix='/status')

status_bp.route('/')(index)
status_bp.route('/update/<string:student_id>', methods=['GET', 'POST'])(update_status)