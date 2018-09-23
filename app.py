from flask import Flask, g, jsonify, render_template

from config import DEBUG, HOST, PORT

app = Flask(__name__)


@app.route('/')
def my_todos():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
