from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app import app, db
from app.models import Class, OperationLog
from app.views.class_forms import ClassForm


# 这是一个操作记录函数，它可以记录用户的ID,
# 操作类型, 操作内容, 操作IP以及操作结果。
# 该函数实现构造对象后将对象保存到数据库
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


# 展示所有教师信息的页面。
# 只有具有管理员权限的用户才能访问此页面，否则会被重定向到（转到）学生页面。
@login_required
def index():
    classes = Class.query.all()
    return render_template('class/index.html', classes=classes, title='班级管理')


# 这是一个需要登录才能访问的添加班级信息页面，
# 可以创建新的班级，并保存到数据库。
@login_required
def add():
    form = ClassForm()
    if form.validate_on_submit():
        class_ = Class(
            class_name=form.class_name.data,
            grade=form.grade.data,
            major=form.major.data
        )
        db.session.add(class_)
        db.session.commit()
        log_operation(current_user.id, 'add_class', f'添加班级: {class_.class_name}', request.remote_addr, 'success')
        flash('班级添加成功', 'success')
        return redirect(url_for('class.index'))
    return render_template('class/add.html', form=form, title='添加班级')


# 登录后才能访问的更新班级信息页面，它根据id查询班级信息，
# 然后根据ClassForm更新班级信息，并保存到数据库。
@login_required
def update(id):
    class_ = Class.query.get_or_404(id)
    form = ClassForm(obj=class_)
    if form.validate_on_submit():
        class_.class_name = form.class_name.data
        class_.grade = form.grade.data
        class_.major = form.major.data
        db.session.commit()
        log_operation(current_user.id, 'update_class', f'更新班级: {class_.class_name}', request.remote_addr, 'success')
        flash('班级信息更新成功', 'success')
        return redirect(url_for('class.index'))
    return render_template('class/update.html', form=form, class_=class_, title='更新班级')

@login_required
def delete(id):
    class_ = Class.query.get_or_404(id)
    db.session.delete(class_)
    db.session.commit()
    log_operation(current_user.id, 'delete_class', f'删除班级: {class_.class_name}', request.remote_addr, 'success')
    flash('班级删除成功', 'success')
    return redirect(url_for('class.index'))