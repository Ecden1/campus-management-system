from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User

# "定义前端表单的输入框和验证规则"

# 登录表单：用户输入账号密码时 → 检查是否为空、长度是否合格
class LoginForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')


# 注册表单：用户填写注册信息时 → 检查密码是否一致、账号是否已存在
class RegistrationForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('角色', choices=[('admin', '管理员'), ('teacher', '教师'), ('student', '学生')],
                       validators=[DataRequired()])
    submit = SubmitField('注册')

    # "自定义验证：去数据库检查这个账号有没有被注册过"
    # 如果账号已存在 → 提示'该账号已存在，请选择其他账号'
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该账号已存在，请选择其他账号')