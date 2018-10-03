from flask import Flask, render_template    # g, jsonify -- for token-based authentication
from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr

# from auth import auth
from config import DEBUG, DEFAULT_RATE, HOST, PORT
from models import initialize, User
from resources.todos import todo_api
from resources.users import users_api

app = Flask(__name__)
app.register_blueprint(todo_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')

limiter = Limiter(app, global_limits=[DEFAULT_RATE], key_func=get_ipaddr)
limiter.limit('100/day')(users_api)
limiter.limit(DEFAULT_RATE, per_method=True,
              methods=['post', 'put', 'delete'])(todo_api)


@app.route('/')
def my_todos():
    return render_template('index.html')

# TOKEN-BASED AUTHENTICATION
# @app.route('/api/v1/users/token', methods=['GET'])
# @auth.login_required
# def get_auth_token():
#     token = g.user.generate_auth_token()
#     return jsonify({'token': token.decode('ascii')})


if __name__ == '__main__':
    initialize()
    # try:
    #     User.create_user(
    #         username='test_user',
    #         password='password'
    #     )
    # except ValueError:
    #     pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
