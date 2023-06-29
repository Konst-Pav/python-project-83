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


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
