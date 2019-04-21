from tally import app, db
from tally.forms import ApplicantForm, WorkExperience, ExtraActivity, CourseWork
from flask import render_template, redirect
### Test Server ###
@app.route('/helloworld')
def hello_world():
    return "Hello World!"


### splash page
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/create')
def create():
    return render_template("create_account.html")

@app.route('/input_resume', methods=['GET', 'POST'])
def input_resume():
    form = ApplicantForm()
    work = WorkExperience()
    activity = ExtraActivity()
    course = CourseWork()
    print(form.validate_on_submit()) #returns false
    if form.is_submitted(): #submitting without validating
        print(form.school.data, form.gpa.data, form.major.data, form.email.data, form.phone.data, work.company.data, work.role.data, work.desc.data, activity.role.data, activity.group.data, activity.desc.data, course.title.data, course.category.data, course.desc.data)
        return redirect('/') #redirects to home screen
    return render_template("input_resume.html", form=form, work=work, activity=activity, course=course)

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")
