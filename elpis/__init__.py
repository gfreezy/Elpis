import time
import sqlite3
import config

from contextlib import closing
from flask import Flask, g
from flaskext import gravatar

# create our little application :)
app = Flask(__name__)
app.config.from_object(config)
 
from elpis.views.frontend import frontend
app.register_module(frontend)

gravatar = gravatar.Gravatar(app, size=100, rating='g', default='retro',
        force_default=False, force_lower=False)

@app.template_filter()
def format_time(t):
    current_time = time.time()
    limit = current_time - t
    if limit < 1:
        return '1 second ago'
    elif 1 < limit < 60:
        return '%d seconds ago' % limit
    elif limit == 60:
        return '1 minute ago'
    elif 60 < limit < 3600:
        return '%d minute ago' % (limit//60)
    elif limit == 3600:
        return 'an hour ago'
    elif 3600 < limit < 86400:
        return '%d hours ago' % (limit//3600)
    elif limit == 86400:
        return 'one day ago'
    elif 86400 < limit < 259200:
        return '%d days ago' % (limit//86400)
    else:
        struct_t = time.localtime(t)
        return 'at %s' % time.strftime('%a %b %d %H:%M:%S', struct_t)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response


if __name__ == '__main__':
    #init_db()
    app.run(debug=True)
