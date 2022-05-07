from flask import Blueprint, render_template, url_for,redirect
from flask_login import login_required, current_user

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    return redirect (url_for('auth.login'))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.nome_user)





# @main.route('/cachorro', methods=['GET', 'POST'])
# def login ():
#     if request.method == 'POST':
#         formulario = request.form
#         email = formulario['email']
#         password = formulario['pass']
#         with mysql.cursor()as Cursor:
#             Cursor.execute("SELECT pass_user FROM user WHERE email_user= %s",(email,))
#             Details = Cursor.fetchall()
#             ss = str(Details)
#             tupla= ss.count(password)
#             Cursor.close()
#             if tupla==1:
#                 return redirect('/usuario/menu')
#             else:
#                 return 'Credenciais invalidas'

