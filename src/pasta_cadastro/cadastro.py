from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from bd.db import mysql
from flask_login import login_user

auth= Blueprint('auth',__name__, template_folder='templates')

@auth.route('/login')
def login():
    return render_template('login.html')

# @auth.route('/login', methods=['POST'])
# def login_post():
#     formulario = request.form
#     email = formulario['email']
#     password = formulario['pass']
#     with mysql.cursor() as Cursor:
#         conta=Cursor.execute("SELECT * FROM user WHERE pass_user= %s and email_user= %s",(email,password))
#         Cursor.close()
#         if not conta:
#             flash('Please check your login details and try again.')
#             return redirect (url_for('auth.login'))
#         session['username'] = email
        
#         return redirect(url_for('user.home'))

# @auth.route('/auth3') #deslogar
# def c():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('cadastro.html')

@auth.route('/signup', methods=['GET','POST'])
def cadastro ():
    formulario = request.form
    nome = formulario['nome_user']
    email = formulario['email_user']
    password = formulario['pass_user']
    type_user = 'user'
    
    with mysql.cursor()as Cursor:
        emaildb=Cursor.execute("SELECT email_user FROM user WHERE email_user= %s",(email,))
        if emaildb:
            flash('Email address already exists')
            return redirect (url_for('auth.signup'))
        Cursor.execute("INSERT INTO user (nome_user, email_user, pass_user,type_user) VALUES(%s, %s, %s, %s)",(nome,email,password,type_user))
        mysql.commit()
        Cursor.close()
    return redirect (url_for('auth.login'))