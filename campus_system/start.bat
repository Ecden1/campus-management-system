@echo off
echo ========================================
echo 微校园学生信息管理系统
echo ========================================
echo.

echo [1] 安装依赖
pip install -r requirements.txt
echo.

echo [2] 初始化数据库
python init_db.py
echo.

echo [3] 启动应用
python run.py

pause