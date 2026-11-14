import http.server
import os
import socket
import socketserver
import sys
import webbrowser

PORT_START = 8765
ROOT = os.path.dirname(os.path.abspath(__file__))


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".webmanifest": "application/manifest+json",
        ".js": "text/javascript",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, format, *args):
        print(f"{self.address_string()} {format % args}")


def lan_address():
    """Find this computer's address on the home network, if it has one."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return ""
    finally:
        sock.close()


def main():
    for port in range(PORT_START, PORT_START + 10):
        try:
            server = socketserver.ThreadingTCPServer(("0.0.0.0", port), QuietHandler)
        except OSError:
            continue
        url = f"http://127.0.0.1:{port}"
        print(f"Trivia is running at {url}", flush=True)
        phone = lan_address()
        if phone:
            print(f"On your phone, open http://{phone}:{port}", flush=True)
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
