# -*- coding: utf-8 -*-
import time
import config
import random

from flask import Flask
from flaskext.gravatar import Gravatar
from flaskext.mail import Mail
from flaskext.sqlalchemy import SQLAlchemy

# create our little application :)
app = Flask(__name__)
app.config.from_object(config)


def get_token(): #获得随机字符串
    return ''.join(random.sample([chr(i) for i in range(48, 123)], 12))

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


gravatar = Gravatar(app, size=100, rating='g', default='retro',
        force_default=False, force_lower=False)
mail = Mail(app)
db = SQLAlchemy(app)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    author = db.Column(db.String(80))
    mail = db.Column(db.String(80))
    time = db.Column(db.Integer)
    comments_count = db.Column(db.Integer)
    token = db.Column(db.String(12))

    def __init__(self, content, author, mail):
        self.content = content
        self.author = author
        self.mail = mail
        self.time = time.time()
        self.comments_count = 0
        self.token = get_token()

    def __repr__(self):
        return '<Entry %d>' % self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    entry_id = db.Column(db.Integer)
    author = db.Column(db.String(80))
    mail = db.Column(db.String(80))
    time = db.Column(db.Integer)
    token = db.Column(db.String(12))

    def __init__(self, content, entry_id, author, mail):
        self.content = content
        self.entry_id = entry_id
        self.author = author
        self.mail = mail
        self.time = time.time()
        self.token = get_token()

    def __repr__(self):
        return '<Comment %d>' % self.id


class Receiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(80))
    phone = db.Column(db.String(11))
    time = db.Column(db.Integer)
    token = db.Column(db.String(12))

    def __init__(self, mail, phone):
        self.mail = mail
        self.phone = phone
        self.time = time.time()
        self.token = get_token()

    def __repr__(self):
        return '<Receiver %d>' % self.id


from elpis.views.frontend import frontend
app.register_module(frontend)
