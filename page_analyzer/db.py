import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
from dotenv import dotenv_values
from dotenv import load_dotenv


load_dotenv()
config = dotenv_values('.env')
DATABASE_URL = config['DATABASE_URL']


def add_url(url):
    sql_query = "INSERT INTO urls (name, created_at) VALUES (%s, %s);"
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            curs.execute(sql_query, (url, datetime.now()))


def get_data_by_url_name(url_name):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute("SELECT id, name, created_at FROM urls WHERE name = %s LIMIT 1;", (url_name,))
            result = curs.fetchone()
    return result


def get_data_by_url_id(url_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute("SELECT id, name, created_at FROM urls WHERE id = %s;", (url_id,))
            result = curs.fetchone()
    return result


def get_all_urls_data():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute("SELECT id, name, created_at FROM urls;")
            result = curs.fetchall()
    return result


def add_url_check(url_id, status_code=None, h1='', title='', description=''):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            curs.execute("""
                INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s);
                """, (url_id, status_code, h1, title, description, datetime.now()))


def get_url_checks_by_url_id(url_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute("""
                SELECT id, status_code, h1, title, description, created_at FROM url_checks WHERE url_id = %s;
                """, (url_id,))
            result = curs.fetchall()
    return result


def get_urls_data():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute("""
                SELECT DISTINCT ON (urls.id)
                urls.id AS id,
                urls.name AS name,
                url_checks.status_code AS status_code,
                url_checks.created_at AS created_at
                FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id
                ORDER BY urls.id, url_checks.created_at DESC;
                """)
            result = curs.fetchall()
    return result
