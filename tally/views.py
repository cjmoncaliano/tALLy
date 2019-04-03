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

@app.route('/aster_chart')
def aster_chart():
    return render_template("aster_chart.html")
