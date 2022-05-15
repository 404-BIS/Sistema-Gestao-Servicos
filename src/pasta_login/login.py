from flask import Blueprint, render_template, url_for,redirect,request,session,flash
from flask_login import login_required, current_user
from bd.db import mysql
main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    return redirect (url_for('auth.login'))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.nome_user)



@main.route('/login', methods=['POST'])
def login_post():
    formulario = request.form
    email_user = formulario['email']
    pass_user = formulario['pass']
    with mysql.cursor()as Cursor:
        Cursor.execute('SELECT * FROM user WHERE email_user = %s AND pass_user = %s', (email_user, pass_user,))
        conta = Cursor.fetchone()
        if not conta:
            flash('Por favor, Insira informações Válidas!')
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
            session['email_admin'] = email_user
            session['loggedin'] = True
            session['id_admin'] = conta[0]
            session['nome_admin'] = conta[1]
            return redirect(url_for("admin.adm"))
