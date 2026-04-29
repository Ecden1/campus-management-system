from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class GradeForm(FlaskForm):
    student_id = SelectField('学生', validators=[DataRequired()])
    course_id = SelectField('课程', validators=[DataRequired()])
    daily_score = FloatField('平时成绩', validators=[DataRequired(), NumberRange(min=0, max=100)])
    exam_score = FloatField('期末成绩', validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('提交')