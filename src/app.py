
from flask import Flask, redirect, url_for,session,request,render_template
from flask_login import LoginManager, logout_user
from bd.db import mysql
import datetime

from pasta_user.user import user_blueprint
from pasta_executor.executor import executor_blueprint
from pasta_login.login import main
from pasta_cadastro.cadastro import auth
from pasta_adm.adm import admin

import os
from werkzeug.utils import secure_filename

import secrets


UPLOAD_FOLDER = 'static/uploads/'


app = Flask(__name__)

secret = secrets.token_urlsafe(32)
app.secret_key = secret


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024


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

@app.route("/logout")
def logout():
    session['loggedin'] = False
    logout_user()
    return redirect(url_for('auth.login'))

@app.route('/usuario/solicitacao', methods=['GET','POST'])
def user():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_user']
    nome = session['nome_user']
    email = session['email_user']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        Cursor.execute("SELECT id_user FROM user WHERE type_user = 'exec'")
        allExec = Cursor.fetchall()

    if request.method == 'POST':
        Details = request.form
        titulo = Details['titulo']
        descricao = Details['descricao']
        tipo = Details['tipo']   
        status_sol = 'Aberta'
        comentario= ''
        hora= datetime.datetime.now()
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
        else:
            filename=''
        if len(allExec) == 0:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with mysql.cursor()as Cursor:
                Cursor.execute("INSERT INTO solicitacao (title_sol, desc_sol, status_sol ,type_problem, comentario,foto, data_inicio, id_user) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,filename,hora,pk_user)) 
                mysql.commit()
                Cursor.close()
                return redirect("/usuario/menu")

        elif len(allExec) == 1:
            execone = allExec[0]
            if file:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else :
                filename=''
            with mysql.cursor()as Cursor:
                Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) ",(titulo,descricao,status_sol,tipo,comentario,filename,pk_user,hora,execone,))
                mysql.commit()
                Cursor.close()
                return redirect("/usuario/menu")
        else:
            if file:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else :
                filename=''
            with mysql.cursor()as Cursor:
                Cursor.execute("SELECT id_sol FROM solicitacao")
                tudo = Cursor.fetchall()
                if len(tudo) >= 1 :
                    Cursor.execute("SELECT id_fechador FROM solicitacao ORDER BY id_sol DESC LIMIT 2")
                    ultimoChamado = Cursor.fetchall()
                    for x in range (len(allExec)):
                        if ultimoChamado[0] in allExec == True:
                                if allExec[x] == ultimoChamado[0]:
                                    if allExec.index(allExec[x]) + 1 < len(allExec):
                                        a = allExec[x+1]

                                    elif allExec.index(allExec[x]) + 2 > len(allExec):
                                        a = allExec[0]

                                    elif allExec.index(allExec[x]) + 1 == len(allExec):
                                        a = allExec[-1]
                                                    
                                    
                                    Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,filename,pk_user,hora,a))
                                    mysql.commit()
                                    Cursor.close()
                                    return redirect("/usuario/menu")

                        else:
                                if allExec[x] == ultimoChamado[0]:
                                    if allExec.index(allExec[x]) + 1 < len(allExec):                                       
                                        a = allExec[x+1]

                                    elif allExec.index(allExec[x]) + 2 > len(allExec):                            
                                        a = allExec[0]

                                    elif allExec.index(allExec[x]) + 1 == len(allExec):
                                        a = allExec[-1]
                                                        
                                    Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,filename,pk_user,hora,a))
                                    mysql.commit()
                                    Cursor.close()
                                    return redirect("/usuario/menu")
                else:
                    for x in allExec:
                        Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,filename,pk_user,hora,x,))
                        mysql.commit()
                        Cursor.close()
                        return redirect("/usuario/menu")

    return render_template('/nova-requisicao-user.html',nome=nome,email=email,senha=senha)


@app.route('/adm/solicitacao',methods=['GET','POST'])
def index():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        Cursor.execute("SELECT id_user FROM user WHERE type_user = 'exec'")
        allExec = Cursor.fetchall()

    if request.method == 'POST':
        Details = request.form
        titulo = Details['titulo']
        descricao = Details['descricao']
        tipo = Details['tipo']   
        status_sol = 'Aberta'
        comentario= ''
        hora= datetime.datetime.now()
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
        else:
            filename=''
        if len(allExec) == 0:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with mysql.cursor()as Cursor:
                Cursor.execute("INSERT INTO solicitacao (title_sol, desc_sol, status_sol ,type_problem, comentario,foto, data_inicio,id_user) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,filename,hora,pk_user)) 
                mysql.commit()
                Cursor.close()
                return redirect("/adm/menu")

        elif len(allExec) == 1:
            execone = allExec[0]
            if file:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else :
                filename=''
            with mysql.cursor()as Cursor:
                Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,filename,pk_user,hora,execone,))
                mysql.commit()
                Cursor.close()
                return redirect("/adm/menu")
        else:
            if file:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else :
                filename=''
            with mysql.cursor()as Cursor:
                Cursor.execute("SELECT id_sol FROM solicitacao")
                tudo = Cursor.fetchall()
                if len(tudo) >= 1 :
                    Cursor.execute("SELECT id_fechador FROM solicitacao ORDER BY id_sol DESC LIMIT 2")
                    ultimoChamado = Cursor.fetchall()
                    for x in range (len(allExec)):
                        if ultimoChamado[0] in allExec == True:
                                
                                if allExec[x] == ultimoChamado[0]:
                                    if allExec.index(allExec[x]) + 1 < len(allExec):
                                        
                                        a = allExec[x+1]

                                    elif allExec.index(allExec[x]) + 2 > len(allExec):
                                        
                                        a = allExec[0]

                                    elif allExec.index(allExec[x]) + 1 == len(allExec):
                                        
                                        a = allExec[-1]
                                                    
                                    
                                    Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,filename,pk_user,hora,a))
                                    mysql.commit()
                                    Cursor.close()
                                    return redirect("/adm/menu")

                        else:
                                
                                if allExec[x] == ultimoChamado[0]:
                                    if allExec.index(allExec[x]) + 1 < len(allExec):
                                                                                                     
                                        a = allExec[x+1]

                                    elif allExec.index(allExec[x]) + 2 > len(allExec):
                                        
                                        a = allExec[0]

                                    elif allExec.index(allExec[x]) + 1 == len(allExec):
                                        
                                        a = allExec[-1]
                                                    
                                    
                                    Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,filename,pk_user,hora,a))
                                    mysql.commit()
                                    Cursor.close()
                                    return redirect("/adm/menu")
                else:
                    for x in allExec:
                        Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,filename,pk_user,hora,x,))
                        mysql.commit()
                        Cursor.close()
                        return redirect("/adm/menu")

    return render_template('/nova-requisicao-adm.html',senha=senha,email=email,nome=nome)


@app.route('/executor/solicitacao', methods=['GET','POST'])
def novaExecutor():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_exec']
    nome=session['nome_exec']
    email = session['email_exec']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        Cursor.execute("SELECT id_user FROM user WHERE type_user = 'exec'and id_user != %s",(pk_user,))
        allExec = Cursor.fetchall()

    if request.method == 'POST':
        Details = request.form
        titulo = Details['titulo']
        descricao = Details['descricao']
        type_problem = Details['tipo']
        status_sol = 'Aberta'
        comentario= ''
        hora= datetime.datetime.now()
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
        else:
            filename=''
        if len(allExec) == 0:
            if file:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with mysql.cursor()as Cursor:
                
                Cursor.execute("INSERT INTO solicitacao (title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,type_problem,comentario,filename,pk_user,hora))
                mysql.commit()
                Cursor.close()
                return redirect("/executor/menu")

        elif len(allExec) == 1:
            execone = allExec[0]
            if file:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else :
                filename=''
            with mysql.cursor()as Cursor:
                Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,type_problem,comentario,filename,pk_user,hora,execone,))
                mysql.commit()
                Cursor.close()
                return redirect("/executor/menu")
        else:
            if file:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else :
                filename=''
            with mysql.cursor()as Cursor:
                Cursor.execute("SELECT id_sol FROM solicitacao")
                tudo = Cursor.fetchall()
                if len(tudo) > 1 :
                    Cursor.execute("SELECT id_fechador FROM solicitacao ORDER BY id_sol DESC LIMIT 2")
                    ultimoChamado = Cursor.fetchall()
                    for x in range (len(allExec)):
                        if ultimoChamado[0] in allExec == True:
                            
                            if allExec[x] == ultimoChamado[0]:
                                if allExec.index(allExec[x]) + 1 < len(allExec):
                                    
                                    a = allExec[x+1]

                                elif allExec.index(allExec[x]) + 2 > len(allExec):
                                    
                                    a = allExec[0]

                                elif allExec.index(allExec[x]) + 1 == len(allExec):
                                    
                                    a = allExec[-1]
                                                
                                
                                Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,type_problem,comentario,filename,pk_user,hora,a))
                                mysql.commit()
                                Cursor.close()
                                return redirect("/executor/menu")

                        else:
                            
                            if allExec[x] == ultimoChamado[0]:
                                if allExec.index(allExec[x]) + 1 < len(allExec):
                                    
                                    a = allExec[x+1]

                                elif allExec.index(allExec[x]) + 2 > len(allExec):
                                    
                                    a = allExec[0]

                                elif allExec.index(allExec[x]) + 1 == len(allExec):

                                    a = allExec[-1]
                                                
                                
                                Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,type_problem,comentario,filename,pk_user,hora,a))
                                mysql.commit()
                                Cursor.close()
                                return redirect("/executor/menu")


                elif len(tudo) == 1:
                    Cursor.execute("SELECT id_fechador FROM solicitacao ORDER BY id_sol DESC LIMIT 1")
                    ultimoChamado = Cursor.fetchall()
                    a = allExec[1]
                    
                    Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,type_problem,comentario,filename,pk_user,hora,a))
                    mysql.commit()
                    Cursor.close()
                    return redirect("/executor/menu")

                else:
                    for x in allExec:
                        Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,type_problem,comentario,filename,pk_user,hora,x,))
                        mysql.commit()
                        Cursor.close()
                        return redirect("/executor/menu")

    return render_template('/nova-requisicao-exec.html',nome=nome,senha=senha,email=email)


if __name__ == "__main__":
    app.run(debug=True)