from flask import render_template
from application import app
from .account import abort_not_confirmed
from flask_login import login_required


@app.route('/')
@login_required
@abort_not_confirmed
def home():
    # Your home logic goes here
    return render_template('general/index.html', page_title='Home')
