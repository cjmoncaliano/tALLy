from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

class WorkExperience(FlaskForm):
    company = StringField('Company Name')
    role = StringField('Role/Title')
    work_desc = StringField('Description')

class ExtraActivity(FlaskForm):
    group = StringField('Company Name')
    title = StringField('Role/Title')
    extra_desc = StringField('Description')

class CourseWork(FlaskForm):
    title = StringField('Company Name')
    category = StringField('Category')
    course_desc = StringField('Description')

class ApplicantForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    gpa = StringField('GPA', validators=[DataRequired()])
    major = StringField('Major(s)/Minor(s)', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Submit')

class JobForm(FlaskForm):
    company = StringField('Company', validators=[DataRequired()])
    role = StringField('Role/Title', validators=[DataRequired()])
    team = StringField('Team', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    deadline = StringField('Application Deadline', validators=[DataRequired()])
    qualities = SelectMultipleField('Top Qualities', choices =[('collaboration', 'Collaboration'), \
        ('oral_comm', 'Oral Communication'), \
        ('conflict_resolution', 'Conflict Resolution'), \
        ('dedication', 'Dedication'), \
        ('leadershi', 'Leadership'), \
        ('adaptability', 'Adaptability'), \
        ('systems_thinking', 'Systems Thinking')],validators=[DataRequired()])
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
