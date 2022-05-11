from flask import Flask, redirect, render_template, url_for,request,session,flash
from flask_login import LoginManager, logout_user
from bd.db import mysql


app = Flask(__name__)
 

from pasta_user.user import user_blueprint
from pasta_executor.executor import executor_blueprint
from pasta_login.login import main
from pasta_cadastro.cadastro import auth
from pasta_adm.adm import admin

import secrets

app = Flask(__name__)

secret = secrets.token_urlsafe(32)
app.secret_key = secret


app.register_blueprint(user_blueprint)
app.register_blueprint(executor_blueprint)
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(admin)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id_user):
    return mysql.get(id_user)



@app.route('/login', methods=['POST'])
def login_post():
    formulario = request.form
    email_user = formulario['email']
    pass_user = formulario['pass']
    with mysql.cursor()as Cursor:
        Cursor.execute('SELECT * FROM user WHERE email_user = %s AND pass_user = %s', (email_user, pass_user,))
        conta = Cursor.fetchone()
        if not conta:
            flash('Please check your login details and try again.')
            return redirect (url_for('auth.login'))
        if conta[4] == 'user':
            session['email_user'] = email_user
            session['loggedin'] = True
            session['id_user'] = conta[0]
            session['nome_user'] = conta[1]
            return redirect(url_for('user.home'))
        elif conta[4] == 'exec':
            session['email_exec'] = email_user
            session['loggedin'] = True
            session['id_exec'] = conta[0]
            session['nome_exec'] = conta[1]
            return redirect(url_for('executor.exec'))
        else:
            session['email_user'] = email_user
            session['loggedin'] = True
            session['id_user'] = conta[0]
            session['nome_user'] = conta[1]
            return redirect(url_for("admin.adm"))

@app.route("/logout")
def logout():
    logout_user()
    session['loggedin'] = False
    return redirect(url_for('auth.login'))

if __name__ == "__main__":
    app.run(debug=True)