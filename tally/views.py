from tally import app, db, login_manager
from tally.forms import ApplicantForm, WorkExperience, ExtraActivity, CourseWork, RegistrationForm, LoginForm
from tally.models import User
from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
import uuid
### Login ###
@login_manager.user_loader
def load_user(userID):
    user = db.users.find_one({"id": str(userID)})
    if not user:
        return None
    return User(user["id"], user["role"])

### splash page
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = db.users.find_one({"username":form.username.data, \
        "password": form.password.data})
        print(form.username.data)
        print(user)
        if user is None:
            return "Invalid Credentials"
        else:
            user_obj = User(user["id"], user["role"])
            login_user(user_obj)
            return redirect(url_for('profile'))
    else:
        print(form.errors)
        return render_template("login.html", form=form)

@app.route('/input_resume', methods=['GET', 'POST'])
@login_required
def input_resume():
    if current_user.get_role() != "student":
        return "You are not allowed to access this page!"
    form = ApplicantForm()
    work = WorkExperience()
    activity = ExtraActivity()
    course = CourseWork()
    if form.is_submitted() and work.is_submitted(): #submitting without validating
        print(form.school.data, form.gpa.data, form.major.data, form.email.data, form.phone.data)
        db.users.find_one_and_update({"id": current_user.get_id()}, {"$set": {"school": form.school.data, "major": form.major.data, "email": form.email.data, "phone": form.phone.data}})
        if work.company.data != "" and work.company.data is not None:
            db.users.find_one_and_update({"id": current_user.get_id()}, {"$push": {"work_exps": {"company": work.company.data, "role": work.role.data, "desc": work.desc.data}}}, upsert=True)
        if activity.group.data != "" and activity.group.data is not None:
            db.users.find_one_and_update({"id": current_user.get_id()}, {"$push": {"activity": {"group": activity.group.data, "role": activity.role.data, "desc": activity.desc.data}}}, upsert=True)
        if course.title.data != "" and course.title.data is not None:
            db.users.find_one_and_update({"id": current_user.get_id()}, {"$push": {"course": {"title": course.title.data, "role": course.category.data, "desc": course.desc.data}}}, upsert=True)
        return redirect('/profile') #redirects to home screen
    return render_template("input_resume.html", form=form, work=work, activity=activity, course=course)

@app.route('/register', methods = ["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = db.users.find_one({"username": form.username.data})
        if user:
            return "Error: username taken"
        id = str(uuid.uuid4())
        db.users.insert_one({
            "username": form.username.data,
            # TODO: change this to hash and salt
            "password": form.password.data,
            "role": form.role.data,
            "id": id,
        })
        return redirect(url_for('login'))
    else:
        print(form.errors)
        return render_template('create_account.html', form = form)

'''
@app.route('/submit_resume', methods=['GET', 'POST'])
def submit_resume():
    form = ApplicantForm()
    print(form.validate_on_submit()) #returns false
    if form.is_submitted(): #submitting without validating
        print(form.school.data, form.gpa.data, form.major.data, form.email.data, form.phone.data)
        return redirect('/') #redirects to home screen
    return render_template("input_resume.html", form=form)
'''

@app.route('/profile')
@login_required
def profile():
    print(current_user.get_id())
    user_info = db.users.find_one({"id": current_user.get_id()})
    print(user_info)
    return render_template("profile.html", user_info = user_info)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

### Test Server ###
@app.route('/helloworld')
def hello_world():
    return "Hello World!"
