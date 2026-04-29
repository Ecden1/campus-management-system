from flask import render_template, redirect, url_for
from flask_login import current_user

# 处理访问请求，关联“auth.py”模块，根据auth中的身份信息跳转到对应界面
# 以实现不同身份登录到对应的端口

def home():
    if current_user.is_authenticated:
        if current_user.role == 'student':
            return redirect(url_for('student.profile'))
        else:
            return redirect(url_for('student.index'))
    return render_template('home.html')

