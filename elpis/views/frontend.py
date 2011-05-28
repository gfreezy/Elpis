# -*- coding: utf-8 -*-
from flask import Module, g, render_template, request, redirect, url_for
from postmarkup import render_bbcode
from flaskext.mail import Message
from elpis import mail, db, Entry, Comment, Receiver

frontend = Module(__name__)

def request_deletion(entity_type, id, entry_id=None):
    if entity_type == 'entry':
        entity = Entry.query.get(id)
        url = url_for('del_entry', id=entity.id, token=entity.token, _external=True)
    elif entity_type == 'comment':
        entity = Comment.query.get(id)
        url = url_for('del_comment', id=entity.id, entry_id=entry_id, token=entity.token, _external=True)
    elif entity_type == 'receiver':
        entity = Receiver.query.get(id)
        url = url_for('del_receiver', id=entity.id, token=entity.token, _external=True)
    else:
        return

    msg = Message('Confirm: Do you want to delete the %s?' % entity_type)
    msg.recipients = [entity.mail]
    msg.html = \
    """<h1>If you want to delete the %s, Click the link below</h1>
    <a href="%s">%s</a>
    """ % (entity_type, url, url)
    mail.send(msg)

def current_page(current):
    g.nav = dict()
    g.nav['home'] = g.nav['add'] = g.nav['view'] = g.nav['receivers'] = False
    g.nav[current] = True

@frontend.route('/')
@frontend.route('/view/')
def show_entries():
    current_page('home')
    entries = Entry.query.all()
    return render_template('show_entries.html', entries=entries)

@frontend.route('/add/', methods=['POST', 'GET'])
def add_entry():
    if request.method == 'POST':
        entry = Entry(
                render_bbcode(request.form['text'], "UTF-8"),
                request.form['author'],
                request.form['mail'])

        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('show_entries'))
    else:
        current_page('add')
        return render_template('add_entry.html')

@frontend.route('/del_entry/<id>/')
@frontend.route('/del_entry/<id>/<token>')
def del_entry(id, token=None):
    if token is None:
        request_deletion('entry', id)
    else:
        entry = Entry.query.filter_by(id=id, token=token).first()
        if entry is not None:
            comments = Comment.query.filter_by(entry_id=id)

            db.session.delete(entry)
            for comment in comments:
                db.session.delete(comment)
            db.session.commit()
    return redirect(url_for('show_entries'))

@frontend.route('/view/<id>/', methods=['POST', 'GET'])
def view(id):
    current_page('view')
    if request.method == 'POST':
        comment = Comment(
                render_bbcode(request.form['text'], "UTF-8"),
                id, 
                request.form['author'], 
                request.form['mail'])

        entry = Entry.query.get(id)
        entry.comments_count += 1

        db.session.add(comment)
        db.session.add(entry)
        db.session.commit()

    entry = Entry.query.get(id)
    comments = Comment.query.filter_by(entry_id=id)
    return render_template('view.html', entry=entry, comments=comments)

@frontend.route('/del_comment/<entry_id>/<id>/')
@frontend.route('/del_comment/<entry_id>/<id>/<token>/')
def del_comment(entry_id=None, id=None, token=None):
    if token is None:
        request_deletion('comment', id, entry_id=entry_id)
    else:
        comment = Comment.query.filter_by(id=id, token=token).first()
        entry = Entry.query.get(entry_id)
        entry.comments_count -= 1

        db.session.add(entry)
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('view', id=id))

@frontend.route('/about/')
def about():
    current_page('about')
    return render_template('about.html')

@frontend.route('/receivers/', methods=['POST', 'GET'])
def receivers():
    current_page('receivers')
    if request.method == 'POST':
        receiver = Receiver(
                request.form['mail'],
                request.form['phone'])

        db.session.add(receiver)
        db.session.commit()

    receivers = Receiver.query.all()
    return render_template('receivers.html', receivers=receivers)

@frontend.route('/del_receiver/<id>/')
@frontend.route('/del_receiver/<id>/<token>/')
def del_receiver(id, token=None):
    if token is None:
        request_deletion('receiver', id)
    else:
        receiver = Receiver.query.filter_by(id=id, token=token).first()
        db.session.delete(receiver)
        db.session.commit()
    return redirect(url_for('receivers'))

