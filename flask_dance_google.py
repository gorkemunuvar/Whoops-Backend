""" from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

# change them all to google
GOOGLE_APP_ID = '167345546409-et21u2i0r2cksg5avc563bjrd8ptvj60.apps.googleusercontent.com'
GOOGLE_APP_SECRET = 'o0oscaAYrGPPbASVNLcHrSqc'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissupposedtobeasecret'

google_blueprint = make_google_blueprint(
    api_key=GOOGLE_APP_ID,
    api_secret=GOOGLE_APP_SECRET,
)


app.register_blueprint(google_blueprint, url_prefix='/login')


@app.route('/google')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))

    account_info = google.get('userinfo')
    account_info_json = account_info.json()

    return '<h1>Your google name is @{}'.format(account_info_json['email'])


if __name__ == '__main__':
    app.run(debug=True)
 """

from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

# Somewhere in webapp_example.py, before the app.run for example
import os

GOOGLE_APP_ID = '167345546409-et21u2i0r2cksg5avc563bjrd8ptvj60.apps.googleusercontent.com'
GOOGLE_APP_SECRET = 'o0oscaAYrGPPbASVNLcHrSqc'


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = "supersekrit"
blueprint = make_google_blueprint(
    client_id=GOOGLE_APP_ID,
    client_secret=GOOGLE_APP_SECRET,
    scope=['https://www.googleapis.com/auth/userinfo.email']
)

app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text

    print(str(resp))
    # return "You are {email} on Google".format(email=resp.json()["emails"][0]["value"])


@app.route("/login/google/authorized")
def google_authorized():
    resp = google.get("/plus/v1/people/me")

    print(resp)


if __name__ == "__main__":
    app.run()
