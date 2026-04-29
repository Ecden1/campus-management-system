from flask import Blueprint
from app.controllers.student import index, add, update, delete, import_students, export_students, profile, edit_profile

student_bp = Blueprint('student', __name__, url_prefix='/student')

student_bp.route('/')(index)
student_bp.route('/add', methods=['GET', 'POST'])(add)
student_bp.route('/update/<int:id>', methods=['GET', 'POST'])(update)
student_bp.route('/delete/<int:id>')(delete)
student_bp.route('/import', methods=['GET', 'POST'])(import_students)
student_bp.route('/export')(export_students)
student_bp.route('/profile')(profile)
student_bp.route('/edit_profile', methods=['GET', 'POST'])(edit_profile)