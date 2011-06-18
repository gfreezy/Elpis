# -*- coding: utf-8 -*-
import time
import config

from flask import Flask
from flaskext import themes
from flaskext.admin import Admin
from flaskext.gravatar import Gravatar
from flaskext.sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown

# create our little application :)
app = Flask(__name__)
app.config.from_object(config)

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


Markdown(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro',
        force_default=False, force_lower=False)


db = SQLAlchemy(app)
from elpis import models

from elpis.frontend.view import frontend
app.register_module(frontend)

from elpis.admin.view import login_required, admin as admin_view
app.register_module(admin_view, url_prefix='/admin')

admin_mod = Admin(app, models, db.session,
                  theme='auth',
                  view_decorator=login_required,
                  exclude_pks=True)

themes.setup_themes(app)
app.register_module(admin_mod, url_prefix='/admin')
