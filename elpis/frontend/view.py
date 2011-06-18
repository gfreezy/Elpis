# -*- coding: utf-8 -*-
import mailer

from flask import Module, g, render_template, request, redirect, url_for
from postmarkup import render_bbcode
from elpis.models import db, Entry, Comment, Receiver
from celery.execute import send_task


frontend = Module(__name__, 'frontend', static_path='/frontend/static')


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
        return 'Error'

    msg = mailer.Message(charset='utf-8')
    msg.From = 'gfreezy@163.com'
    msg.To = entity.mail
    msg.Subject = 'Confirm: Do you want to delete the %s?' % entity_type
    msg.Html = \
    """<h1>If you want to delete the %s, Click the link below</h1>
    <a href="%s">%s</a>
    """ % (entity_type, url, url)
    send_task('tasks.mail.send_mail',[msg,])

    return 'Check your mailbox "%s"' % entity.mail


def inform_new_comment(entry, comment):
    msg = mailer.Message(charset='utf-8')
    msg.From = 'gfreezy@163.com'
    msg.To = entry.mail
    msg.Subject = 'Your post @Elpis has a new comment'
    msg.Html = """
    <strong>Comment:</strong>
        <em>
        <p>"%s"</p>
        </em>
        <p>by <a href="mailto:%s">%s</a> at <a href=%s>%s</a></p>
    <br>
    <br>
    <strong>Your post:</strong>
        <p><em>"%s"</em></p>
    """ % (comment.content, comment.mail, comment.author, 
           url_for('view', id=entry.id, _external=True),
           url_for('view', id=entry.id, _external=True), 
           entry.content)
    send_task('tasks.mail.send_mail', [msg])


def current_page(current):
    g.nav = dict()
    g.nav['home'] = g.nav['add'] = g.nav['view'] = g.nav['receivers'] = False
    g.nav[current] = True


@frontend.route('/')
@frontend.route('/view/')
def show_entries():
    current_page('home')
    entries = Entry.query.order_by('id desc').all()
    return render_template('frontend/show_entries.html', entries=entries)


@frontend.route('/add/', methods=('POST', 'GET'))
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
        return render_template('frontend/add_entry.html')


@frontend.route('/del_entry/<id>/')
@frontend.route('/del_entry/<id>/<token>')
def del_entry(id, token=None):
    if token is None:
        return request_deletion(entity_type='entry', id=id)
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
        inform_new_comment(entry, comment)

    entry = Entry.query.get(id)
    comments = Comment.query.filter_by(entry_id=id)
    return render_template('frontend/view.html', entry=entry, comments=comments)


@frontend.route('/del_comment/<entry_id>/<id>/')
@frontend.route('/del_comment/<entry_id>/<id>/<token>/')
def del_comment(entry_id=None, id=None, token=None):
    if token is None:
        return request_deletion(entity_type='comment', id=id, entry_id=entry_id)
    else:
        comment = Comment.query.filter_by(id=id, token=token).first()
        if not comment is None:
            entry = Entry.query.get(entry_id)
            entry.comments_count -= 1

            db.session.add(entry)
            db.session.delete(comment)
            db.session.commit()
        return redirect(url_for('view', id=id))


@frontend.route('/about/')
def about():
    current_page('about')
    return render_template('frontend/about.html')


@frontend.route('/receivers/', methods=['POST', 'GET'])
def receivers():
    current_page('receivers')
    if request.method == 'POST':
        receiver = Receiver(
                request.form['mail'],
                request.form['phone'])

        db.session.add(receiver)
        db.session.commit()
        send_task("tasks.fetion.add_contact", [request.form['phone']])

    receivers = Receiver.query.order_by('id desc').all()
    return render_template('frontend/receivers.html', receivers=receivers)


@frontend.route('/del_receiver/<id>/')
@frontend.route('/del_receiver/<id>/<token>/')
def del_receiver(id, token=None):
    if token is None:
        return request_deletion(entity_type='receiver', id=id)
    else:
        receiver = Receiver.query.filter_by(id=id, token=token).first()
        if not receiver is None:
            db.session.delete(receiver)
            db.session.commit()
        return redirect(url_for('receivers'))

