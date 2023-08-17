import http.server
import socketserver
import os

# Set the IP address and port for the server
host = "127.0.0.1"
port = 8008

# Specify the directory you want to serve files from
directory_to_serve = "./.data"


# Create a custom request handler that serves files from the specified directory
class CustomRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=directory_to_serve, **kwargs)


# Create a socket server with the specified address and custom handler
with socketserver.TCPServer((host, port), CustomRequestHandler) as server:
    print(f"Serving at http://{host}:{port} from {directory_to_serve}")
    # Start the server and keep it running until interrupted
    server.serve_forever()
