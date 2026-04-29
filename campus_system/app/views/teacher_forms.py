from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class TeacherForm(FlaskForm):
    teacher_id = StringField('教师账号', validators=[
        DataRequired(message='请输入教师账号'),
        Length(min=4, max=20, message='教师账号长度必须在4-20个字符之间')
    ])
    name = StringField('教师姓名', validators=[
        DataRequired(message='请输入教师姓名'),
        Length(min=2, max=50, message='教师姓名长度必须在2-50个字符之间')
    ])
    password = PasswordField('密码', validators=[
        Optional(),
        Length(min=6, max=50, message='密码长度必须在6-50个字符之间')
    ], description='不填写则保持原密码')
    course_id = SelectField('教授科目', validators=[
        DataRequired(message='请选择教授科目')
    ], coerce=int)
    submit = SubmitField('提交')
