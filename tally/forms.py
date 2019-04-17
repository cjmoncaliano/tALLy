from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ApplicantForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    gpa = StringField('GPA', validators=[DataRequired()])
    major = StringField('Major(s)/Minor(s)', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Done')