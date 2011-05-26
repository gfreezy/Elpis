import time

from flask import Module, g, render_template, request, redirect, url_for
from postmarkup import render_bbcode

frontend = Module(__name__)

@frontend.route('/')
def show_entries():
    g.nav_home = True
    cur = g.db.execute('select id, text, author, mail, time from entries order by id desc')
    entries = [dict(id=row[0], text=row[1], author=row[2], mail=row[3], time=row[4]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@frontend.route('/add', methods=['POST', 'GET'])
def add_entry():
    if request.method == 'POST':
        g.db.execute('insert into entries (text, author, mail, time) values (?, ?, ?, ?)',
                    (render_bbcode(request.form['text'], "UTF-8"), request.form['author'], request.form['mail'], time.time()))
        g.db.commit()
        return redirect(url_for('show_entries'))
    else:
        g.nav_home = False
        return render_template('add_entry.html')

@frontend.route('/del/<id>')
def del_entry(id):
    g.db.execute('delete from entries where id = ?', (id,))
    g.db.commit()
    return redirect(url_for('show_entries'))

@frontend.route('/comments/<id>', methods=['POST', 'GET'])
def comment(id):
    if request.method == 'POST':
        pass
    else:
        pass

