from tally import app, db

### Test Server ###
@app.route('/helloworld')
def hello_world():
    return "Hello World!"