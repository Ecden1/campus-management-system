from flask import Blueprint
from app.controllers.course import index, add, update, delete, enroll, drop, students

course_bp = Blueprint('course', __name__, url_prefix='/course')

course_bp.route('/')(index)
course_bp.route('/add', methods=['GET', 'POST'])(add)
course_bp.route('/update/<int:id>', methods=['GET', 'POST'])(update)
course_bp.route('/delete/<int:id>')(delete)
course_bp.route('/enroll/<int:course_id>')(enroll)
course_bp.route('/drop/<int:course_id>')(drop)
course_bp.route('/students/<int:id>')(students)