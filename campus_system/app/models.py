from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


# 用Flask的SQLAlchemy工具包，把数据库表变成了Python里的类


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# ---------------------- 系统用户表 ----------------------
# 存储所有登录用户账号权限，继承UserMixin获得登录所需默认方法
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.role}')"
# ---------------------- 班级信息表 ----------------------
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), unique=True, nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    students = db.relationship('Student', backref='class_', lazy=True)
    
    def __repr__(self):
        return f"Class('{self.class_name}')"
# ---------------------- 学生信息表 ----------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    id_card = db.Column(db.String(18), unique=True, nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    status = db.relationship('StudentStatus', backref='student', uselist=False, lazy=True)
    grades = db.relationship('Grade', backref='student', lazy=True)
    
    def __repr__(self):
        return f"Student('{self.student_id}', '{self.name}')"
# ---------------------- 课程信息表 ----------------------
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    credit = db.Column(db.Float, nullable=False)
    grades = db.relationship('Grade', backref='course', lazy=True)
    
    def __repr__(self):
        return f"Course('{self.course_code}', '{self.course_name}')"
# ---------------------- 学生成绩表 ----------------------
class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10), db.ForeignKey('student.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    daily_score = db.Column(db.Float, nullable=False)
    exam_score = db.Column(db.Float, nullable=False)
    total_score = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='unlocked')  # unlocked, locked
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"Grade('{self.student_id}', '{self.course_id}', '{self.total_score}')"
# ---------------------- 学生学籍变动表 ----------------------
class StudentStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10), db.ForeignKey('student.student_id'), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 在读, 休学, 复学, 转学, 退学, 毕业
    change_reason = db.Column(db.String(500), nullable=True)
    change_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    operator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"StudentStatus('{self.student_id}', '{self.status}')"
# ---------------------- 系统操作日志表 ----------------------
class OperationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    operation_type = db.Column(db.String(50), nullable=False)
    operation_content = db.Column(db.String(1000), nullable=False)
    operation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    operation_ip = db.Column(db.String(50), nullable=False)
    operation_result = db.Column(db.String(20), nullable=False)  # success, failed
    
    def __repr__(self):
        return f"OperationLog('{self.user_id}', '{self.operation_type}', '{self.operation_time}')"