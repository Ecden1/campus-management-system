from flask import Blueprint
from app.controllers.teacher import index, add, update, delete

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')

teacher_bp.route('/', methods=['GET'])(index)
teacher_bp.route('/add', methods=['GET', 'POST'])(add)
teacher_bp.route('/update/<int:id>', methods=['GET', 'POST'])(update)
teacher_bp.route('/delete/<int:id>', methods=['GET'])(delete)
