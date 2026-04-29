from flask import Blueprint
from app.controllers.class_ import index, add, update, delete

class_bp = Blueprint('class', __name__, url_prefix='/class')

class_bp.route('/')(index)
class_bp.route('/add', methods=['GET', 'POST'])(add)
class_bp.route('/update/<int:id>', methods=['GET', 'POST'])(update)
class_bp.route('/delete/<int:id>')(delete)

# 前端访问/class/            →    执行函数index()      显示所有班级列表
# 前端访问/class/add         →    执行函数add()        添加一个新班级
# 前端访问/class/update/1    →    执行函数update()     修改第1号班级
# 前端访问/class/delete/1    →    执行函数delete()     删除第1号班级