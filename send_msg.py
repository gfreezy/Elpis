#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from PyFetion import PyFetion
import sqlite3

FROM = '13856990110'
PASS = '12qwaszx'
DATABASE = 'elpis.db'

def connect_db():
    return sqlite3.connect(DATABASE)

if __name__ == '__main__':
    phone = PyFetion.PyFetion(FROM, PASS, 'HTTP')
    if not phone.login():
        print 'login error'
    else:
        print 'login success'

    db = connect_db()
    cur = db.execute('select phone from receivers order by id desc')
    phone_list = list(u'%s' % num[0] for num in cur.fetchall())

    cur = db.execute('select * from entries order by id desc')
    rlt = cur.fetchone()
    text = rlt[1]

    print phone_list
    print text
    for phone_num in phone_list:
        if not phone.send_sms(text.encode('utf-8'), phone_num):
            print 'send msg to %s error' % phone_num
        else:
            print 'send msg to %s success' % phone_num

    phone.logout()
    db.close()
