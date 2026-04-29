from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Course

class CourseForm(FlaskForm):
    course_code = StringField('课程代码', validators=[DataRequired(), Length(max=20)])
    course_name = StringField('课程名称', validators=[DataRequired(), Length(max=100)])
    credit = FloatField('学分', validators=[DataRequired()])
    submit = SubmitField('提交')
    
    def validate_course_code(self, course_code):
        course = Course.query.filter_by(course_code=course_code.data).first()
        if course:
            raise ValidationError('该课程代码已存在')