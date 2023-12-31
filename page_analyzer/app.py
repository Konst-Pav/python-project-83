from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from datetime import datetime
import page_analyzer.db as db
from page_analyzer.analyzer import url_check
from urllib.parse import urlparse
from dotenv import load_dotenv
from page_analyzer.validator import validate_url
import os


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', url='', messages=messages)


@app.route('/urls', methods=['GET', 'POST'])
def urls():
    url_from_user = request.form.get('url', '')
    url_from_user = url_from_user.lower()
    if request.method == 'POST':
        url_is_valid = validate_url(url_from_user)
        if not url_is_valid:
            flash('Некорректный URL', 'alert alert-danger')
            messages = get_flashed_messages(with_categories=True)
            return render_template('index.html', url=url_from_user, messages=messages), 422
        normalized_url = urlparse(url_from_user)
        name = f"{normalized_url.scheme}://{normalized_url.netloc}"
        url_already_in_db = db.get_data_by_url_name(name)
        if url_already_in_db:
            flash('Страница уже существует', 'alert alert-info')
            return redirect(url_for('get_url_page', id=url_already_in_db['id']))
        db.add_url(name)
        url_data = db.get_data_by_url_name(name)
        flash('Страница успешно добавлена', 'alert alert-success')
        return redirect(url_for('get_url_page', id=url_data.get('id')))
    else:
        messages = get_flashed_messages(with_categories=True)
        urls_data = db.get_urls_data()
        for url in urls_data:
            if url.get('created_at'):
                url['created_at'] = datetime.date(url['created_at'])
        return render_template('urls.html', urls=urls_data, messages=messages)


@app.route('/urls/<int:id>')
def get_url_page(id):
    url_data = db.get_data_by_url_id(id)
    if not url_data:
        return render_template('error/404.html'), 404
    url_data['created_at'] = datetime.date(url_data.get('created_at', ''))
    urls_check_list = db.get_url_checks_by_url_id(id)
    for url in urls_check_list:
        url['created_at'] = datetime.date(url.get('created_at', ''))
    messages = get_flashed_messages(with_categories=True)
    return render_template('url_page.html', messages=messages, url=url_data, urls_check_list=urls_check_list)


@app.post('/urls/<int:id>/checks')
def post_url_check(id):
    url = db.get_data_by_url_id(id).get('name')
    url_data = url_check(url)
    if url_data:
        status_code = url_data.get('status_code')
        h1 = url_data.get('h1', '')
        title = url_data.get('title', '')
        description = url_data.get('description', '')
        db.add_url_check(id, status_code=status_code, h1=h1, title=title, description=description)
        flash('Страница успешно проверена', 'alert alert-success')
        return redirect(url_for('get_url_page', id=id))
    flash('Произошла ошибка при проверке', 'alert alert-danger')
    return redirect(url_for('get_url_page', id=id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('error/500.html'), 500
