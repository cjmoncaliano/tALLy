from tally import app, db, login_manager, model
from tally.forms import ApplicantForm, WorkExperience, ExtraActivity, CourseWork, JobForm, RegistrationForm, LoginForm
from tally.models import User
from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from tally.classifier.classifier import score_experience
import uuid
### Login ###
@login_manager.user_loader
def load_user(userID):
    user = db.users.find_one({"id": str(userID)})
    if not user:
        return None
    return User(user["id"], user["role"])

### splash page
@app.route('/dashboard')
def index():
    print(current_user.get_id())
    user_info = db.users.find_one({"id": current_user.get_id()})
    print(user_info)
    return render_template("index.html", user_info = user_info)
    #return render_template("index.html")

@app.route('/', methods=["GET", "POST"])
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
            if user_obj.role == 'recruiter':
                return redirect('/dashboard')
            else:
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

@app.route('/role_builder', methods=['GET', 'POST'])
def role_builder():
    jobform = JobForm()
    if jobform.is_submitted(): #submitting without validating
        print("form was submitted")
        print(jobform.company.data, jobform.role.data, jobform.team.data, jobform.description.data)
        print(jobform.deadline.data, jobform.major.data, jobform.qualities.data, jobform.year.data)
        if jobform.company.data != "" and jobform.company.data is not None:
            db.users.find_one_and_update({
                "id": current_user.get_id()}, 
                {"$push": {"open_roles": {
                    "company": jobform.company.data, 
                    "role": jobform.role.data, 
                    "team": jobform.team.data, 
                    "desc": jobform.description.data, 
                    "deadline": jobform.deadline.data, 
                    "major": jobform.major.data, 
                    "qualities": jobform.qualities.data, 
                    "grad_year": jobform.year.data}}}, upsert=True)
        return redirect('/dashboard')
    return render_template("role_builder.html", jobform=jobform)

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
        if form.role.data == 'recruiter':
            db.users.find_one_and_update({
                "id": id}, 
                {"$push": {"open_roles": {
                    "company": None, 
                    "role": None, 
                    "team": None, 
                    "desc": None, 
                    "deadline": None, 
                    "major": None, 
                    "qualities": None, 
                    "grad_year": None}}}, upsert=True)
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


@app.route('/classifier_test')
def classifier_test():
    skill, score = score_experience(model, "Led teambuilding division to lead and motivate students.")
    print("\n\n\n")
    print(skill, score)
    print("\n\n\n")
    return "hello world"

### Test Server ###
@app.route('/helloworld')
def hello_world():
    return "Hello World!"
