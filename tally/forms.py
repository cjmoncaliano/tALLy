from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class WorkExperience(FlaskForm):
    company = StringField('Company Name')
    
    role = StringField('Role/Title')
    
    desc = StringField('Description')
    
class ExtraActivity(FlaskForm):
    group = StringField('Company Name')
    
    role = StringField('Role/Title')
    
    desc = StringField('Description')
    
class CourseWork(FlaskForm):
    title = StringField('Company Name')
    
    category = StringField('Role/Title')
    
    desc = StringField('Description')

class ApplicantForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    
    school = StringField('School', validators=[DataRequired()])
    
    gpa = StringField('GPA', validators=[DataRequired()])
    
    major = StringField('Major(s)/Minor(s)', validators=[DataRequired()])
    
    phone = StringField('Phone Number', validators=[DataRequired()])
    
    #course = CourseWork()
    
    submit = SubmitField('Done')
    
    