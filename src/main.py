import logging
from contextlib import redirect_stdout
from io import StringIO
import threading
import time

import notpywinsparkle
from server import server
from sparkle_thread import sparkle

import webview
import webview.menu as wm

logger = logging.getLogger(__name__)

def run_flask():
    server.run(host='127.0.0.1', port=5000, threaded=True, use_reloader=False,debug=True)

if __name__ == '__main__':
    #stream = StringIO()
    #with redirect_stdout(stream):
        sparkle_thread = threading.Thread(target=sparkle, daemon=True)
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        sparkle_thread.start()
        time.sleep(1)  # Wait for Flask to start

        menu = [
            wm.Menu(
                'Menu',
                [wm.MenuAction('Buscar actualizaciones...', notpywinsparkle.win_sparkle_check_update_with_ui)]
            )
            ]

        webview.settings['ALLOW_DOWNLOADS'] = True
        window = webview.create_window('Herramienta', 'http://127.0.0.1:5000/')
        webview.start(menu=menu)