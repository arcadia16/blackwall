from flask import render_template
from blackwall_server import app


@app.route('/')
def index():
    return render_template('index.html', agents=[1, 2, 3, 4])
