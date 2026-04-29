from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config.config import config

# 项目所用依赖包
app = Flask(__name__)
app.config.from_object(config['default'])

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

from app.models import User, Student, Class, Course, Grade, StudentStatus, OperationLog, Teacher

from app.views.home import home_bp
from app.views.auth import auth_bp
from app.views.student import student_bp
from app.views.class_ import class_bp
from app.views.course import course_bp
from app.views.grade import grade_bp
from app.views.status import status_bp
from app.views.audit import audit_bp
from app.views.report import report_bp
from app.views.teacher import teacher_bp

app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(class_bp)
app.register_blueprint(course_bp)
app.register_blueprint(grade_bp)
app.register_blueprint(status_bp)
app.register_blueprint(audit_bp)
app.register_blueprint(report_bp)
app.register_blueprint(teacher_bp)

