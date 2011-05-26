import sys
sys.path.append('.')
from elpis import app
def application(environ, start_response):
    return app(environ, start_response)
