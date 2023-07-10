from flask import (
    Flask,
    flash,
    get_flashed_messages,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from validators.url import url as validate_url
import psycopg2


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def post_urls():
    return redirect(url_for(''))


@app.route('/urls/<id>')
def get_url(id):
    return render_template('url_page.html')
