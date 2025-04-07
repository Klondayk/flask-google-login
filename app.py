from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "QWESRDTFYUIKJHGTFRAWqswdfghjkhgfdsadfg")


oauth = OAuth(app)
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url=CONF_URL,
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/')
def index():
    return '<a href="/login">Войти через Google</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    user = google.get('userinfo').json()
    name = user.get('name')
    email = user.get('email')

    # Редирект на Tilda с параметрами
    return redirect(f"http://hta.store.tilda.ws/?name={name}&email={email}")

if __name__ == "__main__":
    app.run()
