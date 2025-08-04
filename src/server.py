import json
import os
import pandas as pd
import webbrowser
from functools import wraps
from flask import request

import sys

import app as app
from flask import Flask, jsonify, render_template, request

import webview

project_root = os.path.abspath(os.path.dirname(__file__))

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    server = Flask(__name__, static_folder=project_root, template_folder=os.path.join(project_root,'..\\_internal\\assets\\gui\\'))
else:
    server = Flask(__name__, static_folder=project_root, template_folder=os.path.join(project_root,'..\\assets\\gui\\'))
server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1  # disable caching

log_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Format-Tool')
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, 'debug_log.txt')

def log_debug(msg):
    with open(log_path, "a", encoding="utf-8") as f:
      f.write(msg + "\n")
    pass
    
def verify_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data = request.get_json(force=True, silent=True) or {}
        token = data.get('token')
        if not token or token != webview.token:
            log_debug(f"Received token: {token}\nExpected token: {webview.token}\n")
            log_debug("Authentication error!\n")
            return {"error": "Authentication error"}, 401
        return f(*args, **kwargs)
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
    file_types = ('Spreadsheets (*.xls;*.xlsx;*.csv;*.xlsm)', 'All files (*.*)')
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
    data = request.get_json(force=True, silent=True) or {}
    print("Received data:", data)
    global format
    global convert_to
    convert_to = data.get('convert_to', [])
    format = data.get('formato')
    if format=='WALMART':
        save_folder =  webview.windows[0].create_file_dialog(webview.FOLDER_DIALOG, "Select Save Folder")
        app.WALMART_SAE(save_folder)
        response = {'status': 'ok', 'message': 'Conversion exitosa'}
    else:
        result = app.do_stuff(format)
    
        if result:  
            df = pd.DataFrame()
            print("Result:", result)
            df = result[1]
            response = {
                'status': 'ok', 
                'columns': df.columns.tolist(),
                'data': df.values.tolist()
            }
        else:
            response = {'status': 'error'}

    return jsonify(response)



@server.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    columns = data['columns']
    rows = data['data']
    df = pd.DataFrame(rows, columns=columns[1:])
    print("DataFrame to convert:", df.to_string())

    result = app.to_excel(df)
    dir = app.get_dir()
    print(dir)
    file_types = ('Excel file (*.xlsx)', 'All files (*.*)')
    SAE = ('Archivo SAE (*.MOD)', 'All files (*.*)')
    if format == 'SMART':
        if 'Concentrado' in convert_to:
            save = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG, directory=dir, save_filename='Concentrado.xlsx',file_types=file_types)
            app.replace_dummy(save,'data.xlsx')  # Replace the dummy file with the actual file
        if 'SAE' in convert_to:
            app.SMARTSAE()
            save1 = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG, directory=dir, save_filename='SAE.MOD',file_types=SAE)
            app.replace_dummy(save1,'temp.MOD')
    if format=='SORIANA':
        if 'Concentrado' in convert_to:
            save = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG, directory=dir, save_filename='Concentrado.xlsx',file_types=file_types)
            app.replace_dummy(save,'data1.xlsx')
        if 'Plantilla FIX' in convert_to:
            app.S1()
            save1 = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG, directory=dir, save_filename='Plantilla FIX.xlsx',file_types=file_types)
            app.replace_dummy(save1,'data3.xlsx')
        if 'Distribución Semanal' in convert_to:
            app.S2()
            save2 = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG, directory=dir, save_filename='Distribuciones Semanales.xlsx',file_types=file_types)
            print('FFFF')
            app.replace_dummy(save2,'data2.xlsx')
        if 'SAE' in convert_to:
            app.SORIANA_SAE()
            save3 = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG, directory=dir, save_filename='SAE.MOD',file_types=SAE)
            app.replace_dummy(save3,'temp.MOD')

    return jsonify({'result': 'success', 'output': save})