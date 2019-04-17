from tally import app, db, login_manager
from tally.forms import ApplicantForm, RegistrationForm, LoginForm
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

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/login_user')
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        # TODO: change this to hash and salt
        user = db.users.find_one({"username":form.username.data, \
        "password": form.password.data})
        if user is None:
            return "Invalid Credentials"
        else:
            user_obj = User(user["id"], user["role"])
            login_user(user_obj)
            return redirect(url_for('/profile'))
    else:
        return redirect(url_for('login'))


@app.route('/create')
def create():
    return render_template("create_account.html")

@app.route('/register')
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = db.users.find_one({"username": form.username.data})
        if user:
            return "Error: username taken"
        id = str(uuid.uuid4())
        db.users.insert_one({
            "username": form.username.data,
            # TODO: change this to hash and salt
            "password": form.password.data,
            "id": id,
        })
        return redirect(url_for('login'))
    else:
        return redirect(url_for('create'))


@app.route('/input_resume', methods=['GET', 'POST'])
def input_resume():
    form = ApplicantForm()
    print(form.validate_on_submit()) #returns false
    if form.is_submitted(): #submitting without validating
        print(form.school.data, form.gpa.data, form.major.data, form.email.data, form.phone.data)
        return redirect('/') #redirects to home screen
    return render_template("input_resume.html", form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


### Test Server ###
@app.route('/helloworld')
def hello_world():
    return "Hello World!"
