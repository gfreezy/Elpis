import sys
sys.path.append(sys.path[0])

from elpis import app
def application(environ, start_response):
    return app(environ, start_response)
