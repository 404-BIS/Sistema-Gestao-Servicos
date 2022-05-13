from flask import Blueprint,render_template,request,redirect,session, url_for
from flask_login import login_required, current_user
from bd.db import mysql
import datetime

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/adm')
def adm():
    pk_user = session["id_admin"]
    c = 'user'
    with mysql.cursor()as Cursor:    
        Values = Cursor.execute("SELECT * FROM user")
        if Values > 0:
            Details = Cursor.fetchall()
            return render_template('/Controle-adm.html',Details=Details,Values=Values,c=c)
        else:
            return render_template('/Controle-adm.html', Values=Values,c=c)
    # return render_template('adm.html')

@admin.route('/adm/solicitacao',methods=['GET','POST'])
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
            id_user = session["id_admin"]
            Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,id_user,data_inicio) VALUES(%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,id_user,hora,))
            mysql.commit()
            Cursor.close()
        return redirect("/adm/menu")
    return render_template('/nova-requisicao-adm.html')


@admin.route('/adm/menu',methods=['GET','POST'])
def home():
    with mysql.cursor()as Cursor:
        pk_user = session["id_admin"]
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
            return render_template('/home-adm.html', Details=Details,Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto=leitoraberto,leitorfechado=leitorfechado,conta=conta)
        else:
            return render_template('/home-adm.html', Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,pk_user=pk_user)

@admin.route("/adm/requisicoes",methods=["GET"])
def requisicoes():
    with mysql.cursor()as Cursor:
        # pk_user = session["id_exec"]
        cont_hardware=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Hardware'")
        cont_software= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Software'")
        cont_duv= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos'")

        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
        leitorandamento= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Andamento'")

        Values=Cursor.execute("SELECT * FROM solicitacao")
    if Values > 0:
        Details = Cursor.fetchall()
        Cursor.close()
        return render_template('/requisicoes.html', Details=Details,Values=Values,cont_hardware = cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto = leitoraberto ,leitorfechado = leitorfechado ,leitorandamento=leitorandamento)
    return render_template('/requisicoes.html',Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv)

@admin.route("/adm/estatisticas",methods=["GET"])
def estatisticas():
    with mysql.cursor()as Cursor:
        Values=Cursor.execute("SELECT * FROM solicitacao")
    return render_template("/estatisticas.html")


@admin.route("/historico-avaliacao<id>")
def avaliacao(id):
    with mysql.cursor()as Cursor:
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and id_de_quem_fechou =%s",(id,))

        cont_hardware_adm =Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Hardware' and id_de_quem_fechou =%s",(id,))
        cont_software_adm = Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Software' and id_de_quem_fechou =%s",(id,))
        cont_duv_adm = Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and id_de_quem_fechou =%s",(id,))
        print(cont_software_adm)
        with mysql.cursor()as Cursor:
            Cursor.execute("SELECT nome_user FROM user WHERE id_user= %s",(id,))
            nome=Cursor.fetchone()

        with mysql.cursor()as Cursor:
            Cursor.execute("SELECT id_user FROM user WHERE id_user= %s ",(id))
            vai = Cursor.fetchone()

        with mysql.cursor()as Cursor: 
            Values=Cursor.execute("SELECT * FROM solicitacao WHERE id_de_quem_fechou = %s",(id,))
            if Values > 0:
                Details = Cursor.fetchall()
                Cursor.close()
            
    return render_template("/Historico-avaliacao.html",cont_hardware_adm=cont_hardware_adm,cont_software_adm=cont_software_adm,cont_duv_adm=cont_duv_adm,leitorfechado=leitorfechado,Details=Details,vai=vai,nome=nome)


@admin.route("/cargo<id>")
def cargo(id):
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT type_user FROM user WHERE id_user =%s",(id,))
        eounaoe = Cursor.fetchone()
        if eounaoe[0] == "user":
            Cursor.execute("UPDATE user set type_user = 'exec' WHERE id_user = %s",(id,))
            mysql.commit()
            Cursor.close()
        else:
            Cursor.execute("UPDATE user set type_user = 'user' WHERE id_user = %s",(id,))
            mysql.commit()
            Cursor.close()
    return redirect(url_for("admin.adm"))

# @admin.route('/visualizar')
# def visualizar():
    
    
    
@admin.route("/view<id>")
def vizu(id):
    with mysql.cursor()as Cursor:
        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and id_user =%s",(id,))
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and id_user =%s",(id,))
        leitorandamento= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Andamento' and id_user =%s",(id,))

        cont_hardware_adm =Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Hardware' and id_user =%s",(id,))
        cont_software_adm = Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Software'and id_user =%s",(id,))
        cont_duv_adm = Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and id_user =%s",(id,))

    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT id_user FROM user WHERE id_user= %s ",(id))
        vai = Cursor.fetchone()
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT nome_user FROM user WHERE id_user= %s",(id,))
        nome=Cursor.fetchone()
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT * FROM solicitacao WHERE id_user= %s",(id,))
        Details = Cursor.fetchall()
    with mysql.cursor()as Cursor: 
        Values=Cursor.execute("SELECT * FROM solicitacao WHERE id_user= %s",(id,))
        if Values > 0:
            Details = Cursor.fetchall()
            Cursor.close()
    return render_template("/view_solicit_user.html",Values=Values,nome=nome,Details=Details,leitoraberto=leitoraberto,leitorfechado=leitorfechado,leitorandamento=leitorandamento,vai=vai,cont_software_adm=cont_software_adm,cont_hardware_adm=cont_hardware_adm, cont_duv_adm= cont_duv_adm)





@admin.route('/aceitando/<id>', methods=['POST'])
def aceitar(id):
    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE solicitacao SET status_sol ='Andamento' WHERE id_sol = %s",(id,))
        mysql.commit()
        Cursor.close()
    return redirect ('/executor/chamadas-exec')

@admin.route('/recusando/<id>', methods=['POST'])
def recusando(id):
    formulario= request.form
    comentario= formulario['codigo']
    hora= datetime.datetime.now()
    nome= session['nome_exec']
    if comentario != None:
        with mysql.cursor()as Cursor:
            Cursor.execute("UPDATE solicitacao SET status_sol ='Fechada',data_final=%s,nome_exec=%s,comentario=%s WHERE id_sol = %s",(hora,nome,comentario,id,))
            mysql.commit()
            Cursor.close()
    return redirect ('/executor/chamadas-exec')

@admin.route('/andamento/<id>', methods=['POST'])
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
