#!/usr/bin/env python3
""" Flask application
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def root_path():
    """ Root path for Flask application
    """
    return jsonify({
        "message": "Bienvenue"
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")  # type: ignore
