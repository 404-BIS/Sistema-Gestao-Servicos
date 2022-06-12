from re import M
from zlib import DEF_BUF_SIZE
from flask import Blueprint,render_template,request,redirect,session, url_for
from bd.db import mysql
admin = Blueprint('admin', __name__, template_folder='templates')
import datetime


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def P(ANO, MES, DIA, PERIODO):
    M31 = [1, 3, 5, 7, 8, 10, 12]

    day = int(DIA) + PERIODO
    month = int(MES)
    year = int(ANO)
    DATA_FINAL = None
    print(day, month, year)

    if year % 4 == 0:
        if month == 2:
            if day + PERIODO > 28:
                day = day - 28
                month = month + 1
    elif year % 4 != 0:
        if month == '02':
            if day + PERIODO > 29:
                day = day - 29
                month = month + 1
    else:
        if day + PERIODO >31 and month in M31:
            day = day - 31
            month = month + 1
        elif day + PERIODO > 30 and month not in M31:
            day = day - 30
            month = month + 1

    if day < 10:
        if month < 10:
            DATA_FINAL = f'{year}-0{month}-0{day}'
        else:
            DATA_FINAL = f'{year}-{month}-0{day}'
    else:
        if month < 10:
            DATA_FINAL = f'{year}-0{month}-{day}'
        else:
            DATA_FINAL = f'{year}-{month}-{day}'
    return DATA_FINAL

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
        
        Values = Cursor.execute("SELECT * FROM solicitacao WHERE id_user= %s  order by id_sol DESC",(pk_user))
        if Values > 0:
            Details = Cursor.fetchall()
            return render_template('/home-adm.html',Details=Details,Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto=leitoraberto,leitorfechado=leitorfechado,conta=conta,senha=senha,email=email, nome=nome)
        else:
            return render_template('/home-adm.html', Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,pk_user=pk_user,senha=senha,email=email,nome =nome)

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

        Values=Cursor.execute("SELECT * FROM solicitacao order by id_sol DESC")
        if Values > 0:
            Details = Cursor.fetchall()
            
            return render_template('/requisicoes.html', Details=Details,Values=Values,cont_hardware = cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto = leitoraberto ,leitorfechado = leitorfechado ,leitorandamento=leitorandamento,senha = senha , email=email, nome = nome)
        return render_template('/requisicoes.html',Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,senha = senha , email=email, nome = nome)

@admin.route("/adm/estatisticas",methods=['GET'])
def estatisticas():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        # pegando infos do html    
        dias_select = request.args.get('days')
        dataaa = request.args.get('dataaa')
        # Conta
        DATA_ATUAL = dataaa
             # checking days
        if dataaa == '' or dataaa is None:
            DATA_ATUAL = str(datetime.date.today())
            ANO = DATA_ATUAL[:4]
            MES = DATA_ATUAL[5:7]
            DIA = int(DATA_ATUAL[8:])
            if dias_select == '1':
                DATA_FINAL = P(ANO, MES, DIA, 1)
                tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
            elif dias_select == '7':
                DATA_FINAL = P(ANO, MES, DIA, 7)
                tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
            elif dias_select == '15':
                DATA_FINAL = P(ANO, MES, DIA, 15)
                tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
            elif dias_select == '30':
                DATA_FINAL = P(ANO, MES, DIA, 30)
                tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
            else:
                tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware'")
                tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software'")
                tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos'")
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1'")
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2'")
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3'")
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4'")
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5'")
                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null")
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null")
                data_final = Cursor.fetchall()
                lista=[]
                listaa=[]
                listaaa=[]
                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
        else:
            ANO = DATA_ATUAL[:4]
            MES = DATA_ATUAL[5:7]
            DIA = int(DATA_ATUAL[8:])
            if dias_select == '1':
                DATA_FINAL = P(ANO, MES, DIA, 1)
                tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
            elif dias_select == '7':
                DATA_FINAL = P(ANO, MES, DIA, 7)
                tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
            elif dias_select == '15':
                DATA_FINAL = P(ANO, MES, DIA, 15)
                tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
            elif dias_select == '30':
                DATA_FINAL = P(ANO, MES, DIA, 30)
                print(DATA_FINAL)
                tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
                print(type(DATA_ATUAL), DATA_ATUAL, DATA_FINAL)
            else:
                tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware'")
                tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software'")
                tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos'")
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1'")
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2'")
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3'")
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4'")
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5'")
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()
                aberta=[]
                fecha=[]
                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null")
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null")
                data_final = Cursor.fetchall()
                lista=[]
                listaa=[]
                listaaa=[]
                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
        
        with mysql.cursor()as Cursor:
            oi=Cursor.execute("Select * from solicitacao where not avaliacao is null")
            if oi>0: 
                Cursor.execute("SELECT avg(avaliacao) from solicitacao where not avaliacao is null")
                final=Cursor.fetchone()
                final=round(final[0],1)
            else:
                final=0
        return render_template("char.html",tipo_hardware=tipo_hardware,tipo_software=tipo_software,tipo_duvida=tipo_duvida,num_exec=aporcentoExec,num_analise=num_analise,num_andamento=num_andamento,num_fechada=num_fechada,avaliacao_otimo=avaliacao_otimo,avaliacao_bom=avaliacao_bom,num_user=aporcentoUser,avaliacao_ruim=avaliacao_ruim,avaliacao_pessima=avaliacao_pessima,avaliacao_mediana=avaliacao_mediana,senha = senha , email=email, nome = nome, dataaa=dataaa,aporcentoUsers=aporcentoUsers,aporcentoExecs=aporcentoExecs,data_final=data_final,data_inicio=data_inicio,lista=lista,listaa=listaa,listaaa=listaaa)


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
        oi=Cursor.execute("Select * from solicitacao where id_fechador =%s and not avaliacao is null",(id,))
        if oi>0:
            Cursor.execute("SELECT avg(avaliacao) from solicitacao where id_fechador =%s",(id,))
            media=Cursor.fetchone()
            media=round(media[0],1)
        else:
            media=0
        Cursor.execute("SELECT * FROM solicitacao WHERE id_fechador = %s",(id,))
        Details = Cursor.fetchall()
        Values=Cursor.execute("SELECT * FROM solicitacao WHERE id_fechador = %s",(id,))
        if Values > 0:
            Details = Cursor.fetchall()
    return render_template("/Historico-avaliacao.html",Values=Values,Details=Details,cont_hardware_adm=cont_hardware_adm,cont_software_adm=cont_software_adm,cont_duv_adm=cont_duv_adm,leitorfechado=leitorfechado,vai=vai,nome=nome,email=email,senha=senha,nomeuser=nomeuser,media=media)


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
            Cursor.execute("SELECT id_sol FROM solicitacao WHERE id_fechador =%s and status_sol = 'Andamento'",(id,))
            solicitacaoAndamento = Cursor.fetchall()
            Cursor.execute("SELECT id_user FROM user WHERE type_user = 'exec'") 
            allExec = Cursor.fetchall()
            x = 0
            for z in range(len(solicitacaoAndamento)):
                Cursor.execute("UPDATE solicitacao SET status_sol ='Aberta' WHERE id_sol = %s",(solicitacaoAndamento[z]))
                mysql.commit()
            Cursor.execute("SELECT id_sol FROM solicitacao WHERE id_fechador =%s and status_sol = 'Aberta'",(id,))
            solicitacaoExe = Cursor.fetchall()
            for i in range (len(solicitacaoExe)):

                if len(allExec) == 0:
                    Cursor.execute("UPDATE solicitacao set id_fechador = NULL WHERE id_sol = %s",(solicitacaoExe[i][0],))
                    mysql.commit()
                elif len (allExec) == 1:
                    Cursor.execute("UPDATE solicitacao set id_fechador = %s WHERE id_sol = %s",(allExec[0][0],solicitacaoExe[i][0],))
                    mysql.commit()
                else:
                    if allExec.index(allExec[x]) == 0:
                        a = allExec[0]
                        x += 1
                    elif allExec.index(allExec[x]) + 1 < len(allExec):
                        a = allExec[x+1]
                        x += 1
                    elif allExec.index(allExec[x]) + 1 == len(allExec):
                        a = allExec[-1]
                        x = 0
            
                    Cursor.execute("UPDATE solicitacao set id_fechador = %s WHERE id_sol = %s",(a,solicitacaoExe[i][0]))
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
    pk_user = session['id_admin']
    if not 'loggedin' in session:
        return redirect ('/login')
    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE solicitacao SET status_sol ='Andamento',id_fechador=%s WHERE id_sol = %s",(pk_user,id,))
        mysql.commit()
        
    return redirect ('/adm/requisicoes')

@admin.route('/recusando_adm/<id>', methods=['POST'])
def recusando(id):
    pk_user = session['id_admin']
    if not 'loggedin' in session:
        return redirect ('/login')
    formulario= request.form
    comentario= formulario['codigo']
    hora= datetime.datetime.now()

    if comentario != None:
        with mysql.cursor()as Cursor:
            Cursor.execute("UPDATE solicitacao SET status_sol ='Fechada',data_final=%s,comentario=%s,id_fechador=%s WHERE id_sol = %s",(hora,comentario,pk_user,id,))
            mysql.commit()
            
    return redirect ('/adm/requisicoes')

@admin.route('/andamento_adm/<id>', methods=['POST'])
def fechamento(id):
    pk_user = session['id_admin']
    if not 'loggedin' in session:
        return redirect ('/login')
    formulario= request.form
    comentario = formulario['comentario']
    hora= datetime.datetime.now()
    if comentario != None:
        with mysql.cursor()as Cursor:
            Cursor.execute("UPDATE solicitacao SET status_sol ='Fechada',data_final=%s,comentario=%s,id_fechador=%s WHERE id_sol = %s",(hora,comentario,pk_user,id,))
            mysql.commit()
            
    return redirect ('/adm/requisicoes')


@admin.route('/adm/<id>', methods=['POST'])
def delete(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    with mysql.cursor()as Cursor:
        Cursor.execute("DELETE FROM solicitacao WHERE id_sol=%s",(id,))
        mysql.commit()
        Cursor.close()
    return redirect('/adm/menu')