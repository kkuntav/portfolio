import socket
from pathlib import Path
import os


class Server:
    def __init__(self, port: int, db: str | None) -> None:
        self.port = port
        self.db = db



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
            print(f"Esta es la request que se recibe desde navegador:\n\n{request}")
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
        homer = False

        allowed_paths = ("index.html", "/lecter/index.html", "/dabid/index.html", "/entity/index.html")
        match request:
            # Caso de home, index.html en root
            case "":
                with open("index.html", "rb") as given:
                    respuesta += given.read()
                respuesta = respuesta.decode("utf-8")
                http_code = "200 OK"
                
            
            
            case _:
                respuesta += b"No se ha encontrado ese archivo. No busques cosas raras"
                http_code = "404 Not Found"
                content_type = "plain"

        if http_code is "":
            http_code = "200 OK"
            content_type = "html"  # TBD






        # if Path(request).is_file():
        #     # Manejar intento de otros directorios
        #     if "/" in request:
        #         http_code += "403 Forbidden"
        #         respuesta = "No puedes acceder a esta ruta. NO INTENTES ESO"
            
        #     # Servimos el archivo --> homer = lap.html
        #     else:
        #         if request.endswith(".html"):
        #             content_type = "html"
        #         elif request.endswith(".css"):
        #             content_type = "css"
        #         elif request.endswith(".txt"):
        #             content_type = "plain"
                
        #         file = request.lower()
        #         with open(file, "rb") as given:
        #             respuesta += given.read()

        #         respuesta = respuesta.decode("utf-8")
        #         http_code += "200 OK"
                
        #         if homer:
        #             respuesta = respuesta.replace("%RESULT%", f"{qgram_replace}")
        #             respuesta = respuesta.replace("%VALUE%", f"{query}")
        #         else:
        #             # Si no se está tratando todavía homer, quitamos el %RESULT% y %VALUE% para que no aparezcan
        #             respuesta = respuesta.replace("%RESULT%", "")
        #             respuesta = respuesta.replace("%VALUE%", "")


        # # La request no en un archivo
        # else:
        #     http_code += "404 Not Found"
        #     content_type = "plain"
        #     respuesta = "No se ha encontrado ningún archivo, fuera de aquí"


        # Primero codificamos el body antes del content-length porque los acentos valen por 2 bytes
        body = respuesta.encode("utf-8")

        header = f"HTTP/1.1 {http_code}\r\n"
        header += f"Content-Length: {len(body)}\r\n"
        header += f"Content-Type: text/{content_type}; charset=utf-8\r\n"
        header += "Connection: close\r\n\r\n"
        return header.encode("utf-8") + body



def main() -> None:
    entities = "entity/database.tsv"
    port = int(os.environ.get("PORT", 8080))
    server = Server(port, entities)
    server.run()


if __name__ == "__main__":
    main()
