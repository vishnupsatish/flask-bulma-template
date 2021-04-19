from application import app
from flask import render_template


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', page_title='404 - Not Found'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html', page_title='500 - Internal Server Error'), 500


@app.errorhandler(429)
def too_many_request(e):
    return render_template('errors/429.html', page_title='429 - Too Many Requests'), 429
