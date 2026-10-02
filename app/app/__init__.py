import os

from flask import flash
from flask import Flask
from flask import render_template
from flask import request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

if config_dir := os.environ.get('CONFIGURATION_DIRECTORY'):
    app.config.from_pyfile(f"{config_dir}/config.py")
    app.wsgi_app = ProxyFix(app.wsgi_app)
else:
    app.config.update(SECRET_KEY='secret')


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None

    if request.method == 'POST':
        if maybe_name := request.form.get('name', '').strip():
            name = maybe_name
        else:
            flash("You must provide a name!", 'error')

    return render_template('index.html', name=name)
