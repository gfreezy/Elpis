#!/usr/bin/env python2
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

    cur = db.execute('select text from entries order by id desc')
    text = cur.fetchone()

    print phone_list
    for phone in phone_list:
        if not phone.send_sms(text , phone):
            print 'send msg to %s error' % phone
        else:
            print 'send msg to %s success' % phone

    phone.logout()
    db.close()
