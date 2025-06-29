# TODO: docs
# TODO: expose bool arg
import json
import logging
import sqlite3
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


def make_handler_class(conn):
    # TODO: ThreadingHTTPServer? Nebude pak problem s sqlite,
    # ktera je pinovana na thread?
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
            with open("server/assets/index.html", "r", encoding="utf-8") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
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

            sql = """
            SELECT jmeno_prijmeni, datum_narozeni
            FROM justice_angazovane_osoby
            WHERE jmeno_prijmeni LIKE ?
            GROUP BY jmeno_prijmeni, datum_narozeni
            LIMIT 100
            """

            like_pattern = f"%{q.lower()}%"

            cursor = conn.execute(sql, (like_pattern,))
            rows = cursor.fetchall()

            results = []
            for row in rows:
                results.append(
                    {
                        "jmeno_prijmeni": row["jmeno_prijmeni"],
                        "datum_narozeni": row["datum_narozeni"],
                    }
                )

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"query": q, "results": results}).encode("utf-8")
            )

    return CustomHandler


def run_server(db_path, port):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    handler_class = make_handler_class(conn)

    httpd = HTTPServer(("localhost", port), handler_class)
    print(f"Serving on http://localhost:{port}")
    try:
        httpd.serve_forever()
    finally:
        conn.close()


def run_server_in_thread(db_path, port):
    httpd_container = {}

    def target():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        handler_class = make_handler_class(conn)

        httpd = HTTPServer(("localhost", port), handler_class)
        httpd_container["httpd"] = httpd
        httpd.serve_forever()
        conn.close()

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    while True:
        if "httpd" in httpd_container:
            break
        time.sleep(0.1)

    return httpd_container["httpd"], thread
