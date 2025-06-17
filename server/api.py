# TODO: docs
# TODO: expose bool arg
import json
import logging
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


def make_handler_class(db_connection):
    # TODO: ThreadingHTTPServer? Nebude pak problem s sqlite, ktera je pinovana na thread?
    class CustomHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed_path = urlparse(self.path)
            route = parsed_path.path

            try:
                if route == "/":
                    self.index()
                elif route == "/status":
                    self.status()
                elif route == "/api/search":
                    self.search(parsed_path.query)
                else:
                    self.send_error(404, "Not Found")
            except Exception as e:
                logging.error("oops: %s", e)
                self.send_error(500, "oops")

        def index(self):
            with open("server/templates/index.j2", "r", encoding="utf-8") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))

        def status(self):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))

        def search(self, query_string):
            query = parse_qs(query_string)
            q = query.get("q", [None])[0]
            if not q:
                self.send_error(400, "Missing query parameter 'q'")
                return

            # Reuse injected connection
            cursor = db_connection.cursor()
            # Example query
            cursor.execute("SELECT ? as result", (q,))
            rows = [row[0] for row in cursor.fetchall()]

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"query": q, "results": rows}).encode("utf-8"))

    return CustomHandler

    # TODO: neni tam zadne razeni
    # TODO: neni to kolace nad latin1_general_ci_ai (nejak mi nefungovala)
    # TODO: neni to indexovane (na sqlite mi to nechce chytit index na computed sloupec)
    # tbl = self.table_schemas[("justice", "angazovane_osoby")]
    # cols = {k: v for k, v in tbl.columns.items()}  # TODO: yikes
    # query = (
    #     session.query(cols["jmeno"], cols["prijmeni"], cols["datum_narozeni"])
    #     .filter(
    #         func.lower((column("jmeno") + " " + column("prijmeni"))).contains(q)
    #     )
    #     .group_by(column("jmeno"), column("prijmeni"), column("datum_narozeni"))
    #     .limit(100)
    # )
    # print(query)
    # results = [
    #     {
    #         "jmeno": j.jmeno,
    #         "prijmeni": j.prijmeni,
    #         "datum_narozeni": j.datum_narozeni.isoformat()
    #         if j.datum_narozeni
    #         else None,
    #     }
    #     for j in query.all()
    # ]

    # return jsonify(result={"status": "ok", "results": results})


def run_server(db_path, port):
    conn = sqlite3.connect(db_path)
    handler_class = make_handler_class(conn)

    httpd = HTTPServer(("localhost", port), handler_class)
    print(f"Serving on http://localhost:{port}")
    try:
        httpd.serve_forever()
    finally:
        conn.close()
