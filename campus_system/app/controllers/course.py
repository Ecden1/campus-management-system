from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app import app, db
from app.models import Course, OperationLog, StudentCourse, Teacher, Student
from app.views.course_forms import CourseForm


#记录操作日志
def log_operation(user_id, operation_type, operation_content, operation_ip, operation_result):
    log = OperationLog(
        user_id=user_id,
        operation_type=operation_type,
        operation_content=operation_content,
        operation_ip=operation_ip,
        operation_result=operation_result
    )
    db.session.add(log)
    db.session.commit()


#展示所有课程信息。
#如果当前用户是学生则同时展示已选课程信息。
@login_required
def index():
    courses = Course.query.all()
    
    # 获取每门课程的任课教师信息
    course_teachers = {}
    for course in courses:
        teachers = Teacher.query.filter_by(course_id=course.id).all()
        course_teachers[course.id] = teachers
    
    # 对于学生角色，获取已选课程信息
    if current_user.role == 'student':
        # 获取学生已选的课程ID列表
        enrolled_course_ids = [sc.course_id for sc in StudentCourse.query.filter_by(student_id=current_user.username).all()]
        return render_template('course/index.html', courses=courses, enrolled_course_ids=enrolled_course_ids, course_teachers=course_teachers, title='课程管理')
    else:
        return render_template('course/index.html', courses=courses, course_teachers=course_teachers, title='课程管理')

#add函数：添加新课程。
#此函数从CourseForm中获取数据，在数据库中创建新课程，然后重定向回课程列表页面。
@login_required
def add():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            course_code=form.course_code.data,
            course_name=form.course_name.data,
            credit=form.credit.data
        )
        db.session.add(course)
        db.session.commit()
        log_operation(current_user.id, 'add_course', f'添加课程: {course.course_code} - {course.course_name}', request.remote_addr, 'success')
        flash('课程添加成功', 'success')
        return redirect(url_for('course.index'))
    return render_template('course/add.html', form=form, title='添加课程')


#update函数：更新课程。
#此函数从CourseForm中获取数据，更新数据库中的课程信息，然后重定向回课程列表页面。
@login_required
def update(id):
    course = Course.query.get_or_404(id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        course.course_code = form.course_code.data
        course.course_name = form.course_name.data
        course.credit = form.credit.data
        db.session.commit()
        log_operation(current_user.id, 'update_course', f'更新课程: {course.course_code} - {course.course_name}', request.remote_addr, 'success')
        flash('课程信息更新成功', 'success')
        return redirect(url_for('course.index'))
    return render_template('course/update.html', form=form, course=course, title='更新课程')


#delete函数：删除课程。
#此函数根据ID获取课程，从数据库中删除，然后重定向回课程列表页面。
@login_required
def delete(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    log_operation(current_user.id, 'delete_course', f'删除课程: {course.course_code} - {course.course_name}', request.remote_addr, 'success')
    flash('课程删除成功', 'success')
    return redirect(url_for('course.index'))


#enroll(course_id) 函数的主要职责是：处理学生选择课程的操作。下面是详细的逻辑：
#首先，通过 login_required 装饰器，确保只有登录用户可以进行选课操作。
#接着，检查当前登录用户的角色是否为学生。如果非学生用户尝试选课，将会返回一个错误信息并重定向到课程列表页面。
#然后，查询数据库以检查学生是否已经选择了这门课程。如果已选，返回一个信息并重定向到课程列表页面。
#如果学生未选该课程，就创建一个新的记录，记录学生已选择该课程，并将状态设置为 "enrolled"（已选课）。
#然后，将这个新的记录添加到数据库并提交更改。
#最后，记录这次操作并向用户返回成功的反馈信息，再重定向到课程列表页面。
@login_required
def enroll(course_id):
    if current_user.role != 'student':
        flash('权限不足', 'danger')
        return redirect(url_for('course.index'))
    
    # 检查是否已经选课
    existing = StudentCourse.query.filter_by(student_id=current_user.username, course_id=course_id).first()
    if existing:
        flash('您已经选择了这门课程', 'info')
        return redirect(url_for('course.index'))
    
    # 添加选课记录
    student_course = StudentCourse(
        student_id=current_user.username,
        course_id=course_id,
        status='enrolled'
    )
    db.session.add(student_course)
    db.session.commit()
    
    course = Course.query.get(course_id)
    log_operation(current_user.id, 'enroll_course', f'选课: {course.course_code} - {course.course_name}', request.remote_addr, 'success')
    flash('选课成功', 'success')
    return redirect(url_for('course.index'))


#drop(course_id) 函数的主要职责是：处理学生取消选课的操作。下面是详细的逻辑：
#首先，通过 login_required 装饰器，确保只有登录用户可以进行取消选课操作。
#查当前登录用户的角色是否为学生。如果非学生用户尝试取消选课，将会返回一个错误信息并重定向到课程列表页面。
#然后，查询数据库以检查学生是否已经选择了这门课程。如果未选，返回一个信息并重定向到课程列表页面。
#如果学生已选该课程，则将该记录从数据库中删除并提交更改。
#最后，记录这次操作并向用户返回成功的反馈信息，再重定向到课程列表页面。
@login_required
def drop(course_id):
    if current_user.role != 'student':
        flash('权限不足', 'danger')
        return redirect(url_for('course.index'))
    
    # 检查是否已经选课
    existing = StudentCourse.query.filter_by(student_id=current_user.username, course_id=course_id).first()
    if not existing:
        flash('您还没有选择这门课程', 'info')
        return redirect(url_for('course.index'))
    
    # 删除选课记录
    db.session.delete(existing)
    db.session.commit()
    
    course = Course.query.get(course_id)
    log_operation(current_user.id, 'drop_course', f'取消选课: {course.course_code} - {course.course_name}', request.remote_addr, 'success')
    flash('取消选课成功', 'success')
    return redirect(url_for('course.index'))


#展示选了某课程的所有学生。
#只有非学生用户（如教师、管理员）才能访问此函数。
@login_required
def students(id):
    if current_user.role == 'student':
        flash('权限不足', 'danger')
        return redirect(url_for('course.index'))
    
    course = Course.query.get_or_404(id)
    # 获取选择该课程的所有学生
    student_courses = StudentCourse.query.filter_by(course_id=id).all()
    student_ids = [sc.student_id for sc in student_courses]
    students = Student.query.filter(Student.student_id.in_(student_ids)).all()
    
    return render_template('course/students.html', course=course, students=students, title='选课学生列表')