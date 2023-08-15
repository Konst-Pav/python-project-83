import psycopg2
from datetime import datetime
import yaml
from yaml.loader import SafeLoader
from dotenv import dotenv_values


config = dotenv_values('.env')
CONNECTION_URI = config['CONNECTION_URI']


def add_url(url):
    conn = psycopg2.connect(CONNECTION_URI)
    cur = conn.cursor()
    cur.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s);", (url, datetime.now()))
    conn.commit()
    cur.close()
    conn.close()


def get_url_by_name(url):
    conn = psycopg2.connect(CONNECTION_URI)
    cur = conn.cursor()
    cur.execute("SELECT id, name, created_at FROM urls WHERE name = %s LIMIT 1;", (url, ))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        return {'id': result[0], 'name': result[1], 'created_at': result[2]}
    return result


def get_url_by_id(id):
    conn = psycopg2.connect(CONNECTION_URI)
    cur = conn.cursor()
    cur.execute("SELECT id, name, created_at FROM urls WHERE id = %s;", (id, ))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        return {'id': result[0], 'name': result[1], 'created_at': result[2]}
    return result


def get_all_urls():
    conn = psycopg2.connect(CONNECTION_URI)
    cur = conn.cursor()
    cur.execute("SELECT id, name, created_at FROM urls;")
    result = cur.fetchall()
    cur.close()
    conn.close()
    if result:
        urls = []
        for item in result:
            urls.append({'id': item[0], 'name': item[1], 'created_at': item[2]})
        return urls
    return result


def add_url_check(url_id, status_code=None, h1='', title='', description=''):
    conn = psycopg2.connect(CONNECTION_URI)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)
        VALUES (%s, %s, %s, %s, %s, %s);
        """, (url_id, status_code, h1, title, description, datetime.now())
        )
    conn.commit()
    cur.close()
    conn.close()


def get_all_urls_check_by_id(id):
    conn = psycopg2.connect(CONNECTION_URI)
    cur = conn.cursor()
    cur.execute("SELECT id, status_code, h1, title, description, created_at FROM url_checks WHERE url_id = %s;", (id,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    if result:
        url_checks = []
        for item in result:
            url_checks.append(
                {
                    'id': item[0],
                    'status_code': item[1],
                    'h1': item[2],
                    'title': item[3],
                    'description': item[4],
                    'created_at': item[5]
                })
        return url_checks
    return result


def get_urls():
    conn = psycopg2.connect(CONNECTION_URI)
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT ON (urls.id) urls.id, urls.name, url_checks.status_code, url_checks.created_at 
        FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id
        ORDER BY urls.id, url_checks.created_at DESC;
        """)
    result = cur.fetchall()
    cur.close()
    conn.close()
    if result:
        urls_with_checks = []
        for item in result:
            id = item[0]
            name = item[1]
            status_code = item[2] if item[2] else ''
            created_at = item[3] if item[3] else ''
            urls_with_checks.append({'id': id, 'name': name, 'status_code': status_code, 'created_at': created_at})
        return urls_with_checks
    return result
