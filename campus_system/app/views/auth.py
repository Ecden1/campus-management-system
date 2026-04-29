from flask import Blueprint
from app.controllers.auth import login, register, logout

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_bp.route('/login', methods=['GET', 'POST'])(login)
auth_bp.route('/register', methods=['GET', 'POST'])(register)
auth_bp.route('/logout')(logout)

# "将特定的URL路径映射到特定的Python视图函数上"

# 当浏览器访问 /auth/login 时 → 执行 login() 函数

# 当浏览器访问 /auth/register 时 → 执行 register() 函数

# 当浏览器访问 /auth/logout 时 → 执行 logout() 函数
