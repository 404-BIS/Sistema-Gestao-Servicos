from flask import Blueprint,render_template,request,redirect,session,url_for
from flask_login import login_required, current_user
from bd.db import mysql

user_blueprint= Blueprint('user', __name__ , template_folder='templates')
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@user_blueprint.route('/perfil',methods=['POST'])
def perfil():
    pk_user = session['id_user']
    Details = request.form
    nome_troca = Details['nome']
    email_troca = Details ['troca_email']
    troca_senha = Details ['troca_senha']
    session['nome_user'] = nome_troca
    session['email_user'] = email_troca

    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE user SET nome_user = %s, email_user=%s, pass_user = %s WHERE id_user = %s ",(nome_troca,email_troca,troca_senha,pk_user,))
        mysql.commit()
        Cursor.close()    
    return redirect(url_for('user.home'))



# @user_blueprint.route('/usuario/solicitacao', methods=['GET','POST'])
# def index():
#     if not 'loggedin' in session:
#         return redirect ('/login')
#     pk_user = session['id_user']
#     nome = session['nome_user']
#     email = session['email_user']
#     with mysql.cursor()as Cursor:
#         Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
#         senha = Cursor.fetchone()
#         Cursor.execute("SELECT id_user FROM user WHERE type_user = 'exec'")
#         allExec = Cursor.fetchall()

#     if request.method == 'POST':
#         Details = request.form
#         titulo = Details['titulo']
#         descricao = Details['descricao']
#         tipo = Details['tipo']   
#         status_sol = 'Aberta'
#         comentario= ''
#         hora= datetime.datetime.now()
#         file = request.files['file']
#         filename = secure_filename(file.filename)
#         if len(allExec) == 0:
#             with mysql.cursor()as Cursor:
#                 Cursor.execute("INSERT INTO solicitacao (title_sol, desc_sol, status_sol ,type_problem, comentario,foto, data_inicio, id_user) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,filename,hora,pk_user)) 
#                 mysql.commit()
#                 # Cursor.execute("UPDATE solicitacao set foto=%s",(filename,))
#                 # mysql.commit()
#                 Cursor.close()
#                 return redirect("/usuario/menu")

#         elif len(allExec) == 1:
#             execone = allExec[0]
#             with mysql.cursor()as Cursor:
#                 Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) ",(titulo,descricao,status_sol,tipo,comentario,filename,pk_user,hora,execone,))
#                 mysql.commit()
#                 Cursor.close()
#                 return redirect("/salvar",methods=['POST'])
#         else:
#             with mysql.cursor()as Cursor:
#                 Cursor.execute("SELECT id_sol FROM solicitacao")
#                 tudo = Cursor.fetchall()
#                 if len(tudo) >= 1 :
#                     Cursor.execute("SELECT id_fechador FROM solicitacao ORDER BY id_sol DESC LIMIT 2")
#                     ultimoChamado = Cursor.fetchall()
#                     for x in range (len(allExec)):
#                         if ultimoChamado[0] in allExec == True:
#                                 print(ultimoChamado[0])
#                                 print(allExec)
#                                 if allExec[x] == ultimoChamado[0]:
#                                     if allExec.index(allExec[x]) + 1 < len(allExec):
#                                         print(allExec.index(allExec[x]),'== Primeira cond')
#                                         print(allExec[x])
#                                         a = allExec[x+1]

#                                     elif allExec.index(allExec[x]) + 2 > len(allExec):
#                                         print('segunda faixa')
#                                         a = allExec[0]

#                                     elif allExec.index(allExec[x]) + 1 == len(allExec):
#                                         print('terceira faixa')
#                                         print(allExec.index(allExec[x]))
#                                         print(allExec[x])
#                                         print(len(allExec))
#                                         a = allExec[-1]
                                                    
                                    
#                                     Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,filename,pk_user,hora,a))
#                                     mysql.commit()
#                                     Cursor.close()
#                                     return redirect("/usuario/menu")

#                         else:
#                                 print(allExec[x],ultimoChamado)
#                                 if allExec[x] == ultimoChamado[0]:
#                                     if allExec.index(allExec[x]) + 1 < len(allExec):
#                                         print('Diferente 1')
#                                         print(allExec.index(allExec[x]))
#                                         print(allExec[x])
                                    
                                        
#                                         print(len(allExec))
#                                         a = allExec[x+1]

#                                     elif allExec.index(allExec[x]) + 2 > len(allExec):
#                                         print('diferente 2')
#                                         a = allExec[0]

#                                     elif allExec.index(allExec[x]) + 1 == len(allExec):
#                                         print('diferente 3')
#                                         print(allExec.index(allExec[x]))
#                                         print(allExec[x])
#                                         print(len(allExec))
#                                         a = allExec[-1]
                                                    
                                    
#                                     Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,filename,pk_user,hora,a))
#                                     mysql.commit()
#                                     Cursor.close()
#                                     return redirect("/usuario/menu")
#                 else:
#                     for x in allExec:
#                         Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,foto,id_user,data_inicio,id_fechador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,filename,pk_user,hora,x,))
#                         mysql.commit()
#                         Cursor.close()
#                         return redirect("/usuario/menu")

#     return render_template('/nova-requisicao-user.html',nome=nome,email=email,senha=senha)

@user_blueprint.route('/usuario/menu',methods=['GET','POST'])
def home():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_user']
    nome = session['nome_user']
    email = session['email_user']
    with mysql.cursor()as Cursor:
        # Cursor.execute("SELECT id sol from solicitacao WHERE id_user = %s",(pk_user))
        # allSolicitacao = Cursor.fetchall()

        Cursor.execute("SELECT * from solicitacao")
        image = Cursor.fetchall()

        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        Cursor.execute("SELECT id_user FROM user WHERE id_user = %s", (pk_user,))
        conta = Cursor.fetchone() 
        cont_hardware=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Hardware' and id_user= %s",(pk_user,))
        cont_software= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Software' and id_user =%s", (pk_user,))
        cont_duv= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos'and id_user =%s", (pk_user,))
        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and id_user =%s",(pk_user,))
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and id_user =%s",(pk_user,))
        Values = Cursor.execute("SELECT * FROM solicitacao WHERE id_user= %s",(pk_user,))
        if Values > 0:
            Details = Cursor.fetchall()
            return render_template('/home-user.html', Details=Details,Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto=leitoraberto,leitorfechado=leitorfechado,conta=conta,nome=nome,email=email,pk_user=pk_user,senha=senha,filename=image)
        else:
            return render_template('/home-user.html', Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,pk_user=pk_user,conta=conta,nome=nome,email=email,senha=senha)

@user_blueprint.route('/avaliar/<id>', methods=['POST'])
def avaliacao(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    pessimo = request.form.get('pes')
    ruim = request.form.get('ruim')
    mediano = request.form.get('med')
    otimo = request.form.get('otimo')
    bom = request.form.get('bom')
    
    comentario_avaliacao= request.form['avaliacao']
    x = [pessimo,ruim,mediano,bom,otimo]
    for i in x:
        if str(i) in "12345":
            with mysql.cursor()as Cursor:
                Cursor.execute("UPDATE solicitacao SET avaliacao =%s WHERE id_sol = %s ",(i,id,))
                mysql.commit()
                Cursor.close()
    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE solicitacao SET coment_avaliacao=%s WHERE id_sol = %s",(comentario_avaliacao,id,))
        mysql.commit()
        Cursor.close()
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT id_user from solicitacao WHERE id_sol=%s",(id,))
        a= Cursor.fetchone()
        Cursor.execute("SELECT type_user from user WHERE id_user= %s",(a,))
        teste = Cursor.fetchone()
        Cursor.close()
        if teste[0] == 'user':
            return redirect ('/usuario/menu')
        elif teste[0] == 'exec':
            return redirect ('/executor/menu')
        else:
            return redirect ('/adm/menu')

            
        
@user_blueprint.route('/usuario/<id>', methods=['POST'])
def delete(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    with mysql.cursor()as Cursor:
        Cursor.execute("DELETE FROM solicitacao WHERE id_sol=%s",(id,))
        mysql.commit()
        Cursor.close()
    return redirect('/usuario/menu')




