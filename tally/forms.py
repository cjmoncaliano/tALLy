from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
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
    submit = SubmitField('Done')

class RegistrationForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices =[('student', 'Student'), ('recruiter', 'Recruiter')], validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
