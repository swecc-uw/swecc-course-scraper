import http.server
import socketserver
import json

PORT=8000

def command(json_path: str):
    """
    Initializes a local HTTP server that serves the content of a JSON file at /data

    Args:
        json_path (str): The path to a JSON file to be served

    Returns:
        None

    Raises:
    FileNotFoundError: If the given JSON file does not exist
    ValueError: If the file is not in valid JSON format
    OSError: If the server fails to bind to the specified port
    """
    class JSONDataHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/data":
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        response = json.dumps(data).encode("utf-8")
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.send_header("Content-Length", str(len(response)))
                        self.end_headers()
                        self.wfile.write(response)
                except FileNotFoundError:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"File not found")
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(f"Server error: {str(e)}".encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not found")

    with socketserver.TCPServer(("", PORT), JSONDataHandler) as httpd:
        print("Serving at port", PORT)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down...")
        finally:
            httpd.server_close()
