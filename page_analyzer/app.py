from flask import Flask, render_template, request, redirect, url_for, flash, abort
import requests
import os
from datetime import datetime
from page_analyzer import db_manager as db
from page_analyzer.utils import is_valid, normalize_url
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template(
        'index.html',
    )

@app.route('/urls', methods = ['POST'])
def add_url():
    url = request.form.to_dict()['url']

    if not is_valid(url):
        flash('Некорректный URL', 'danger')
        return render_template(
            'index.html',
            url=url,
        ), 422
    
    normalized_url = normalize_url(url)
    conn = db.connect_db(app)
    existed_url = db.get_url_by_name(conn, normalized_url)
    if existed_url:
        flash('Страница уже существует', 'warning')
        url_id = existed_url.id
    else:
        url_id = db.insert_url(conn, normalized_url)
        flash('Страница успешно добавлена', 'success')
    db.close_connection(conn)
    return redirect(url_for('show_url', id=url_id))


@app.route('/urls/<int:id>', methods = ['GET'])
def show_url(id):
    conn = db.connect_db(app)
    url = db.get_url_by_id(conn, id)
    if not url:
        abort(404)
    db.close_connection(conn)
    return render_template('url.html', url=url)


@app.route('/urls', methods = ['GET'])
def show_urls():
    conn = db.connect_db(app)
    urls = db.get_urls(conn)
    db.close_connection(conn)
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>/checks', methods = ['POST'])
def check_url(id):
    conn = db.connect_db(app)
    url = db.get_url_by_id(conn, id)
    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        db.close_connection(conn)
        #return redirect(url_for('show_url', id=id))
    flash('Страница успешно проверена', 'success')
    db.close_connection
    return redirect(url_for('show_url', id=id))


if __name__ == 'main':
    index()