from flask import Blueprint,render_template,request,redirect
from db import mysql

login_blueprint= Blueprint('login',__name__, template_folder='templates')~

@login_blueprint.route('/login/menu')
def Getlogin():
    return render_template ('login/index.html')


@login_blueprint.route('/cachorro', methods=['GET', 'POST'])
def login ():
    if request.method == 'POST':
        formulario = request.form
        email = formulario['email']
        password = formulario['pass']
        with mysql.cursor()as Cursor:
            Cursor.execute("SELECT pass_user FROM user WHERE email_user= %s",(email,))
            Details = Cursor.fetchall()
            ss = str(Details)
            tupla= ss.count(password)
            Cursor.close()
            if tupla==1:
                return redirect('/usuario/menu')
            else:
                return 'Credenciais invalidas'