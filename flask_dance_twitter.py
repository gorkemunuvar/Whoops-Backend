from flask import Flask, redirect, url_for
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

TWITTER_APP_ID = '6D2OVkNHpJmHFf3OnCPGL6sv3'
TWITTER_APP_SECRET = 'BIQ7CUSu9JDo0xUIs4QwOoGvRCNm1UBo8V4FfrpbSBU0HaNcRl'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissupposedtobeasecret'

twitter_blueprint = make_twitter_blueprint(
    api_key=TWITTER_APP_ID,
    api_secret=TWITTER_APP_SECRET,
)


app.register_blueprint(twitter_blueprint, url_prefix='/login')


@app.route('/twitter')
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))

    account_info = twitter.get('account/settings.json')
    account_info_json = account_info.json()

    print(account_info_json)

    return '<h1>Your Twitter name is @{}'.format(account_info_json['screen_name'])


if __name__ == '__main__':
    app.run(debug=True)
