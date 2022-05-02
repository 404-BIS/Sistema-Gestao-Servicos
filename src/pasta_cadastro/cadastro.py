from flask import Blueprint,render_template,request,redirect
from db import mysql

cadastro_blueprint= Blueprint('cadastro',__name__, template_folder='templates')

@cadastro_blueprint.route('/login/cadastro', methods=['GET','POST'])
def cadastro ():
    if request.method == 'POST':
        formulario = request.form
        nome = formulario['nome_user']
        email = formulario['email_user']
        password = formulario['pass_user']
        type_user = 'user'
        with mysql.cursor()as Cursor:
            Cursor.execute("INSERT INTO user (nome_user, email_user, pass_user,type_user) VALUES(%s, %s, %s, %s)",(nome,email,password,type_user))
            mysql.connection.commit()
            Cursor.close()
            return redirect ('/login/menu')
    return render_template ('cadastro/index.html')
