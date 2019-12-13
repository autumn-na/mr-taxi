from flask import Flask, render_template, request

app = Flask(__name__)

dest = ''

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/setdest')
def ret_dest():
    global dest

    dest = request.args.get('dest', "")
    return 'Destination Set! ' + dest

if __name__ == '__main__':
    app.run()