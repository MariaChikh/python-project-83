import requests
from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer import db_manager as db
from page_analyzer.parser import extract_page_data
from page_analyzer.utils import is_valid, normalize_url

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template(
        'index.html',
    )


@main_bp.route('/urls', methods=['POST'])
def add_url():
    url = request.form.to_dict()['url']

    if not is_valid(url):
        flash('Некорректный URL', 'danger')
        return render_template(
            'index.html',
            url=url,
        ), 422
    
    normalized_url = normalize_url(url)
    with db.get_db_connection() as conn:
        existed_url = db.get_url_by_name(conn, normalized_url)
        if existed_url:
            flash('Страница уже существует', 'warning')
            url_id = existed_url.id
        else:
            url_id = db.insert_url(conn, normalized_url)
            flash('Страница успешно добавлена', 'success')
    return redirect(url_for('main.show_url', id=url_id))


@main_bp.route('/urls/<int:id>', methods=['GET'])
def show_url(id: int):
    with db.get_db_connection() as conn:
        url = db.get_url_by_id(conn, id)
        checks = db.get_checks(conn, id)
    if not url:
        abort(404)
    return render_template('url.html', url=url, checks=checks)


@main_bp.route('/urls', methods=['GET'])
def show_urls():
    with db.get_db_connection() as conn:
        urls = db.get_urls(conn)
    return render_template('urls.html', urls=urls)


@main_bp.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id: int):
    with db.get_db_connection() as conn:
        url = db.get_url_by_id(conn, id)
        if not url:
            abort(404)
        try:
            response = requests.get(url.name)
            response.raise_for_status()
            url_info = extract_page_data(response)
            db.insert_checks(conn, id, url_info)
            flash('Страница успешно проверена', 'success')
        except requests.RequestException:
            flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('main.show_url', id=id))
