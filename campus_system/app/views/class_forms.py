from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Class

class ClassForm(FlaskForm):
    class_name = StringField('班级名称', validators=[DataRequired(), Length(max=50)])
    grade = StringField('年级', validators=[DataRequired(), Length(max=20)])
    major = StringField('专业', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('提交')
    
    def validate_class_name(self, class_name):
        class_ = Class.query.filter_by(class_name=class_name.data).first()
        if class_:
            raise ValidationError('该班级名称已存在')