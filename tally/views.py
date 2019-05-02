from tally import app, db, login_manager, model
from tally.forms import ApplicantForm, WorkExperience, ExtraActivity, CourseWork, JobForm, RegistrationForm, LoginForm
from tally.models import User
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from tally.classifier.classifier import score_experience, return_skills
from sklearn import preprocessing
import numpy as np

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
    user = db.users.find_one({"id": current_user.get_id()})
    open_roles = user["open_roles"]

    roles = []
    teams = []

    qualities = []

    for index in range(len(open_roles)):
        print(index)
        print(open_roles[index]['role'])
        roles.append(open_roles[index]['role'])
        qualities.append(open_roles[index]['qualities'])
        teams.append(open_roles[index]['team'])
    print(qualities)
    return render_template("index.html", user_info = user, roles = roles, teams = teams, qualities = qualities)
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

            # User has not filled out resume yet
            if user["role"] == "student" and len(user) <=5:
                return redirect(url_for('input_resume'))
            elif user_obj.role == 'recruiter':
                return redirect('/role_builder')
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
    user_name = db.users.find_one({"id": current_user.get_id()})["username"]
    if form.is_submitted() and work.is_submitted(): #submitting without validating
        print(form.name.data, form.school.data, form.gpa.data, form.major.data, form.email.data, form.phone.data)
        print(work.company.data, work.role.data, work.work_desc.data)
        db.users.find_one_and_update({"id": current_user.get_id()}, {"$set": {"name": form.name.data, "school": form.school.data, "major": form.major.data, "email": form.email.data, "phone": form.phone.data}})
        if work.work_desc.data != "" and work.company.data is not None:
            db.users.find_one_and_update({"id": current_user.get_id()}, {"$push": {"work_exps": {"company": work.company.data, "role": work.role.data, "desc": work.work_desc.data}}}, upsert=True)
        if activity.extra_desc.data != "" and activity.group.data is not None:
            db.users.find_one_and_update({"id": current_user.get_id()}, {"$push": {"activity": {"group": activity.group.data, "role": activity.title.data, "desc": activity.extra_desc.data}}}, upsert=True)
        if course.course_title.data != "" and course.course_title.data is not None:
            db.users.find_one_and_update({"id": current_user.get_id()}, {"$push": {"course": {"course_title": course.course_title.data, "role": course.category.data, "desc": course.course_desc.data}}}, upsert=True)

        # Calculate skills according to descriptions given
        user_info = db.users.find_one({"id": current_user.get_id()})
        descriptions = []
        for exp in user_info["work_exps"]:
            descriptions.append(exp["desc"])
        for exp in user_info["activity"]:
            descriptions.append(exp["desc"])
        for exp in user_info["course"]:
            descriptions.append(exp["desc"])
        skills, scores = classifier_test(descriptions)
        print(skills, scores)
        sorted_skills = [skills for _,skills in sorted(zip(scores, skills), reverse = True)]
        sorted_scores = sorted(scores, reverse = True)
        print(sorted_skills, sorted_scores)
        db.users.find_one_and_update({"id": current_user.get_id()}, {"$set": {"skills": {"types": sorted_skills, "scores": sorted_scores}}}, upsert=True)
        return redirect('/profile') #redirects to home screen
    return render_template("input_resume.html", form=form, work=work, activity=activity, course=course, user_name= user_name)

@app.route('/role_builder', methods=['GET', 'POST'])
def role_builder():
    user_name = db.users.find_one({"id": current_user.get_id()})["username"]

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
    return render_template("role_builder.html", jobform=jobform, user_name = user_name)

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


@app.route('/profile')
@login_required
def profile():
    print(current_user.get_id())
    user_info = db.users.find_one({"id": current_user.get_id()})
    return render_template("profile.html", user_info = user_info, user_name = user_info["username"])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def classifier_test(descriptions = []):
    skills = return_skills()

    scores_list = []
    scores = []

    for desc in descriptions:
        scores_list.append(score_experience(model, desc))
    scores = [sum(x) for x in zip(*scores_list)]

    score_min = min(scores)
    score_max = max(scores)
    score_range= score_max - score_min

    normalized = [(score) * 10/score_max for score in scores]
    return skills, normalized

@app.route('/find_top_matches/<role_id>', methods = ["GET"])
def find_top_matches(role_id, n_top = 2):
    student_scores = []
    ids = []
    students = list(db.users.find({"role": "student"}))
    recruiter_info = db.users.find_one({"id": current_user.get_id()})
    open_roles = recruiter_info["open_roles"]
    role_id = int(role_id)
    role = open_roles[role_id] # find role

    for student in students:
        scores = student["skills"]["scores"]

        # get scores that match with the skills that matter for the role
        types = student["skills"]["types"]

        scores_2 = []
        for ind in range(len(types)):
            if types[ind] in role['qualities']:
                scores_2.append(scores[ind])

        student_scores.append(sum(scores_2))
        ids.append(student["id"])

    if len(student_scores) < n_top:
        min_len = len(student_scores)
    else:
        min_len = n_top

    index_scores = np.argsort(student_scores)
    index_scores = index_scores[::-1]
    top_ids = []
    user_info_list = []
    print(student_scores)
    print(index_scores)
    for i in range(min_len):
        #top_ids.append(ids[index_scores[i]])
        user_info = db.users.find_one({"id": ids[index_scores[i]]})
        user_info_list.append(user_info["id"])
        user_info_list.append(user_info["name"])
        print(user_info["name"])
        print(student_scores[i])
        user_info_list.append(user_info["skills"])
    return str(user_info_list)


### Test Server ###
@app.route('/helloworld')
def hello_world():
    return "Hello World!"
