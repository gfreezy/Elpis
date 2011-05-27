import time

from flask import Module, g, render_template, request, redirect, url_for
from postmarkup import render_bbcode

frontend = Module(__name__)


def current_page(current):
    g.nav = dict()
    g.nav['home'] = g.nav['add'] = g.nav['view'] = g.nav['receivers'] = False
    g.nav[current] = True

@frontend.route('/')
@frontend.route('/view/')
def show_entries():
    current_page('home')
    cur = g.db.execute('select id, text, author, mail, time, comments_num from entries order by id desc')
    entries = (dict(id=row[0], text=row[1], author=row[2], mail=row[3], time=row[4], comments_num=row[5]) for row in cur.fetchall())
    return render_template('show_entries.html', entries=entries)

@frontend.route('/add/', methods=['POST', 'GET'])
def add_entry():
    if request.method == 'POST':
        g.db.execute('insert into entries (text, author, mail, time, comments_num) values (?, ?, ?, ?, ?)',
                    (render_bbcode(request.form['text'], "UTF-8"), request.form['author'], request.form['mail'], time.time(), 0))
        g.db.commit()
        return redirect(url_for('show_entries'))
    else:
        current_page('add')
        return render_template('add_entry.html')

@frontend.route('/del/<id>')
def del_entry(id):
    g.db.execute('delete from comments where post_id = ?', (id,))
    g.db.execute('delete from entries where id = ?', (id,))
    g.db.commit()
    return redirect(url_for('show_entries'))

@frontend.route('/view/<id>', methods=['POST', 'GET'])
def view(id):
    current_page('view')
    if request.method == 'POST':
        g.db.execute('insert into comments (text, post_id, author, mail, time) values (?, ?, ?, ?, ?)',
                    (render_bbcode(request.form['text'], "UTF-8"), id, request.form['author'], request.form['mail'], time.time()))
        g.db.execute('update entries set comments_num = comments_num+1 where id = ?', (id,))
        g.db.commit()

    cur = g.db.execute('select id, text, author, mail, time from entries where id = ?', (id,))
    r = cur.fetchone()
    entry = dict((key, r[i]) for (i, key) in enumerate(('id', 'text', 'author', 'mail', 'time')))

    cur = g.db.execute('select id, text, author, mail, time from comments where post_id = ?', (id,))
    comments = (dict(id=row[0], text=row[1], author=row[2], mail=row[3], time=row[4]) for row in cur.fetchall())
    return render_template('view.html', entry=entry, comments=comments)

@frontend.route('/del_comment/<post_id>/<id>')
def del_comment(post_id, id):
    g.db.execute('delete from comments where post_id = ? and id = ?', (post_id, id))
    g.db.execute('update entries set comments_num = comments_num -1 where id = ?', (post_id,))
    g.db.commit()
    return redirect(url_for('view', id=id))

@frontend.route('/about/')
def about():
    current_page('about')
    return render_template('about.html')

#@frontend.route('/receivers/<action>/<id>', methods=['POST', 'GET'])
@frontend.route('/receivers/', methods=['POST', 'GET'])
def receivers():
    current_page('receivers')
    if request.method == 'POST':
        g.db.execute('insert into receivers (mail, phone, time) values (?, ?, ?)',
                    (request.form['mail'], request.form['phone'], time.time()))
        g.db.commit()
    cur = g.db.execute('select * from receivers')
    receivers = (dict(id=row[0], mail=row[1], phone=row[2], time=row[3]) for row in cur.fetchall())

    return render_template('receivers.html', receivers=receivers)
