import argparse
import logging

from .api import run_server

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port", type=int, default=3000, help="HTTP port to host this on"
    )
    parser.add_argument(
        "--db",
        required=True,
        type=str,
        help="cesta k sqlite db",
    )
    args = parser.parse_args()

    run_server(args.db, args.port)
