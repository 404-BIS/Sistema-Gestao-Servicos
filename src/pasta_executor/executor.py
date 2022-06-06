from flask import Blueprint,render_template,request,redirect,session,url_for
from bd.db import mysql
import datetime

executor_blueprint= Blueprint('executor',__name__, template_folder='templates')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    

@executor_blueprint.route('/perfil_exec',methods=['POST'])
def perfil():
    pk_user = session['id_exec']
    Details = request.form
    nome_troca = Details['nome']
    email_troca = Details ['troca_email']
    troca_senha = Details ['troca_senha']
    session['nome_exec'] = nome_troca
    session['email_exec'] = email_troca

    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE user SET nome_user = %s, email_user=%s, pass_user = %s WHERE id_user = %s ",(nome_troca,email_troca,troca_senha,pk_user,))
        mysql.commit()
            
    return redirect(url_for('executor.exec'))



@executor_blueprint.route('/executor/menu' , methods=['GET','POST'])
def exec():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_exec']
    nome = session['nome_exec']
    email = session['email_exec']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        pk_user = session["id_exec"]
        Cursor.execute("SELECT id_user FROM solicitacao WHERE id_user = %s", (pk_user,))
        conta = Cursor.fetchone()  


        cont_hardware=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Hardware' and id_user= %s",(pk_user,))
        cont_software= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Software' and id_user =%s", (pk_user,))
        cont_duv= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and id_user =%s", (pk_user,))
        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and id_user =%s",(pk_user,))
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and id_user =%s",(pk_user,))
        Values = Cursor.execute("SELECT * FROM solicitacao WHERE id_user= %s order by id_sol DESC",(pk_user,))
        if Values > 0:
            Details = Cursor.fetchall()
            return render_template('/home-exec.html', Details=Details,Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto=leitoraberto,leitorfechado=leitorfechado,conta=conta,senha=senha,email=email, nome = nome)
        else:
            return render_template('/home-exec.html', Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,pk_user=pk_user,senha=senha,email=email, nome = nome )
            
@executor_blueprint.route('/executor/chamadas-exec', methods=['GET','POST'])
def ExecChamada():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_exec']
    nome = session['nome_exec']
    email = session['email_exec']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        pk_user = session["id_exec"]
        Cursor.execute("SELECT id_user FROM solicitacao WHERE id_user = %s", (pk_user,))
        conta = Cursor.fetchone()
        
        cont_hardware=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Hardware' and id_fechador= %s",(pk_user,))
        cont_software= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Software' and id_fechador= %s",(pk_user,))
        cont_duv= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and id_fechador= %s",(pk_user,))

        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and  id_fechador =%s",(pk_user,))
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and id_fechador= %s",(pk_user,))
        leitorandamento= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Andamento' and id_fechador= %s",(pk_user,))

        Values=Cursor.execute("SELECT * FROM solicitacao WHERE id_fechador=%s order by id_sol DESC",(pk_user,))

    if Values > 0:
        Details = Cursor.fetchall()
        
        return render_template('/chamadas-exec.html', Details=Details,Values=Values,cont_hardware = cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto = leitoraberto ,leitorfechado = leitorfechado ,leitorandamento=leitorandamento,conta=conta,pk_user=pk_user,senha=senha,email=email,nome=nome)
    return render_template('/chamadas-exec.html',Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,conta=conta,pk_user=pk_user,leitorfechado = leitorfechado,senha=senha,email=email,nome=nome)

@executor_blueprint.route('/aceitando/<id>', methods=['POST'])
def aceitar(id):
    
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session["id_exec"]
    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE solicitacao SET status_sol ='Andamento',id_fechador= %s WHERE id_sol = %s",(pk_user,id,))
        mysql.commit()
        
    return redirect ('/executor/chamadas-exec')

@executor_blueprint.route('/recusando/<id>', methods=['POST'])
def recusando(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    formulario= request.form
    comentario= formulario['codigo']
    hora= datetime.datetime.now()
    id_de_qm_fechou = session['id_exec']
    if comentario != None:
        with mysql.cursor()as Cursor:
            Cursor.execute("UPDATE solicitacao SET status_sol ='Fechada',data_final=%s,comentario=%s,id_fechador=%s WHERE id_sol = %s",(hora,comentario,id_de_qm_fechou,id,))
            mysql.commit()
            
    return redirect ('/executor/chamadas-exec')

@executor_blueprint.route('/andamento/<id>', methods=['POST'])
def fechamento(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    formulario= request.form
    comentario = formulario['comentario']
    hora= datetime.datetime.now()
    if comentario != None:
        with mysql.cursor()as Cursor:
            Cursor.execute("UPDATE solicitacao SET status_sol ='Fechada',data_final=%s,comentario=%s WHERE id_sol = %s",(hora,comentario,id,))
            mysql.commit()
            
    return redirect ('/executor/chamadas-exec')

@executor_blueprint.route('/executor/<id>', methods=['POST'])
def delete(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    with mysql.cursor()as Cursor:
        Cursor.execute("DELETE FROM solicitacao WHERE id_sol = %s",(id,))
        mysql.commit()
        
    return redirect('/executor/menu')