from flask import Flask,make_response


#File for all the server stuff

app = Flask(__name__)

@app.route('/')
def index():
    return make_response('Home Page',200)


app.run(host='0.0.0.0',port=8080)