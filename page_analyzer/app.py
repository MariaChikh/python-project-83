from flask import Flask

from page_analyzer.blueprints.main import main_bp
from page_analyzer.settings import DATABASE_URL, SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DATABASE_URL'] = DATABASE_URL
app.register_blueprint(main_bp)

if __name__ == 'main':
    app.run(debug=True)