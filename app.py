from flask import Flask, g, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr

from auth import auth
from config import DEBUG, DEFAULT_RATE, HOST, PORT
from models import initialize
from resources.todos import todo_api

app = Flask(__name__)
app.register_blueprint(todo_api, url_prefix='/api/v1/')


@app.route('/')
def my_todos():
    return render_template('index.html')


@app.route('/api/v1/users/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


if __name__ == '__main__':
    initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
