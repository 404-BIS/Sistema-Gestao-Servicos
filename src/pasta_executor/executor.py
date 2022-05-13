from flask import Blueprint,render_template,request,redirect,session
from bd.db import mysql
import datetime

executor_blueprint= Blueprint('executor',__name__, template_folder='templates')

@executor_blueprint.route('/executor/solicitacao', methods=['GET','POST'])
def novaExecutor():
    if request.method == 'POST':
        Details = request.form
        titulo = Details['titulo']
        descricao = Details['descricao']
        type_problem = Details['tipo']   
        status_sol = 'Aberta'
        comentario= ''
        hora= datetime.datetime.now()
        with mysql.cursor()as Cursor:
            id_user = session["id_exec"]
            Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,id_user,data_inicio) VALUES(%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,type_problem,comentario,id_user,hora))
            mysql.commit()
            Cursor.close()
        return redirect("/executor/menu")
    return render_template('/nova-requisicao-exec.html')


@executor_blueprint.route('/executor/menu' , methods=['GET','POST'])
def exec():
    with mysql.cursor()as Cursor:
        pk_user = session["id_exec"]
        Cursor.execute("SELECT id_user FROM solicitacao WHERE id_user = %s", (pk_user,))
        conta = Cursor.fetchone()
    with mysql.cursor()as Cursor:    
        cont_hardware=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Hardware' and id_user= %s",(pk_user,))
        cont_software= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Software' and id_user =%s", (pk_user,))
        cont_duv= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and id_user =%s", (pk_user,))
        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and id_user =%s",(pk_user,))
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and id_user =%s",(pk_user,))
        Values = Cursor.execute("SELECT * FROM solicitacao WHERE id_user= %s",(pk_user,))
        if Values > 0:
            Details = Cursor.fetchall()
            return render_template('/home-exec.html', Details=Details,Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto=leitoraberto,leitorfechado=leitorfechado,conta=conta)
        else:
            return render_template('/home-exec.html', Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,pk_user=pk_user)
            
@executor_blueprint.route('/executor/chamadas-exec', methods=['GET','POST'])
def ExecChamada():
    with mysql.cursor()as Cursor:
        pk_user = session["id_exec"]
        Cursor.execute("SELECT id_user FROM solicitacao WHERE id_user = %s", (pk_user,))
        conta = Cursor.fetchone()
        
        cont_hardware=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Hardware'")
        cont_software= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Software'")
        cont_duv= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos'")

        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and not id_user =%s",(pk_user,))
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and not id_user =%s",(pk_user,))
        leitorandamento= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Andamento' and not id_user =%s",(pk_user,))

        Values=Cursor.execute("SELECT * FROM solicitacao")
    if Values > 0:
        Details = Cursor.fetchall()
        Cursor.close()
        return render_template('/chamadas-exec.html', Details=Details,Values=Values,cont_hardware = cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto = leitoraberto ,leitorfechado = leitorfechado ,leitorandamento=leitorandamento,conta=conta)
    return render_template('/chamadas-exec.html',Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,conta=conta)

@executor_blueprint.route('/aceitando/<id>', methods=['POST'])
def aceitar(id):
    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE solicitacao SET status_sol ='Andamento' WHERE id_sol = %s",(id,))
        mysql.commit()
        Cursor.close()
    return redirect ('/executor/chamadas-exec')

@executor_blueprint.route('/recusando/<id>', methods=['POST'])
def recusando(id):
    formulario= request.form
    comentario= formulario['codigo']
    hora= datetime.datetime.now()
    nome= session['nome_exec']
    id_de_qm_fechou = session['id_exec']
    if comentario != None:
        with mysql.cursor()as Cursor:
            Cursor.execute("UPDATE solicitacao SET status_sol ='Fechada',data_final=%s,nome_exec=%s,comentario=%s,id_de_quem_fechou=%s WHERE id_sol = %s",(hora,nome,comentario,id_de_qm_fechou,id,))
            mysql.commit()
            Cursor.close()
    return redirect ('/executor/chamadas-exec')

@executor_blueprint.route('/andamento/<id>', methods=['POST'])
def fechamento(id):
    formulario= request.form
    comentario = formulario['comentario']
    hora= datetime.datetime.now()
    nome= session['nome_exec']
    if comentario != None:
        with mysql.cursor()as Cursor:
            Cursor.execute("UPDATE solicitacao SET status_sol ='Fechada',data_final=%s,nome_exec=%s,comentario=%s WHERE id_sol = %s",(hora,nome,comentario,id,))
            mysql.commit()
            Cursor.close()
    return redirect ('/executor/chamadas-exec')

@executor_blueprint.route('/executor/<id>', methods=['POST'])
def delete(id):
    with mysql.cursor()as Cursor:
        Cursor.execute("DELETE FROM solicitacao WHERE id_sol = %s",(id,))
        mysql.commit()
        Cursor.close()
    return redirect('/executor/menu')
