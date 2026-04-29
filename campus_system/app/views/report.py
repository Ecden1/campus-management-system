from flask import Blueprint
from app.controllers.report import index, class_report, grade_report, export_class_report, export_grade_report, export_student_grades

report_bp = Blueprint('report', __name__, url_prefix='/report')

report_bp.route('/')(index)
report_bp.route('/class')(class_report)
report_bp.route('/grade')(grade_report)
report_bp.route('/export/class/<int:class_id>')(export_class_report)
report_bp.route('/export/grade/<int:course_id>')(export_grade_report)
report_bp.route('/export/student/grades')(export_student_grades)