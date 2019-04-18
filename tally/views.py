from tally import app, db
from tally.forms import ApplicantForm, WorkExperience, ExtraActivity
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
    print(form.validate_on_submit()) #returns false
    if form.is_submitted(): #submitting without validating
        print(form.school.data, form.gpa.data, form.major.data, form.email.data, form.phone.data, work.company.data, activity.role.data)
        return redirect('/') #redirects to home screen
    return render_template("input_resume.html", form=form, work=work, activity=activity)

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")
