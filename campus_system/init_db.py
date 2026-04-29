from app import app, db
from app.models import User, Class, Student, Course, Grade, StudentStatus, OperationLog
from flask_bcrypt import Bcrypt
import random
from datetime import datetime, timedelta
# 原生sql语句
# 初始化数据库
def init_db():
    with app.app_context():
        # 删除所有表
        db.drop_all()
        # 创建所有表
        db.create_all()
        
        # 创建默认管理员用户
        bcrypt = Bcrypt(app)
        admin = User(
            username='admin',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            role='admin'
        )
        db.session.add(admin)
        
        # 创建默认教师用户
        teacher = User(
            username='teacher',
            password=bcrypt.generate_password_hash('teacher123').decode('utf-8'),
            role='teacher'
        )
        db.session.add(teacher)
        
        # 创建班级
        classes = []
        for i in range(174, 186):  # 2023174到2023185
            class_ = Class(
                class_name=f'2023{i}',
                grade='2023级',
                major='计算机科学与技术'
            )
            classes.append(class_)
            db.session.add(class_)
        
        # 创建计算机相关课程
        courses = []
        course_list = [
            ('CS101', '计算机基础', 3.0),
            ('CS102', '编程语言', 4.0),
            ('CS103', '数据结构', 4.0),
            ('CS104', '操作系统', 3.5),
            ('CS105', '计算机网络', 3.5),
            ('CS106', '数据库原理', 3.0),
            ('CS107', '算法设计与分析', 3.0),
            ('CS108', '软件工程', 3.0)
        ]
        for code, name, credit in course_list:
            course = Course(
                course_code=code,
                course_name=name,
                credit=credit
            )
            courses.append(course)
            db.session.add(course)
        
        # 提交班级和课程数据
        db.session.commit()
        
        # 创建学生数据
        students = []
        names = ['张', '王', '李', '赵', '钱', '孙', '周', '吴', '郑', '陈']
        first_names = ['明', '红', '军', '芳', '伟', '娜', '勇', '艳', '杰', '静']
        
        # 为每个班级分配25-30个学生
        for class_ in classes:
            # 每个班随机分配25-30个学生
            student_count = random.randint(25, 30)
            
            for i in range(1, student_count + 1):
                # 生成9位学号：2023 + 班级号 + 班内序号
                class_number = class_.class_name[4:]  # 提取班级号（如174）
                student_id = f'2023{class_number}{i:02d}'
                
                # 生成随机姓名
                last_name = random.choice(names)
                first_name = random.choice(first_names)
                name = last_name + first_name
                
                # 生成随机性别
                gender = random.choice(['男', '女'])
                
                # 生成随机出生日期（18-20岁）
                today = datetime.now()
                birthday = today - timedelta(days=random.randint(6570, 7300))  # 18-20岁
                
                # 生成随机身份证号（模拟）
                id_card = f'110101{birthday.strftime("%Y%m%d")}{random.randint(1000, 9999)}'
                
                # 生成随机手机号
                phone = f'138{random.randint(10000000, 99999999)}'
                
                # 生成随机地址
                address = f'北京市海淀区学院路{random.randint(1, 100)}号'
                
                student = Student(
                    student_id=student_id,
                    name=name,
                    gender=gender,
                    birthday=birthday,
                    id_card=id_card,
                    phone=phone,
                    address=address,
                    class_id=class_.id
                )
                students.append(student)
                db.session.add(student)
                
                # 创建学生用户
                student_user = User(
                    username=student_id,
                    password=bcrypt.generate_password_hash('student123').decode('utf-8'),
                    role='student'
                )
                db.session.add(student_user)
                
                # 创建初始学籍状态
                status = StudentStatus(
                    student_id=student_id,
                    status='在读',
                    operator_id='admin'
                )
                db.session.add(status)
        
        # 提交学生数据
        db.session.commit()
        
        # 创建成绩数据
        for student in students:
            for course in courses:
                # 生成随机成绩
                daily_score = random.randint(60, 100)
                exam_score = random.randint(60, 100)
                total_score = daily_score * 0.4 + exam_score * 0.6
                
                grade = Grade(
                    student_id=student.student_id,
                    course_id=course.id,
                    daily_score=daily_score,
                    exam_score=exam_score,
                    total_score=total_score,
                    status='unlocked'
                )
                db.session.add(grade)
        
        # 提交所有更改
        db.session.commit()
        print('数据库初始化完成！生成了以下数据：')
        print(f'- 管理员用户：1个')
        print(f'- 教师用户：1个')
        print(f'- 学生用户：{len(students)}个')
        print(f'- 班级：{len(classes)}个')
        print(f'- 课程：{len(courses)}个')
        print(f'- 成绩记录：{len(students) * len(courses)}条')

if __name__ == '__main__':
    init_db()