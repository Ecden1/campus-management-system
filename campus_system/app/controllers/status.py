from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app import app, db
from app.models import StudentStatus, Student, OperationLog
from app.views.status_forms import StatusForm
from datetime import datetime

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

# 显示所有学生的学籍状态
@login_required
def index():
    statuses = StudentStatus.query.all()
    return render_template('status/index.html', statuses=statuses, title='学籍管理')

# 这个函数用来更新特定学生的学籍状态。它首先从数据库查询指定ID的学生和他的学籍状态
# 如果学籍状态不存在，它会创建一个新的学籍状态
@login_required
def update_status(student_id):
    student = Student.query.filter_by(student_id=student_id).first_or_404()
    status = StudentStatus.query.filter_by(student_id=student_id).first()
    form = StatusForm()
    if form.validate_on_submit():
        if status:
            status.status = form.status.data
            status.change_reason = form.change_reason.data
            status.change_date = datetime.utcnow()
            status.operator_id = current_user.id
        else:
            status = StudentStatus(
                student_id=student_id,
                status=form.status.data,
                change_reason=form.change_reason.data,
                operator_id=current_user.id
            )
            db.session.add(status)
        db.session.commit()
        log_operation(current_user.id, 'update_status', f'更新学籍状态: {student_id} - {form.status.data}', request.remote_addr, 'success')
        flash('学籍状态更新成功', 'success')
        return redirect(url_for('status.index'))
    elif status:
        form.status.data = status.status
        form.change_reason.data = status.change_reason
    return render_template('status/update.html', form=form, student=student, title='更新学籍状态')