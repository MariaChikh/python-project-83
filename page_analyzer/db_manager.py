import psycopg2
from bs4 import BeautifulSoup
from psycopg2.extras import NamedTupleCursor
from requests import Response


def connect_db(app):
    return psycopg2.connect(app.config['DATABASE_URL'])


def close_connection(conn):
    conn.close()


def insert_url(conn, url: str):
    '''Inserts a new url in database'''

    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('''INSERT INTO urls (name, created_at)
                     VALUES (%s, CURRENT_DATE) RETURNING id;''', (url, ))
        result = curs.fetchone().id
        conn.commit()
    return result


def get_url_by_name(conn, url: str):
    '''Extracts an url from database by it's name'''

    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('''SELECT id, name, created_at
                     FROM urls WHERE name=%s;''', (url,))
        result = curs.fetchone()
    return result


def get_url_by_id(conn, url: str):
    '''Extracts an url from database by it's id'''
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('''SELECT id, name, created_at
                     FROM urls WHERE id=%s;''', (url,))
        result = curs.fetchone()
    return result


def get_urls(conn):
    '''Shows all urls added to database'''
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('''
                    SELECT urls.id, 
                    urls.name, 
                    MAX(checks.created_at) as last_check, 
                    MAX(checks.status_code) as last_status_code 
                    FROM urls
                    LEFT JOIN checks ON urls.id=checks.url_id
                    GROUP BY urls.id
                    ORDER BY urls.id;
                    ''')
        return curs.fetchall()
     

def insert_checks(conn, id: int, content: dict):
    '''Inserts url checks to database'''

    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('''
                     INSERT INTO checks 
                     (url_id, status_code, h1, title, description, created_at)
                     VALUES (%s, %s, %s, %s, %s, CURRENT_DATE) 
                     RETURNING url_id;''', (id, 
                                            content['status_code'],
                                            content['h1'],
                                            content['title'],
                                            content['description'],))
        result = curs.fetchone().url_id
        conn.commit()
    return result


def get_checks(conn, url_id: int):
    '''Shows all url's checks added to database'''
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT * from checks WHERE url_id=%s;', (url_id,))
        result = curs.fetchone()
    return result


def extract_page_data(url_response: Response):
    '''Extract the following page data from given url: 
    h1, title, status_code and description'''

    soup = BeautifulSoup(url_response.text, 'html.parser')
    h1_tag = soup.find('h1')
    title_tag = soup.find('title')
    description_tag = soup.find('meta', attrs={'name': 'description'})

    return {'h1': h1_tag.text[:255] if h1_tag else '',
            'title': title_tag.text[:255] if title_tag else '',
            'status_code': url_response.status_code,
            'description': (description_tag.get('content', '')[:255]
                            if description_tag else '')
    }
