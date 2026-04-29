from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class StatusForm(FlaskForm):
    status = SelectField('学籍状态', choices=[('在读', '在读'), ('休学', '休学'), ('复学', '复学'), ('转学', '转学'), ('退学', '退学'), ('毕业', '毕业')], validators=[DataRequired()])
    change_reason = TextAreaField('变更原因', validators=[DataRequired()])
    submit = SubmitField('提交')