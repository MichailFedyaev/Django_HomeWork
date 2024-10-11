from http.server import BaseHTTPRequestHandler, HTTPServer


# Настройки запуска
hostName = "localhost" # Адрес
serverPort = 8080 # Порт


class MyServer(BaseHTTPRequestHandler):
    """Класс, который отвечает за обработку входящих запросов от клиентов"""

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """

        print(f"Получен GET-запрос {self.path}") # Печать в консоль

        path = self.path

        if path == "/css/bootstrap.min.css":
            path = "../css/bootstrap.min.css"
            type_header = "text/css"
        elif path == "/js/bootstrap.bundle.min.js":
            path = "../js/bootstrap.bundle.min.js"
            type_header = "text/javascript"

        else:
            path = self.path.replace("/", "")
            path = "../html/contacts.html"
            type_header = "text/html"

        self.send_response(200)
        self.send_header("Content-type", type_header) # Отправка типа данных, который будет передаваться
        self.end_headers()
        with open(path,encoding="utf-8") as file:
            content = file.read()
            self.wfile.write(bytes(content, "utf-8")) # Тело ответа

    def do_POST(self):
        """ Метод для отправки информации на сервер POST-запросов """

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        response = f"Получены POST-данные: {post_data.decode('utf-8')}"
        print(response)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(response, "utf-8"))


if __name__ == "__main__":
    # Инициализация веб-сервера который будет принимать запросы и отправлять их на обработку
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Старт сервера: http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Ctrl + C
        pass

    # Корректная остановка веб-сервера
    webServer.server_close()
    print("Сервер стоп!")