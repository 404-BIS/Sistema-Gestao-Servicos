from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from bd.db import mysql

auth= Blueprint('auth',__name__, template_folder='templates')

@auth.route('/login')
def login():
    return render_template('login.html')

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
        
    return redirect (url_for('auth.login'))