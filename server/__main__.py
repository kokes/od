# TODO: docs, requirements
# TODO: expose bool arg
import argparse
import logging

from flask import Flask, abort, jsonify, render_template, request
from sqlalchemy import create_engine, text, func, column, collate
from sqlalchemy.orm import sessionmaker


class API(Flask):
    def __init__(self, import_name, connstring: str):
        super(API, self).__init__(import_name)
        self.engine = create_engine(connstring)
        self.sessionmaker = sessionmaker(bind=self.engine)

        self.table_schemas = {}
        from data.justice.schema import meta

        for table_name, table in meta.tables.items():
            table.name = "justice_" + table.name  # TODO: jen pro sqlite
            self.table_schemas[("justice", table_name)] = table

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
        session = self.sessionmaker()

        # TODO: neni tam zadne razeni
        # TODO: neni to kolace nad latin1_general_ci_ai (nejak mi nefungovala)
        # TODO: neni to indexovane
        tbl = self.table_schemas[("justice", "angazovane_osoby")]
        cols = {k: v for k, v in tbl.columns.items()}  # TODO: yikes
        query = (
            session.query(cols["jmeno"], cols["prijmeni"], cols["datum_narozeni"])
            .filter((column("jmeno") + " " + column("prijmeni")).contains(q))
            .group_by(column("jmeno"), column("prijmeni"), column("datum_narozeni"))
            .limit(100)
        )
        print(query)
        results = [
            {
                "jmeno": j.jmeno,
                "prijmeni": j.prijmeni,
                "datum_narozeni": j.datum_narozeni.isoformat()
                if j.datum_narozeni
                else None,
            }
            for j in query.all()
        ]

        return jsonify(result={"status": "ok", "results": results})


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
    app.json.ensure_ascii = False

    app.run(port=args.port, debug=args.debug)
