from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Student

class StudentForm(FlaskForm):
    student_id = StringField('学号', validators=[DataRequired(), Length(min=10, max=10)])
    name = StringField('姓名', validators=[DataRequired(), Length(max=50)])
    gender = SelectField('性别', choices=[('男', '男'), ('女', '女')], validators=[DataRequired()])
    birthday = DateField('出生日期', validators=[DataRequired()])
    id_card = StringField('身份证号', validators=[DataRequired(), Length(min=18, max=18)])
    phone = StringField('手机号', validators=[DataRequired(), Length(min=11, max=11)])
    address = StringField('地址', validators=[DataRequired(), Length(max=200)])
    class_id = SelectField('班级', validators=[DataRequired()])
    submit = SubmitField('提交')
    
    def validate_student_id(self, student_id):
        student = Student.query.filter_by(student_id=student_id.data).first()
        if student:
            raise ValidationError('该学号已存在')
    
    def validate_id_card(self, id_card):
        student = Student.query.filter_by(id_card=id_card.data).first()
        if student:
            raise ValidationError('该身份证号已存在')

class StudentUpdateForm(FlaskForm):
    student_id = StringField('学号', validators=[DataRequired(), Length(min=10, max=10)])
    name = StringField('姓名', validators=[DataRequired(), Length(max=50)])
    gender = SelectField('性别', choices=[('男', '男'), ('女', '女')], validators=[DataRequired()])
    birthday = DateField('出生日期', validators=[DataRequired()])
    id_card = StringField('身份证号', validators=[DataRequired(), Length(min=18, max=18)])
    phone = StringField('手机号', validators=[DataRequired(), Length(min=11, max=11)])
    address = StringField('地址', validators=[DataRequired(), Length(max=200)])
    class_id = SelectField('班级', validators=[DataRequired()])
    submit = SubmitField('提交')