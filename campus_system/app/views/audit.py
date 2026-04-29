from flask import Blueprint
from app.controllers.audit import index, search

audit_bp = Blueprint('audit', __name__, url_prefix='/audit')

audit_bp.route('/')(index)
audit_bp.route('/search')(search)


# 特定的网页链接到特定的 Python 函数上。
# "将特定的URL路径映射到特定的Python视图函数上"
# 当浏览器访问 /audit/ 时 → 执行 index() 函数
# 当浏览器访问 /audit/search 时 → 执行 search() 函数

# 这样，在网页上点击一个链接或者在浏览器中输入一个网址时，
# 方便调用对应的函数来处理请求和生成网页