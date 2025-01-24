import psycopg2
from psycopg2.extras import NamedTupleCursor
from datetime import datetime


def connect_db(app):
    return psycopg2.connect('postgresql://maria:password123@localhost:5432/page_analyzer')


def close_connection(conn):
    conn.close()


def insert_url(conn, url):
    with conn.cursor(cursor_factory = NamedTupleCursor) as curs:
            curs.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;', (url, datetime.now()))
            result = curs.fetchone().id
            conn.commit()
    return result


def get_url_by_name(conn, url):
    with conn.cursor(cursor_factory = NamedTupleCursor) as curs:
          curs.execute('SELECT id, name, created_at FROM urls WHERE name=%s;', (url,))
          result = curs.fetchone()
    return result


def get_url_by_id(conn, url):
    with conn.cursor(cursor_factory = NamedTupleCursor) as curs:
          curs.execute('SELECT id, name, created_at FROM urls WHERE id=%s;', (url,))
          result = curs.fetchone()
    return result


def get_urls(conn):
     with conn.cursor(cursor_factory = NamedTupleCursor) as curs:
          curs.execute('SELECT * FROM urls ORDER BY urls.id;')
          return curs.fetchall()