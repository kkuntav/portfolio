import argparse
import socket
import time
from pathlib import Path

class Server:
    def __init__(self, port: int, db: str | None) -> None:
        """

        Initializes a simple HTTP server with
        the given q-gram index and port.

        SPARQL engine and database are optional.

        """
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

        # TODO: add your code here
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
            
            
        
        
        
        
        
        
        # Ahora esperamos después de ponernos a escuchar 
        # while True:
        #     print(f"\nEscuchando en el puerto {self.port}...")
        #     client_socket, client_adress = sock.accept()  # esto bloquea la escucha
        #     print(f"Conexión establecida con cliente en {client_adress}")
            
        #     # Recibimos los mensajes en bytes
        #     request = b""
        #     while True:
        #         data = client_socket.recv(4096)
        #         if not data:
        #             break
                
        #         request += data
        #         if b"\r\n\r\n" in request:  # doble salto de línea para terminar mensaje
        #             break
        #     request = request.decode("utf-8").strip()  # para pasar de bytes a esa codificacion
        #     print(f"Mensaje recibido del cliente: {request}")
            
            
        #     # Para extraer el mensaje del protocolo http:
        #     # GET /homer HTTP/1.1
        #     pre_message = len("GET /")
        #     first_line = request.split("\n")[0]
        #     post_message = len(first_line) - len(" HTTP/1.1") - 1
        #     mensaje = request[pre_message:post_message]
            
        #     # Para manejar el mensaje del cliente
        #     respuesta = self.handle_request(mensaje)  # recogemos el mensaje del cliente y lo respondemos
        #     client_socket.sendall(respuesta)  # mandamos todo al socket del cliente
        #     client_socket.close()  # cerramos conección




    def handle_request(self, request: str) -> str:
        respuesta = b""
        http_code = ""
        content_type = ""
        homer = False

        # Si se entra aquí, es porque se ha respondido el form, 
        # así que se hace el proceso de qgram y con el flag de homer
        # se decide hacer el replace
        # ?homer=Fuente
        if "?homer=" in request:
            homer = not homer
            request, query = request.split("?homer=")
            query = query.replace("+", " ")
            
            q_grams = []
            query_normalized = query.lower()
            for i in range(len(query) - 2):
                q_grams.append(query_normalized[i:i + 3])
            qgram_replace = f"3-Grams de {query}: {{" + ", ".join(q_grams) + "}"


        if Path(request).is_file():
            # Manejar intento de otros directorios
            if "/" in request:
                http_code += "403 Forbidden"
                respuesta = "No puedes acceder a esta ruta. NO INTENTES ESO"
            
            # Servimos el archivo --> homer = lap.html
            else:
                if request.endswith(".html"):
                    content_type = "html"
                elif request.endswith(".css"):
                    content_type = "css"
                elif request.endswith(".txt"):
                    content_type = "plain"
                
                file = request.lower()
                with open(file, "rb") as given:
                    respuesta += given.read()

                respuesta = respuesta.decode("utf-8")
                http_code += "200 OK"
                
                if homer:
                    respuesta = respuesta.replace("%RESULT%", f"{qgram_replace}")
                    respuesta = respuesta.replace("%VALUE%", f"{query}")
                else:
                    # Si no se está tratando todavía homer, quitamos el %RESULT% y %VALUE% para que no aparezcan
                    respuesta = respuesta.replace("%RESULT%", "")
                    respuesta = respuesta.replace("%VALUE%", "")


        # La request no en un archivo
        else:
            http_code += "404 Not Found"
            content_type = "plain"
            respuesta = "No se ha encontrado ningún archivo, fuera de aquí"


        # Primero codificamos el body antes del content-length porque los acentos valen por 2 bytes
        body = respuesta.encode("utf-8")

        header = f"HTTP/1.1 {http_code}\r\n"
        header += f"Content-Length: {len(body)}\r\n"
        header += f"Content-Type: text/{content_type}; charset=utf-8\r\n"
        header += "Connection: close\r\n\r\n"
        return header.encode("utf-8") + body
        
        
        
        
        
        # # Mandar el file que nos pida el mensaje
        # respuesta = b""
        # query_result = ""
        # query = ""
        # http_code = ""
        # content_type = ""

        
        # # caso de tener ya la query en la url
        # if "?query=" in request:
        #     request, query = request.split("?query=")
            
        #     # Vamos a generar 3-grams del query
        #     q_grams = []
        #     query = query.replace("+"," ")
        #     # |qgram(x)| = len(x) - q + 1
        #     query_normalized = query.lower()
        #     for i in range(len(query) - 2):
        #         q_grams.append(query_normalized[i: i + 3])
            
        #     query_result = f"3-Grams de \"{query}\": {{"
        #     query_result += ", ".join(q_grams)
        #     query_result += "}"





        # if Path(request).is_file():
        #     if "/" in request:  # intentar acceder con ruta absoluta
        #         respuesta = f"VEGGA no te entregará acceso a \"{request}\". Eso no está bien".encode("utf-8")
        #         http_code = "403 Go out"


        #     else:
        #         file = request.lower()
        #         http_code = "200 Todo cool"
        #         with open(file, "rb") as given:
        #             respuesta += given.read()


        #         # tipo del archivo para el header
        #         if request.endswith(".html"):
        #             content_type = "text/html"
        #         elif request.endswith(".txt"):
        #             content_type = "text/plain"
        #         elif request.endswith(".css"):
        #             content_type = "text/css"
                
                
        #         # Responder la query
        #         if request == "search.html":
        #             # Con los replace, lo que hacemos es poner esos strings en los &values%
        #             # que tenemos en el html; editamos el html antes de mandarlo al navegador
        #             respuesta = respuesta.replace(b"%QUERY%", query.encode("utf-8"))
        #             respuesta = respuesta.replace(b"%RESULT%", query_result.encode("utf-8"))
        
        # else:
        #     respuesta = "Ese archivo no existe fam".encode("utf-8")
        #     http_code = "404 No existe"



        # # Para responder a un mensaje de un navegador con http tenemos un protocolo de respuesta
        # encoding = "utf-8"
        # content_type += f"; charset={encoding}"
        
        # header = f"HTTP/1.1 {http_code}\r\n"
        # header += f"Content-Length: {len(respuesta)}\r\n"
        # header += f"Content-Type: {content_type}\r\n"
        # header += "Connection: close\r\n"
        # header += "\r\n"
        
        # header = header.encode("utf-8")
        # return (header + respuesta)
        
        


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "entities", type=str, help="path to entities file for q-gram index"
    )
    parser.add_argument("port", type=int, help="port to run the server on")
    parser.add_argument(
        "-db",
        "--database",
        type=str,
        default=None,
        help="path to sqlite3 database for SPARQL engine",
    )
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    """

    Builds a q-gram index from the given file
    and starts a server on the given port.

    """
    # Create a new q-gram index from the given file.
    print(f"Building q-gram index from file {args.entities}.")
    start = time.perf_counter()
    print(f"Done, took {(time.perf_counter() - start) * 1000:.1f}ms.")

    server = Server(args.port, args.database)
    print(
        f"Starting server on port {args.port}, go to "
        f"http://localhost:{args.port}/search.html"
    )
    server.run()


if __name__ == "__main__":
    main(parse_args())
