from flask import Blueprint
from app.controllers.grade import index, add, update, delete, lock, unlock, analysis

grade_bp = Blueprint('grade', __name__, url_prefix='/grade')

grade_bp.route('/')(index)
grade_bp.route('/add', methods=['GET', 'POST'])(add)
grade_bp.route('/update/<int:id>', methods=['GET', 'POST'])(update)
grade_bp.route('/delete/<int:id>')(delete)
grade_bp.route('/lock/<int:id>')(lock)
grade_bp.route('/unlock/<int:id>')(unlock)
grade_bp.route('/analysis')(analysis)