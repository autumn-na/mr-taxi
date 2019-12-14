from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'MR.TAXI'

@app.route('/pickup')
def pickup():
    return 'PickUp!'

@app.route('/arrive')
def arrive():
    global dest

    cost = request.args.get('cost', 0)
    json_cost = {'cost' : cost}

    return jsonify(json_cost)

@app.route('/pay')
def pay():
    global dest
    dest = ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)