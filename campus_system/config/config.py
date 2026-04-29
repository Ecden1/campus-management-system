import os
from dotenv import load_dotenv

load_dotenv()

#项目基础配置

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'                              # 加密密钥
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///campus_system.db'   # 数据库地址，链接数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'data/uploads'                                                             # 上传文件存入地址
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # 邮件配置（可选）
    MAIL_SERVER = 'smtp.qq.com'                                                                # QQ邮件配置，通过QQ邮件找回密码等功能
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
class DevelopmentConfig(Config):                                                                # 开发环境
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {                                                                                      # 调用入口，分为开发和上线、两种端口
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
