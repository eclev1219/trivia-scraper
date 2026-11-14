import http.server
import os
import socketserver
import sys
import webbrowser

PORT_START = 8765
ROOT = os.path.dirname(os.path.abspath(__file__))


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, format, *args):
        print(f"{self.address_string()} {format % args}")


def main():
    for port in range(PORT_START, PORT_START + 10):
        try:
            server = socketserver.ThreadingTCPServer(("127.0.0.1", port), QuietHandler)
        except OSError:
            continue
        url = f"http://127.0.0.1:{port}"
        print(f"Trivia is running at {url}", flush=True)
        print("Leave this window open while you play. Press Ctrl+C to stop.", flush=True)
        if "--no-browser" not in sys.argv:
            webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
        finally:
            server.server_close()
        return

    raise SystemExit("Could not find a free port starting at 8765.")


if __name__ == "__main__":
    main()
