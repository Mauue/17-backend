from wsgiref.simple_server import make_server
from app import create_app

app = create_app()
httpd = make_server('localhost', 5000, app)
print("server on port:5000")
httpd.serve_forever()