import pytest
import psycopg2
from psycopg2.extras import DictCursor, RealDictCursor
import page_analyzer.db as db
from dotenv import dotenv_values


config = dotenv_values('.env')
CONNECTION_URI = config['CONNECTION_URI']


@pytest.mark.parametrize('url, expected_result', [
    ('https://test', 'https://test')
])
def test_add_url(url, expected_result):
    db.add_url(url)
    with psycopg2.connect(CONNECTION_URI) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute("SELECT name FROM urls WHERE name = %s LIMIT 1;", (url,))
            result = curs.fetchone()
            curs.execute("DELETE FROM urls WHERE name = %s;", (url,))
    assert result['name'] == expected_result


@pytest.mark.parametrize('url_name', [
    'https://test'
])
def test_get_data_by_url_name(url_name):
    with psycopg2.connect(CONNECTION_URI) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute("INSERT INTO urls (name) VALUES (%s);", (url_name, ))
            conn.commit()
            result = db.get_data_by_url_name(url_name)
            curs.execute("DELETE FROM urls WHERE name = %s;", (url_name, ))
    assert result['name'] == url_name


@pytest.mark.parametrize('url_name', [
    'https://test'
])
def test_get_data_by_url_id(url_name):
    with psycopg2.connect(CONNECTION_URI) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute("INSERT INTO urls (name) VALUES (%s);", (url_name, ))
            conn.commit()
            curs.execute("SELECT id FROM urls WHERE name = %s;", (url_name, ))
            url_data = curs.fetchone()
            result = db.get_data_by_url_id(url_data['id'])
            assert result['name'] == url_name
            curs.execute("DELETE FROM urls WHERE id = %s", (url_data['id'], ))


@pytest.mark.parametrize('url_id, status_code, h1, title, description', [
    (-1, 777, 'h1', 'title', 'description')
])
def test_add_url_check(url_id, status_code, h1, title, description):
    db.add_url_check(url_id, status_code=status_code, h1=h1, title=title, description=description)
    with psycopg2.connect(CONNECTION_URI) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute("""
            SELECT url_id, status_code, h1, title, description 
            FROM url_checks;
            """, (url_id, ))
            result = curs.fetchone()
            expected_result = {
                'url_id': url_id,
                'status_code': status_code,
                'h1': h1,
                'title': title,
                'description': description
            }
            curs.execute("""
                        DELETE FROM url_checks
                        WHERE url_id = %s AND status_code = %s AND h1 = %s AND title = %s AND description = %s;
                        """, (url_id, status_code, h1, title, description))
            assert result == expected_result
