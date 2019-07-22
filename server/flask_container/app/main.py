#!/usr/bin/env python
from flask import Flask, render_template
from json2html import json2html
import time
import db_handler

# Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/current_info')
def get_data():
    results = db_handler.get_all()
    return json2html.convert(json=results, encode=True, escape=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
