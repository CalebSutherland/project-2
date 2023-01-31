"""
John Doe's Flask API.
"""

from flask import Flask, abort, send_from_directory

import os
import configparser

# configuration parser from project 0
def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

config = parse_config(["credentials.ini", "default.ini"])
debug = config["SERVER"]["DEBUG"]
port = config["SERVER"]["PORT"]

app = Flask(__name__)

@app.route("/<path:request>")
def hello(request):
    path = './pages/' + request

    if ".." in path or "~" in path:
        abort(403)

    if os.path.isfile(path):
        return send_from_directory('pages/', request), 200
    else:
        abort(404)

@app.errorhandler(403)
def forbidden(e):
    return send_from_directory('pages/', '403.html'), 403

@app.errorhandler(404)
def forbidden(e):
    return send_from_directory('pages/', '404.html'), 403


if __name__ == "__main__":
    app.run(debug=debug, host='0.0.0.0', port=port)
