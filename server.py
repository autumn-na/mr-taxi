from flask import Flask, escape, request

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "Flask2")
    return f'Hello, {escape(name)}!'


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080")
