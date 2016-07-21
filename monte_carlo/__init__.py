from flask import Flask, session, request
from flask_cors import CORS
# from monte-carlo.lib.session_handler import ItsdangerousSessionInterface

app = Flask(__name__)
app.secret_key = 'this-is-a-secret-key'
#app.session_interface = ItsdangerousSessionInterface('app_user_session')

if app.debug:
    CORS(app, supports_credentials=True)


@app.before_request
def set_domain_session():
    app.SESSION_COOKIE_DOMAIN = request.headers['Host']


import monte_carlo.game_views
