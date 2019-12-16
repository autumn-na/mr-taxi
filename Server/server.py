from flask import Flask, request, jsonify

app = Flask(__name__)

dest = ''
is_arrived = False

@app.route('/')
def hello_world():
    return 'MR.TAXI'

@app.route('/pickup')
def pickup():
    global dest
    global is_arrived

    dest = request.args.get('dest', 0)
    is_arrived = False

    return 'PickUp! Dest: ' + dest

@app.route('/arrive')
def arrive():
    global dest
    global is_arrived

    dest = dest
    is_arrived = True

    cost = request.args.get('cost', 0)
    json_cost = {'cost' : cost}

    return jsonify(json_cost)

@app.route('/pay')
def pay():
    global dest
    global is_arrived

    dest = ''
    is_arrived = False

    return 'Paid!'

@app.route('/getdata')
def get():
    global dest
    global is_arrived

    data = {'dest': dest, 'is_arrive': is_arrived}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)