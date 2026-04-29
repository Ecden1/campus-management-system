# Models package
from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 该模块定义数据库结构

# `Teacher`模型用于表示教师，每个教师都有一个唯一的教师ID，名字，密码，并关联到一个课程ID
# `User`模型用于表示用户，每个用户都有一个唯一的用户名，密码，以及指定的角色
# `Class`模型用于表示班级，每个班级都有一个唯一的班级名，年级，以及专业
# `Student`模型用于表示学生，每个学生都有一个唯一的学生ID，姓名，性别，出生日期，身份证号，电话，
    # 地址和关联到一个班级ID
# `Course`模型用于表示课程，每个课程都有一个唯一的课程代码，课程名，以及学分
# `Grade`模型用于表示成绩，每个成绩都有一个唯一的学生ID，课程ID，平时成绩，考试成绩，总成绩和状态
# `OperationLog`模型用于记录操作日志，每条操作日志都有一个唯一的用户ID，操作类型，操作内容，操作时间，
    # 操作IP地址和操作结果




class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    course = db.relationship('Course', backref=db.backref('teachers', lazy=True))
    
    def __repr__(self):
        return f"Teacher('{self.teacher_id}', '{self.name}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.role}')"

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), unique=True, nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    students = db.relationship('Student', backref='class_', lazy=True)
    
    def __repr__(self):
        return f"Class('{self.class_name}')"

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
    courses = db.relationship('StudentCourse', backref='student', lazy=True)
    
    def __repr__(self):
        return f"Student('{self.student_id}', '{self.name}')"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    credit = db.Column(db.Float, nullable=False)
    grades = db.relationship('Grade', backref='course', lazy=True)
    students = db.relationship('StudentCourse', backref='course', lazy=True)
    
    def __repr__(self):
        return f"Course('{self.course_code}', '{self.course_name}')"

class StudentCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10), db.ForeignKey('student.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='enrolled')  # enrolled, completed
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='_student_course_uc'),)
    
    def __repr__(self):
        return f"StudentCourse('{self.student_id}', '{self.course_id}')"

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

class StudentStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10), db.ForeignKey('student.student_id'), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 在读, 休学, 复学, 转学, 退学, 毕业
    change_reason = db.Column(db.String(500), nullable=True)
    change_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    operator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"StudentStatus('{self.student_id}', '{self.status}')"

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
