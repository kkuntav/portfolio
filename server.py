import socket
import os

from entity.entity import main as entity


class Server:
    def __init__(self, port: int) -> None:
        self.port = port



    def run(self) -> None:
        """

        Runs the server loop:
        Creates a socket, and then, in an infinite loop,
        waits for requests and processes them.

        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(("0.0.0.0", self.port))
        sock.listen(1)
        print(f"Escuchando en puerto {self.port}")

        while True:
            client_socket, client_address = sock.accept()
            print(f"Conexión del cliente desde {client_address}")
            request = b""
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                request += data
                if b"\r\n\r\n" in request:
                    break
            request = request.decode("utf-8").strip()
            # GET /homer HTTP/1.1
            print(f"\n\nEsta es la request que se recibe desde navegador:\n\n{request}")
            first_line = request.split("\r\n")[0]
            pre = len("GET /")
            post = len(" HTTP/1.1")
            homer = first_line[pre:len(first_line) - post]
            respuesta = self.handle_request(homer)
            client_socket.sendall(respuesta)
            client_socket.close()



    def handle_request(self, request: str) -> str:
        respuesta = b""
        http_code = ""
        content_type = ""
        entry_flag = True


        if request == "":
            # index.html, hub primero
            with open("index.html", "rb") as given:
                respuesta += given.read()
            respuesta = respuesta.decode("utf-8")
        
        elif "entity" in request:
            query = ""
            result = ""
            tiempo = ""
            if "?homer" in request:
                # tratar la query solo si se ha respondido
                query = request[len("entity?homer="):]
                tiempo, result = entity(query)
                
            # solo servir el index
            request = "entity/index.html"
            with open(request, "rb") as given:
                respuesta += given.read()
            respuesta = respuesta.decode("utf-8")
            respuesta = respuesta.replace("%TIME%", tiempo)
            respuesta = respuesta.replace("%VALUE%", query.strip().replace("+", " "))
            respuesta = respuesta.replace("%RESULT%", result)


        elif "lecter" in request:
            pass
        
        elif "dabid" in request:
            pass
        
        elif request == "style.css":
            with open(request, "rb") as given:
                respuesta += given.read()
            respuesta = respuesta.decode("utf-8")
        
        else:  # Error 404, no se ha accedido como debe ser a los proyectos
            entry_flag = False
            respuesta += b"No se ha encontrado ese archivo. No busques cosas raras"
            respuesta = respuesta.decode("utf-8")
            http_code = "404 Not Found"
            content_type = "plain"

        # content-type block & code
        if entry_flag:
            http_code = "200 OK"
            if request.endswith(".html") or request == "":
                content_type = "html"
            elif request.endswith(".css"):
                content_type = "css"
            elif request.endswith(".txt"):
                content_type = "plain"

        # Primero codificamos el body antes del content-length porque los acentos valen por 2 bytes
        body = respuesta.encode("utf-8")

        header = f"HTTP/1.1 {http_code}\r\n"
        header += f"Content-Length: {len(body)}\r\n"
        header += f"Content-Type: text/{content_type}; charset=utf-8\r\n"
        header += "Connection: close\r\n\r\n"
        return header.encode("utf-8") + body



def main() -> None:
    port = int(os.environ.get("PORT", 8080))
    server = Server(port)
    server.run()


if __name__ == "__main__":
    main()
