import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# Path to the file containing student marks
MARKS_FILE_PATH = Path("../data/q-vercel-python.json")

# Load the marks data from the file
def load_marks():
    if not MARKS_FILE_PATH.exists():
        raise FileNotFoundError(f"Marks file not found at {MARKS_FILE_PATH}")
    with open(MARKS_FILE_PATH, "r") as file:
        return json.load(file)

marks_data = load_marks()  # This is now a list of dictionaries

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        names = query_params.get("name", [])

        # Normalize names (strip whitespace, make case-insensitive)
        names = [name.strip() for name in names]

        # Fetch marks for the given names
        marks = []
        for name in names:
            # Search for the name in the list of dictionaries
            mark = next((item["marks"] for item in marks_data if item["name"] == name), None)
            marks.append(mark)

        # Prepare the response
        response = {"marks": marks}

        # Send the response
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))
        return

# # Start the HTTP server
# def run(server_class=HTTPServer, handler_class=handler, port=8000):
#     server_address = ("", port)
#     httpd = server_class(server_address, handler_class)
#     httpd.serve_forever()

# if __name__ == "__main__":
#     run()
