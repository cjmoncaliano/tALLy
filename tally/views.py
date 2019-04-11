from tally import app, db
from flask import render_template
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

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")