from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, bcrypt
from app.models import User, OperationLog
from app.views.auth_forms import LoginForm, RegistrationForm

#记录操作结果，返回给管理人员的操作日志

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


#处理用户登录请求。如果用户已经登录，根据角色重定向到不同页面；
# 如果用户还没登录，验证其输入的用户名和密码，若验证成功，将用户登录状态设置为已登录，
# 并重定向到其下一步请求的页面或者不同角色的默认页面。
# 无论登录成功与否，都会记录操作日志。

def login():                             # 接收到前端发送的请求后该函数被调用
    from app.models import Teacher
    if current_user.is_authenticated:    # 检查登陆状态
        if current_user.role == 'student':
            return redirect(url_for('student.profile'))##是学生往学生的主界面跳
        else:
            return redirect(url_for('student.index'))##系统首页
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # 教师角色需要验证是否在教师表中
            if user.role == 'teacher':
                teacher = Teacher.query.filter_by(teacher_id=user.username).first()
                if not teacher:
                    log_operation(0, 'login', f'登录失败: 教师 {user.username} 不在教师表中', request.remote_addr, 'failed')
                    flash('登录失败，该教师账号未在系统中注册', 'danger')
                    return render_template('auth/login.html', title='登录', form=form)
            login_user(user)
            next_page = request.args.get('next')
            log_operation(user.id, 'login', f'用户 {user.username} 登录系统', request.remote_addr, 'success')
            if next_page:
                return redirect(next_page)
            else:
                if user.role == 'student':
                    return redirect(url_for('student.profile'))
                else:
                    return redirect(url_for('student.index'))
        else:
            log_operation(0, 'login', f'登录失败: {form.username.data}', request.remote_addr, 'failed')
            flash('登录失败，请检查账号和密码', 'danger')
    return render_template('auth/login.html', title='登录', form=form)



# 处理用户注册请求。若用户已登录，重定向到了学生的主页；
# 未登录，创建一个新用户，保存到数据库，并记录操作日志。
# 注册完成后，提示用户注册成功并重定向到登录页面。

def register():
    if current_user.is_authenticated:
        return redirect(url_for('student.index'))
    form = RegistrationForm()##注册表单
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        ##用了某种加密，Db中也看不到
        user = User(username=form.username.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        log_operation(current_user.id if current_user.is_authenticated else 0, 'register', f'注册新用户: {form.username.data}', request.remote_addr, 'success')
        flash('注册成功，请登录', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='注册', form=form)


# 处理用户注销请求，将用户的登录状态设置为未登录，并重定向到登录页面。
# 如果用户已登录，还会记录操作日志。

def logout():
    if current_user.is_authenticated:
        log_operation(current_user.id, 'logout', f'用户 {current_user.username} 退出系统', request.remote_addr, 'success')
    logout_user()
    return redirect(url_for('auth.login'))