from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app import app, db, bcrypt
from app.models import Teacher, Course, OperationLog, User
from app.views.teacher_forms import TeacherForm


#对操作进行日志记录。它接收用户ID、操作类型、操作内容、
#操作IP以及操作结果作为参数，并将这些信息存入OperationLog对象中，最后将这些存入数据库。
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


#展示所有教师信息的页面。只有具有管理员权限的用户才能访问此页面，否则会被重定向到学生页面
@login_required
def index():
    if current_user.role != 'admin':
        flash('权限不足！', 'danger')
        return redirect(url_for('student.index'))
    
    teachers = Teacher.query.all()
    return render_template('teacher/index.html', teachers=teachers, title='教师管理')

#管理员可以添加教师信息，并创建对应的用户账户。
#如果管理员输入了密码，系统会使用这个密码，否则默认密码为"teacher123"。所有的密码都会被哈希加密存储。
@login_required
def add():
    if current_user.role != 'admin':
        flash('权限不足！', 'danger')
        return redirect(url_for('student.index'))
    
    form = TeacherForm()
    form.course_id.choices = [(course.id, course.course_name) for course in Course.query.all()]
    
    if form.validate_on_submit():
        if Teacher.query.filter_by(teacher_id=form.teacher_id.data).first():
            flash('教师账号已存在！', 'danger')
            return redirect(url_for('teacher.add'))
        
        # 获取密码，默认为 teacher123
        password = form.password.data if form.password.data else 'teacher123'
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        teacher = Teacher(
            teacher_id=form.teacher_id.data,
            name=form.name.data,
            password=hashed_password,
            course_id=form.course_id.data
        )
        db.session.add(teacher)
        
        # 创建对应的用户账号
        user = User(
            username=form.teacher_id.data,
            password=hashed_password,
            role='teacher'
        )
        db.session.add(user)
        
        db.session.commit()
        
        log_operation(current_user.id, '新增', f'新增教师: {form.teacher_id.data}', request.remote_addr, '成功')
        flash('教师添加成功！', 'success')
        return redirect(url_for('teacher.index'))
    
    return render_template('teacher/add.html', form=form, title='添加教师')


#管理员可以更新教师信息，包括姓名和课程ID。如果管理员输入了新密码，
#那么教师的密码会被更新。所有的密码都会被哈希加密存储。
@login_required
def update(id):
    if current_user.role != 'admin':
        flash('权限不足！', 'danger')
        return redirect(url_for('student.index'))
    
    teacher = Teacher.query.get_or_404(id)
    form = TeacherForm()
    form.course_id.choices = [(course.id, course.course_name) for course in Course.query.all()]
    
    if form.validate_on_submit():
        teacher.name = form.name.data
        teacher.course_id = form.course_id.data
        
        # 如果填写了新密码，则更新密码
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            teacher.password = hashed_password
            
            # 更新对应的用户账号密码
            user = User.query.filter_by(username=teacher.teacher_id).first()
            if user:
                user.password = hashed_password
        
        db.session.commit()
        
        log_operation(current_user.id, '修改', f'修改教师: {teacher.teacher_id}', request.remote_addr, '成功')
        flash('教师信息修改成功！', 'success')
        return redirect(url_for('teacher.index'))
    
    form.teacher_id.data = teacher.teacher_id
    form.name.data = teacher.name
    form.course_id.data = teacher.course_id
    form.teacher_id.render_kw = {'readonly': True}
    
    return render_template('teacher/update.html', form=form, title='修改教师信息')

#管理员可以删除教师以及其对应的用户账户。
@login_required
def delete(id):
    if current_user.role != 'admin':
        flash('权限不足！', 'danger')
        return redirect(url_for('student.index'))
    
    teacher = Teacher.query.get_or_404(id)
    
    # 删除对应的用户账号
    user = User.query.filter_by(username=teacher.teacher_id).first()
    if user:
        db.session.delete(user)
    
    db.session.delete(teacher)
    db.session.commit()
    
    log_operation(current_user.id, '删除', f'删除教师: {teacher.teacher_id}', request.remote_addr, '成功')
    flash('教师删除成功！', 'success')
    return redirect(url_for('teacher.index'))
