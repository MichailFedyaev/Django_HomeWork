import http.server
import socketserver
import urllib.parse
import os

PORT = 8000

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"Получен гэт-запрос на {self.path}")
        if self.path == '/':
            self.path = '../html/contacts.html'

        file_path = os.path.join(os.path.dirname(__file__), self.path[1:])

        try:
            with open(self.path[1:], 'rb') as file:
                content = file.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "файлик не найден!: %s" % self.path)

    def do_POST(self):
        print("получены пост-данные")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data_str = post_data.decode('utf-8')
        post_data_dict = urllib.parse.parse_qs(post_data_str)

        print("получены пост-данные:")
        for key, value in post_data_dict.items():
            print(f"{key}: {value}")

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"POST request received")

Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("сервак стартанул на порте:", PORT)
    httpd.serve_forever()