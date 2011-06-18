from functools import wraps

from flask import Module, current_app, session, redirect, url_for, request
from flaskext import themes


admin = Module(__name__, 'admin',)# static_path='/admin/static')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/login/', methods=('GET', 'POST'))
def login():
    if request.form.get('username', None) and request.form.get('password', None):
        user = request.form['username']
        passwd = request.form['password']
        if user == current_app.config['ADMIN'] and \
           passwd == current_app.config['PASS']:
            session['user'] = user
            return redirect(request.args.get('next', url_for('flaskext.admin.index')))
        else:
            return themes.render_theme_template("auth", "login.html",
                                                bad_login=True)
    else:
        if request.method == 'POST':
            return themes.render_theme_template("auth", "login.html",
                                                bad_login=True)
        else:
            return themes.render_theme_template("auth", "login.html")


@admin.route('/logout/')
def logout():
    del session['user']
    return redirect('/')
