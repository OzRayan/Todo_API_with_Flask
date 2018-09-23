from flask import Flask, g, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr

from config import DEBUG, DEFAULT_RATE, HOST, PORT
from models import initialize

app = Flask(__name__)


@app.route('/')
def my_todos():
    return render_template('index.html')


if __name__ == '__main__':
    initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
