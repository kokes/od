# TODO: docs, requirements
import argparse
import logging
from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine

def status():
    return jsonify({"status": "ok"})

def index():
    return render_template("index.j2")

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable debug mode in Flask (autoreload, exception handling)",
    )
    parser.add_argument(
        "--connstring",
        required=True,
        type=str,
        help="connection string pro databazi tve volby",
    )
    parser.add_argument(
        "--schema_prefix",
        type=str,
        default="",
        help="prefix pro nazvy schemat (postgres) ci tabulek (sqlite)",
    )
    args = parser.parse_args()

    engine = create_engine(args.connstring)
    logging.info("connected to %s", engine)

    app = Flask(__name__)

    app.add_url_rule("/status", 'status', status)
    app.add_url_rule("/", 'index', index)

    app.run(port=3000, debug=args.debug)
