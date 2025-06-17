import json
import os
import webbrowser
from functools import wraps

import app
from flask import Flask, jsonify, render_template, request

import webview

project_root = os.path.abspath(os.path.dirname(__file__))

server = Flask(__name__, static_folder=project_root, template_folder=project_root)
server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1  # disable caching


def verify_token(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        data = json.loads(request.data)
        token = data.get('token')
        if token == webview.token:
            return function(*args, **kwargs)
        else:
            raise Exception('Authentication error')

    return wrapper


@server.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


@server.route('/')
def landing():
    """
    Render index.html. Initialization is performed asynchronously in initialize() function
    """
    print("Landing route called")
    print("webview.token:", webview.token)

    return render_template('index.html', token=webview.token)


@server.route('/init', methods=['POST'])
@verify_token
def initialize():
    """
    Perform heavy-lifting initialization asynchronously.
    :return:
    """
    can_start = app.initialize()

    if can_start:
        response = {
            'status': 'ok',
        }
    else:
        response = {'status': 'error'}

    return jsonify(response)


@server.route('/choose/path', methods=['POST'])
@verify_token
def choose_path():
    """
    Invoke a folder selection dialog here
    :return:
    """
    file_types = ('Spreadsheets (*.xls;*.xlsx;*.csv)', 'All files (*.*)')
    dirs = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG,allow_multiple=True, file_types=file_types)
    app.load_dir(dirs[0])  # Save the directory for later use

    if dirs and len(dirs) > 0:
        directory = dirs[0]
        if isinstance(directory, bytes):
            directory = directory.decode('utf-8')

        response = {'status': 'ok', 'directory': directory}
    else:
        response = {'status': 'cancel'}

    return jsonify(response)


@server.route('/fullscreen', methods=['POST'])
@verify_token
def fullscreen():
    webview.windows[0].toggle_fullscreen()
    return jsonify({})


@server.route('/open-url', methods=['POST'])
@verify_token
def open_url():
    url = request.json['url']
    webbrowser.open_new_tab(url)

    return jsonify({})


@server.route('/do/stuff', methods=['POST'])
@verify_token
def do_stuff():
    result = app.do_stuff()
    file_types = ('Excel file (*.xlsx)', 'All files (*.*)')
    save = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG, directory=result[2], save_filename='output.xlsx',file_types=file_types)
    app.replace_dummy(save)  # Replace the dummy file with the actual file
    if result:
        response = {'status': 'ok', 'result': result[0]}
    else:
        response = {'status': 'error'}

    return jsonify(response)