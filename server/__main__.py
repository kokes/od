# TODO: docs, requirements
# TODO: expose bool arg
import argparse
import logging

from flask import Flask, abort, jsonify, render_template, request
from sqlalchemy import create_engine, text


class API(Flask):
    def __init__(self, import_name, connstring: str):
        super(API, self).__init__(import_name)
        self.engine = create_engine(connstring)

        self.route("/", methods=["GET"])(self.index)
        self.route("/status", methods=["GET"])(self.status)
        self.route("/api/search", methods=["GET"])(self.search)
        # self.route("/api/datasets", methods=["GET"])(self.datasets)

    def status(self):
        return jsonify({"status": "ok"})

    def index(self):
        return render_template("index.j2")

    def search(self):
        q = request.args.get("q")
        if not q:
            abort(400, "missing query parameter 'q'")

        results = []
        with self.engine.begin() as conn:
            cursor = conn.execute(text("SELECT 1"))
            results = [str(j) for j in cursor.fetchall()]

        return jsonify({"status": "ok", "results": results})


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable debug mode in Flask (autoreload, exception handling)",
    )
    parser.add_argument(
        "--port", type=int, default=3000, help="HTTP port to host this on"
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

    app = API(__name__, connstring=args.connstring)

    app.run(port=args.port, debug=args.debug)
