from flask import Flask

app = Flask(__name__)


@app.route('/hi')
@app.route('/hi/<name>')
def hi(name='Programmer'):
    return '<h1>Hello {}!</h1>'.format(name)


@app.route('/')
def index():
    return '<h1>Hello Flask!</h1>'