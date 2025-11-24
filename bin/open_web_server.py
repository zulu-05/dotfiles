#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import socket

def find_free_port():
    """Finds an available port on the local machine."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def main():
    PORT = find_free_port()
    Handler = http.server.SimpleHTTPRequestHandler

    # Allow reusing addresses to prevent errors on quick restarts
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        host = "127.0.0.1"
        url = f"http://{host}:{PORT}"

        print("="*50)
        print(f"  Serving HTTP on http://{host}:{PORT}")
        print("  Press Ctrl+C to stop the server.")
        print("="*50)

        webbrowser.open(url)
        httpd.serve_forever()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped.")
