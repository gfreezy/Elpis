# all the imports
from contextlib import closing
import time
import sqlite3
from flask import Flask, request, g, redirect, url_for, \
    render_template
from flaskext import gravatar
from postmarkup import render_bbcode

# configuration
DATABASE = 'elpis.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

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

@app.route('/')
def show_entries():
    g.nav_home = True
    cur = g.db.execute('select id, text, author, mail, time from entries order by id desc')
    entries = [dict(id=row[0], text=row[1], author=row[2], mail=row[3], time=row[4]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST', 'GET'])
def add_entry():
    g.nav_home = False
    if request.method == 'POST':
        g.db.execute('insert into entries (text, author, mail, time) values (?, ?, ?, ?)',
                    [render_bbcode(request.form['text'], "UTF-8"), request.form['author'], request.form['mail'], time.time()])
        g.db.commit()
        return redirect(url_for('show_entries'))
    else:
        return render_template('add_entry.html')

@app.route('/delete/<id>')
def del_entry(id):
    g.db.execute('delete from entries where id=?', id)
    g.db.commit()
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    #init_db()
    app.run(debug=True)
