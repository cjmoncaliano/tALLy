from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

class WorkExperience(FlaskForm):
    company = StringField('Company Name')
    role = StringField('Role/Title')
    work_desc = StringField('Description')

class ExtraActivity(FlaskForm):
    group = StringField('Group Name')
    title = StringField('Role/Title')
    extra_desc = StringField('Description')

class CourseWork(FlaskForm):
    course_title = StringField('Course Name')
    category = StringField('Category')
    course_desc = StringField('Description')

class ApplicantForm(FlaskForm):
    name = StringField('Full Name')
    email = StringField('Email')
    school = StringField('School')
    gpa = StringField('GPA')
    major = StringField('Major(s)/Minor(s)')
    phone = StringField('Phone Number')
    submit = SubmitField('Submit')

class JobForm(FlaskForm):
    company = StringField('Company', validators=[DataRequired()])
    role = StringField('Role/Title', validators=[DataRequired()])
    team = StringField('Team', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    deadline = StringField('Application Deadline', validators=[DataRequired()])
    qualities = SelectMultipleField('Top Qualities', choices =[('collaboration', 'Collaboration'),
        ('persistence', 'Persistence'), \
        ('quantitative', 'Quantitative'), \
        ('leadership', 'Leadership'), \
        ('adaptability', 'Adaptability'), \
        ('creativity', 'Creativity')],validators=[DataRequired()])
    major = StringField('Preferred Major(s)/Minor(s)', validators=[DataRequired()])
    year = StringField('School Year', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices =[('student', 'Student'), ('recruiter', 'Recruiter')], validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
