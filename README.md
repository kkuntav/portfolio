# portfolio

1. Tener el servidor en tu repositorio

Por ejemplo:

portfolio/
├── server/
│   ├── server.py
│   ├── http_request.py
│   ├── http_response.py
│   ├── router.py
│   └── mime_types.py
│
├── index.html
├── dabid_demo/
├── lecter_demo/
└── entity_demo/

Y que el servidor sea código tuyo, sin depender de Flask/FastAPI para la parte HTTP.

En el README de GitHub puedes explicar:

Custom HTTP Server

This portfolio is served by a lightweight HTTP server
implemented from scratch in Python using TCP sockets.

Features:
- HTTP request parsing
- GET requests
- URL routing
- Static file serving
- MIME type detection
- HTTP status codes
- 404 handling
- Content-Length headers
2. Añadir una sección en tu portfolio

Por ejemplo:

How this portfolio works

This website is served by a custom HTTP server implemented from scratch in Python using TCP sockets. Instead of using a web framework, the server parses incoming HTTP requests, resolves routes and serves the corresponding resources.

Y un botón:

[ View source on GitHub ]

que lleve directamente a la carpeta server/.