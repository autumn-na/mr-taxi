from flask import Flask, request, jsonify


app = Flask(__name__)

dest = ''

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/setdest')
def set_dest():
    global dest
    dest = request.args.get('dest', "default")

    return 'Destination Set! ' + dest

@app.route('/getdest')
def get_dest():
    global dest
    json_dest = {'dest' : dest}

    return jsonify(json_dest)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)