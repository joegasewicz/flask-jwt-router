"""
A testing server that runs in a thread for testing http requests
"""
from flask import Flask, request
import threading

app = Flask(__name__)

mock_exchange_response = {
    "access_token": "<access_token>",
    "expires_in": 3920,
    "token_type": "Bearer",
    "scope": "https://www.googleapis.com/auth/drive.metadata.readonly",
    "refresh_token": "<refresh_token>"
}


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shut_down', methods=['POST'])
def shutdown():
    shutdown_server()
    return {
        "message": "stopping server in thread",
    }


@app.route("/mock_google_exchange", methods=["GET", "POST"])
def mock_google_exchange():
    return mock_exchange_response


server_thread = threading.Thread(target=app.run, kwargs={"host": "localhost", "port": 5009})
