from flask import Flask, request, jsonify

app = Flask(__name__)

dest = ''
is_picked_up = False
is_arrived = False
is_found = False
cost = 0

@app.route('/')
def hello_world():
    return 'MR.TAXI'

@app.route('/find')
def find():
    global dest
    global is_arrived
    global is_picked_up
    global is_found

    is_found = True

    return 'Find!'

@app.route('/pickup')
def pickup():
    global dest
    global is_arrived
    global is_picked_up

    dest = request.args.get('dest', 0)
    is_arrived = False
    is_picked_up = True

    return 'PickUp! Dest: ' + dest

@app.route('/arrive')
def arrive():
    global dest
    global is_arrived
    global is_picked_up
    global cost

    dest = dest
    is_arrived = True
    is_picked_up = True

    cost = request.args.get('cost', 0)
    json_cost = {'cost' : cost}

    return jsonify(json_cost)

@app.route('/pay')
def pay():
    global dest
    global is_arrived
    global is_picked_up
    global is_found

    dest = ''
    is_arrived = False
    is_picked_up = False
    is_found = False

    return 'Paid!'

@app.route('/getdata')
def get():
    global dest
    global is_arrived
    global is_picked_up
    global is_found
    global cost

    data = {'dest': dest, 'is_arrived': is_arrived, 'is_picked_up': is_picked_up, 'is_found': is_found, 'cost': cost}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)