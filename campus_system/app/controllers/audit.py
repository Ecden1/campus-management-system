from flask import render_template, url_for, request
from flask_login import login_required
from app import app, db
from app.models import OperationLog, User


#完成调用后将参数传递给前端
def index():
    logs = OperationLog.query.order_by(OperationLog.operation_time.desc()).all()
    return render_template('audit/index.html', logs=logs, title='安全审计')


# 前端发送请求后
# 使用request.args.get()从GET请求中提取查询参数。
# 功能为日志筛选
def search():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    operation_type = request.args.get('operation_type')
    user_id = request.args.get('user_id')
    
    query = OperationLog.query
    
    if start_time:
        query = query.filter(OperationLog.operation_time >= start_time)
    if end_time:
        query = query.filter(OperationLog.operation_time <= end_time)
    if operation_type:
        query = query.filter(OperationLog.operation_type == operation_type)
    if user_id:
        query = query.filter(OperationLog.user_id == user_id)
    
    logs = query.order_by(OperationLog.operation_time.desc()).all()
    return render_template('audit/index.html', logs=logs, title='安全审计')