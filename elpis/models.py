# -*- coding: utf-8 -*-
import time
import random

from elpis import db
def get_token(): #获得随机字符串
    return ''.join(random.sample([chr(i) for i in range(48, 123)], 12))


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    author = db.Column(db.String(80))
    mail = db.Column(db.String(80))
    time = db.Column(db.Integer)
    comments_count = db.Column(db.Integer)
    token = db.Column(db.String(12))

    def __init__(self, content=None, author=None, mail=None):
        self.content = content
        self.author = author
        self.mail = mail
        self.time = int(time.time())
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

    def __init__(self, content=None, entry_id=None, author=None, mail=None):
        self.content = content
        self.entry_id = entry_id
        self.author = author
        self.mail = mail
        self.time = int(time.time())
        self.token = get_token()

    def __repr__(self):
        return '<Comment %d>' % self.id


class Receiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(80))
    phone = db.Column(db.String(11))
    time = db.Column(db.Integer)
    token = db.Column(db.String(12))

    def __init__(self, mail=None, phone=None):
        self.mail = mail
        self.phone = phone
        self.time = int(time.time())
        self.token = get_token()

    def __repr__(self):
        return '<Receiver %d>' % self.id


