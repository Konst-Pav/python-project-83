import psycopg2
from datetime import datetime
import yaml
from yaml.loader import SafeLoader

cfg = yaml.load(open("config.yml"), Loader=SafeLoader)
DB_NAME = cfg.get('db_name')
USER = cfg.get('user')


def get_urls():
    with psycopg2.connect(f"dbname={DB_NAME} user={USER}") as conn:
        with conn.cursor as curs:
            curs.execute('SELECT * FROM urls;')
            f_all = curs.fetchall()
            f_one = curs.fetchone()
            print(f'fetchall = {f_all}')
            print(f'fetchall = {f_one}')
