from flask import Blueprint,render_template,request,redirect,session, url_for
from bd.db import mysql
import datetime

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/perfil_adm',methods=['POST'])
def perfil():
    pk_user = session['id_admin']
    Details = request.form
    nome_troca = Details['nome']
    email_troca = Details ['troca_email']
    troca_senha = Details ['troca_senha']
    session['nome_admin'] = nome_troca
    session['email_admin'] = email_troca

    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE user SET nome_user = %s, email_user=%s, pass_user = %s WHERE id_user = %s ",(nome_troca,email_troca,troca_senha,pk_user,))
        mysql.commit()
            
    return redirect(url_for('admin.adm'))


@admin.route('/adm')
def adm():
    if not 'loggedin' in session:
        return redirect ('/login')
    c = 'user'
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        Values = Cursor.execute("SELECT * FROM user")
        if Values > 0:
            Details = Cursor.fetchall()
            return render_template('/Controle-adm.html',Details=Details,Values=Values,c=c,senha = senha , email=email, nome = nome)
        else:
            return render_template('/Controle-adm.html', Values=Values,c=c,senha = senha , email=email, nome = nome)
    # return render_template('adm.html')

@admin.route('/adm/solicitacao',methods=['GET','POST'])
def index():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        if request.method == 'POST':
            Details = request.form
            titulo = Details['titulo']
            descricao = Details['descricao']
            tipo = Details['tipo']   
            status_sol = 'Aberta'
            comentario= ''
            hora= datetime.datetime.now()

            id_admin = session["id_admin"]
            Cursor.execute("INSERT INTO solicitacao(title_sol,desc_sol,status_sol,type_problem,comentario,id_user,data_inicio) VALUES(%s,%s,%s,%s,%s,%s,%s)",(titulo,descricao,status_sol,tipo,comentario,id_admin,hora,))
            mysql.commit()
            return redirect("/adm/menu")
    return render_template('/nova-requisicao-adm.html',senha=senha,email=email,nome=nome)


@admin.route('/adm/menu',methods=['GET','POST'])
def home():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        pk_user = session["id_admin"]
        Cursor.execute("SELECT id_user FROM solicitacao WHERE id_user = %s", (pk_user,))
        conta = Cursor.fetchone()
        cont_hardware=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Hardware' and id_user= %s",(pk_user,))
        cont_software= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Software' and id_user =%s", (pk_user,))
        cont_duv= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos'and id_user =%s", (pk_user,))

        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and id_user =%s",(pk_user,))
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and id_user =%s",(pk_user,))
        
        Values = Cursor.execute("SELECT * FROM solicitacao WHERE id_user= %s",(pk_user))
        if Values > 0:
            Details = Cursor.fetchall()
            return render_template('/home-adm.html', Details=Details,Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto=leitoraberto,leitorfechado=leitorfechado,conta=conta,senha = senha , email=email, nome = nome)
        else:
            return render_template('/home-adm.html', Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,pk_user=pk_user,senha = senha , email=email, nome = nome)

@admin.route("/adm/requisicoes",methods=["GET"])
def requisicoes():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()

        cont_hardware=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Hardware'")
        cont_software= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Software'")
        cont_duv= Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos'")

        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
        leitorandamento= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Andamento'")

        Values=Cursor.execute("SELECT * FROM solicitacao")
        if Values > 0:
            Details = Cursor.fetchall()
            
            return render_template('/requisicoes.html', Details=Details,Values=Values,cont_hardware = cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto = leitoraberto ,leitorfechado = leitorfechado ,leitorandamento=leitorandamento,senha = senha , email=email, nome = nome)
        return render_template('/requisicoes.html',Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,senha = senha , email=email, nome = nome)

@admin.route("/adm/estatisticas",methods=["GET"])
def estatisticas():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware'")
        tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software'")
        tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos'")

        num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
        num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
        num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
        num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
        num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")

        avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1'")
        avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2'")
        avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3'")
        avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4'")
        avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5'")

    return render_template("char.html",tipo_hardware=tipo_hardware,tipo_software=tipo_software,tipo_duvida=tipo_duvida,num_exec=num_exec,num_analise=num_analise,num_andamento=num_andamento,num_fechada=num_fechada,avaliacao_otimo=avaliacao_otimo,avaliacao_bom=avaliacao_bom,num_user=num_user,avaliacao_ruim=avaliacao_ruim,avaliacao_pessima=avaliacao_pessima,avaliacao_mediana=avaliacao_mediana,senha = senha , email=email, nome = nome)


@admin.route("/historico-avaliacao<id>")
def avaliacao(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and id_fechador =%s and avaliacao!=0 ",(id,))

        cont_hardware_adm =Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Hardware' and id_fechador =%s and avaliacao != 0 ",(id,))
        cont_software_adm = Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Software' and id_fechador =%s and avaliacao != 0 ",(id,))
        cont_duv_adm = Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and id_fechador =%s and avaliacao != 0 ",(id,))
        Cursor.execute("SELECT id_user FROM user WHERE id_user= %s ",(id))
        vai = Cursor.fetchone()
        Cursor.execute("SELECT nome_user FROM user WHERE id_user= %s ",(id))
        nomeuser = Cursor.fetchone()

        Cursor.execute("SELECT * FROM solicitacao WHERE id_fechador = %s",(id,))
        Details = Cursor.fetchall()
        Values=Cursor.execute("SELECT * FROM solicitacao WHERE id_fechador = %s",(id,))
        if Values > 0:
            Details = Cursor.fetchall()
            
        
    return render_template("/Historico-avaliacao.html",Values=Values,Details=Details,cont_hardware_adm=cont_hardware_adm,cont_software_adm=cont_software_adm,cont_duv_adm=cont_duv_adm,leitorfechado=leitorfechado,vai=vai,nome=nome,email=email,senha=senha,nomeuser=nomeuser)


@admin.route("/cargo<id>")
def cargo(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT type_user FROM user WHERE id_user =%s",(id,))
        eounaoe = Cursor.fetchone()
        if eounaoe[0] == "user":
            Cursor.execute("UPDATE user set type_user = 'exec' WHERE id_user = %s",(id,))
            mysql.commit()
            
        else:
            Cursor.execute("UPDATE user set type_user = 'user' WHERE id_user = %s",(id,))
            mysql.commit()
            
    return redirect(url_for("admin.adm"))

    
@admin.route("/view<id>")
def vizu(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and id_user =%s",(id,))
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and id_user =%s",(id,))
        leitorandamento= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Andamento' and id_user =%s",(id,))

        cont_hardware_adm =Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Hardware' and id_user =%s",(id,))
        cont_software_adm = Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Problemas de Software'and id_user =%s",(id,))
        cont_duv_adm = Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and id_user =%s",(id,))


        Cursor.execute("SELECT id_user FROM user WHERE id_user= %s ",(id))
        vai = Cursor.fetchone()

        Cursor.execute("SELECT nome_user FROM user WHERE id_user= %s ",(id))
        nomeuser = Cursor.fetchone()

        Cursor.execute("SELECT * FROM solicitacao WHERE id_user= %s",(id,))
        Details = Cursor.fetchall()

        Values=Cursor.execute("SELECT * FROM solicitacao WHERE id_user= %s",(id,))
        if Values > 0:
            Details = Cursor.fetchall()
            
    return render_template("/view_solicit_user.html",Values=Values,nome=nome,Details=Details,leitoraberto=leitoraberto,leitorfechado=leitorfechado,leitorandamento=leitorandamento,vai=vai,cont_software_adm=cont_software_adm,cont_hardware_adm=cont_hardware_adm, cont_duv_adm= cont_duv_adm,email=email,senha=senha, nomeuser=nomeuser)

@admin.route('/aceitando_adm/<id>', methods=['POST'])
def aceitar(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE solicitacao SET status_sol ='Andamento' WHERE id_sol = %s",(id,))
        mysql.commit()
        
    return redirect ('/adm/requisicoes')

@admin.route('/recusando_adm/<id>', methods=['POST'])
def recusando(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    formulario= request.form
    comentario= formulario['codigo']
    hora= datetime.datetime.now()
    nome= session['nome_admin']
    if comentario != None:
        with mysql.cursor()as Cursor:
            Cursor.execute("UPDATE solicitacao SET status_sol ='Fechada',data_final=%s,nome_exec=%s,comentario=%s WHERE id_sol = %s",(hora,nome,comentario,id,))
            mysql.commit()
            
    return redirect ('/adm/requisicoes')

@admin.route('/andamento_adm/<id>', methods=['POST'])
def fechamento(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    formulario= request.form
    comentario = formulario['comentario']
    hora= datetime.datetime.now()
    nome= session['nome_admin']
    if comentario != None:
        with mysql.cursor()as Cursor:
            Cursor.execute("UPDATE solicitacao SET status_sol ='Fechada',data_final=%s,nome_exec=%s,comentario=%s WHERE id_sol = %s",(hora,nome,comentario,id,))
            mysql.commit()
            
    return redirect ('/adm/requisicoes')
