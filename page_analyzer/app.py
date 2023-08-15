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
from datetime import datetime
import yaml
from yaml.loader import SafeLoader
import page_analyzer.db as db
from page_analyzer.analyzer import url_check
from urllib.parse import urlparse

cfg = yaml.load(open("config.yml"), Loader=SafeLoader)
SECRET_KEY = cfg.get('secret_key')


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', url='', messages=messages)


@app.route('/urls', methods=['GET', 'POST'])
def post_urls():
    url_from_user = request.form.get('url', '')
    url_from_user = url_from_user.lower()
    if request.method == 'POST':
        url_is_valid = validate_url(url_from_user) and len(url_from_user) <= 255
        if not url_is_valid:
            flash('Некорректный URL', 'alert alert-danger')
            return redirect(url_for('index'))
        normalized_url = urlparse(url_from_user)
        name = f"{normalized_url.scheme}://{normalized_url.netloc}"
        url_already_in_db = db.get_url_by_name(name)
        if url_already_in_db:
            flash('Страница уже существует', 'alert alert-info')
            return redirect(url_for('get_url', id=url_already_in_db['id']))
        db.add_url(name)
        url_data = db.get_url_by_name(name)
        flash('Страница успешно добавлена', 'alert alert-success')
        return redirect(url_for('get_url', id=url_data.get('id')))
    else:
        messages = get_flashed_messages(with_categories=True)
        urls = db.get_urls()
        for url in urls:
            if url.get('created_at'):
                url['created_at'] = datetime.date(url['created_at'])
        return render_template('urls.html', urls=urls, messages=messages)


@app.route('/urls/<int:id>')
def get_url(id):
    url_data = db.get_url_by_id(id)
    url_data['created_at'] = datetime.date(url_data.get('created_at', ''))
    urls_check_list = db.get_all_urls_check_by_id(id)
    for url in urls_check_list:
        url['created_at'] = datetime.date(url.get('created_at', ''))
    messages = get_flashed_messages(with_categories=True)
    return render_template('url_page.html', messages=messages, url=url_data, urls_check_list=urls_check_list)


@app.post('/urls/<int:id>/checks')
def post_url_check(id):
    url = db.get_url_by_id(id).get('name')
    url_data = url_check(url)
    if url_data:
        status_code = url_data.get('status_code')
        h1 = url_data.get('h1', '')
        title = url_data.get('title', '')
        description = url_data.get('description', '')
        db.add_url_check(id, status_code=status_code, h1=h1, title=title, description=description)
        flash('Страница успешно проверена', 'alert alert-success')
        return redirect(url_for('get_url', id=id))
    flash('Произошла ошибка при проверке', 'alert alert-danger')
    return redirect(url_for('get_url', id=id))
