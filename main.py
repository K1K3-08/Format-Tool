import logging
from contextlib import redirect_stdout
from io import StringIO
import threading
import time

from server import server

import webview

logger = logging.getLogger(__name__)



def run_flask():
    server.run(host='127.0.0.1', port=5000, threaded=True, use_reloader=False,debug=True)

if __name__ == '__main__':
    stream = StringIO()
    with redirect_stdout(stream):

        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

        time.sleep(1)  # Wait for Flask to start

        webview.settings['ALLOW_DOWNLOADS'] = True
        window = webview.create_window('My first pywebview application', 'http://127.0.0.1:5000/')
        webview.start()