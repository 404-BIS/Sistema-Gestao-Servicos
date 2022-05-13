from flask import Blueprint,render_template,request,redirect,session
from flask_login import login_required, current_user
from bd.db import mysql
import datetime
user_blueprint= Blueprint('user', __name__ , template_folder='templates')


@user_blueprint.route('/usuario/solicitacao', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        Details = request.form
        titulo = Details['titulo']
        descricao = Details['descricao']
        tipo = Details['tipo']   
        status_sol = 'Aberta'
        comentario= ''
        hora= datetime.datetime.now()
        with mysql.cursor()as Cursor:
            id_user = session["id_user"]
            Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,id_user,data_inicio) VALUES(%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,id_user,hora,))
            mysql.commit()
            Cursor.close()
        return redirect("/usuario/menu")
    return render_template('/nova-requisicao-user.html')



@user_blueprint.route('/usuario/menu',methods=['GET','POST'])
def home():
    with mysql.cursor()as Cursor:
        pk_user = session["id_user"]
        Cursor.execute("SELECT id_user FROM solicitacao WHERE id_user = %s", (pk_user,))
        conta = Cursor.fetchone()
    with mysql.cursor()as Cursor:    
        cont_hardware=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Hardware' and id_user= %s",(pk_user,))
        cont_software= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Software' and id_user =%s", (pk_user,))
        cont_duv= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos'and id_user =%s", (pk_user,))
        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and id_user =%s",(pk_user,))
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and id_user =%s",(pk_user,))
        Values = Cursor.execute("SELECT * FROM solicitacao WHERE id_user= %s",(pk_user))
        if Values > 0:
            Details = Cursor.fetchall()
            return render_template('/home-user.html', Details=Details,Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto=leitoraberto,leitorfechado=leitorfechado,conta=conta)
        else:
            return render_template('/home-user.html', Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,pk_user=pk_user)

@user_blueprint.route('/avaliar/<id>', methods=['POST'])
def avaliacao(id):
    pessimo = request.form.get('pes')
    ruim = request.form.get('ruim')
    mediano = request.form.get('med')
    otimo = request.form.get('otimo')
    bom = request.form.get('bom')
    
    comentario_avaliacao= request.form['avaliacao']
    trocar = session["id_user"]
    x = [pessimo,ruim,mediano,bom,otimo]
    for i in x:
        if str(i) in "12345":
            print(id)
            with mysql.cursor()as Cursor:
                Cursor.execute("UPDATE solicitacao SET avaliacao =%s WHERE id_sol = %s ",(i,id,))
                mysql.commit()
                Cursor.close()
        
            
    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE solicitacao SET coment_avaliacao=%s WHERE id_sol = %s",(comentario_avaliacao,id,))
        mysql.commit()
        Cursor.close()
    return redirect ('/usuario/menu')
        
@user_blueprint.route('/usuario/<id>', methods=['POST'])
def delete(id):
    with mysql.cursor()as Cursor:
        Cursor.execute("DELETE FROM solicitacao WHERE id_sol=%s",(id,))
        mysql.commit()
        Cursor.close()
    return redirect('/usuario/menu')