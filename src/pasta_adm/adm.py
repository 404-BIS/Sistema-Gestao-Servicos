from flask import Blueprint,render_template,request,redirect,session, url_for
from bd.db import mysql
admin = Blueprint('admin', __name__, template_folder='templates')
import datetime


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        mescom31 = ['01', '03', '05', '07', '08', '10', '12']    
        dias_select = request.args.get('days')
        dataaa = request.args.get('dataaa')
        # Conta
        DATA_ATUAL = dataaa
             # checking days
        if dataaa == '':
            DATA_ATUAL = '2022-06-06'
        if dias_select == '1':
            ano = DATA_ATUAL[:4]
            mes = DATA_ATUAL[5:7]
            dia = int(DATA_ATUAL[8:])
            print(dia, mes, ano)
            if (dia - 1 <= 0):
                if int(ano) %4 == 0:
                    if mes == '02':
                        cdias = (dia - 1)*(-1)
                        dia = 29 + cdias
                        mes = '01'
                elif int(ano) %4 != 0:
                    if mes == '02':
                        cdias = (dia - 1)*(-1)
                        dia = 28 + cdias
                        mes = '01'
                elif mes in mescom31:
                    cdias = (dia - 1)*(-1)
                    dia = 31 + cdias
                    mes = int(mes)
                    mess=mes-1
                    mes = '0' + str(mess)
                else:
                    cdias = (dia - 1)*(-1)
                    dia = 30 + cdias
                    mes = int(mes)
                    mess=mes-1
                    mes = '0' + str(mess)
            MENOS_1 = f"{ano}-{mes}-{dia-1}"
            print(MENOS_1)

            tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware' and data_inicio between %s and %s", (MENOS_1, DATA_ATUAL,))

            tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software' and data_inicio between %s and %s", (MENOS_1, DATA_ATUAL,))

            tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and data_inicio between %s and %s", (MENOS_1, DATA_ATUAL,))

            num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
            num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
            totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
            totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
            
            num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (MENOS_1, DATA_ATUAL,))
            num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (MENOS_1, DATA_ATUAL,))
            num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (MENOS_1, DATA_ATUAL,))
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
    
    


            avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (MENOS_1, DATA_ATUAL,))
            avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (MENOS_1, DATA_ATUAL,))
            avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (MENOS_1, DATA_ATUAL,))
            avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (MENOS_1, DATA_ATUAL,))
            avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (MENOS_1, DATA_ATUAL,))
        elif dias_select == '7':
            ano = DATA_ATUAL[:4]
            mes = DATA_ATUAL[5:7]
            dia = int(DATA_ATUAL[8:])   
            if (dia - 7 <= 0):
                if int(ano) %4 == 0:
                    if int(ano) %4 == 0:
                        if mes == '02':
                            cdias = (dia - 7)*(-1)
                            dia = 29 + cdias
                            mes = '01'
                elif int(ano) %4 != 0:
                    if mes == '02':
                        cdias = (dia - 7)*(-1)
                        dia = 28 + cdias
                        mes = '01'
                    else:
                        cdias = (dia - 7)*(-1)
                        dia = 28 + cdias
                        mes = '01'
                elif mes in mescom31:
                    cdias = (dia - 7)*(-1)
                    dia = 31 + cdias
                    mes = int(mes)
                    mess=mes-1
                    mes = '0' + str(mess)
                else:
                    cdias = (dia - 7)*(-1)
                    dia = 30 + cdias
                    mes = int(mes)
                    mess=mes-1
                    mes = '0' + str(mess)
            MENOS_7 = (f"{ano}-{mes}-{dia-7}")
            print(MENOS_7)
        
            tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware' and data_inicio between %s and %s", (MENOS_7, DATA_ATUAL,))

            tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software' and data_inicio between %s and %s", (MENOS_7, DATA_ATUAL,))

            tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and data_inicio between %s and %s", (MENOS_7, DATA_ATUAL,))

            num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
            num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
            num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (MENOS_7, DATA_ATUAL,))
            num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (MENOS_7, DATA_ATUAL,))
            num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (MENOS_7, DATA_ATUAL,))
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
    
    


            avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (MENOS_7, DATA_ATUAL,))
            avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (MENOS_7, DATA_ATUAL,))
            avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (MENOS_7, DATA_ATUAL,))
            avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (MENOS_7, DATA_ATUAL,))
            avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (MENOS_7, DATA_ATUAL,))
        elif dias_select == '15':
            ano = DATA_ATUAL[:4]
            mes = DATA_ATUAL[5:7]
            dia = int(DATA_ATUAL[8:])
            if (dia - 15 <= 0):
                if int(ano) %4 == 0:
                    if mes == '02':
                        cdias = (dia - 15)*(-1)
                        dia = 29 + cdias
                        mes = '01'
                elif int(ano) %4 != 0:
                    if mes == '02':
                        cdias = (dia - 15)*(-1)
                        dia = 28 + cdias
                        mes = '01'
                    else:
                        cdias = (dia - 15)*(-1)
                        dia = 28 + cdias
                        mes = '01'
                elif mes in mescom31:
                    cdias = (dia - 15)*(-1)
                    dia = 31 + cdias
                    mes = int(mes)
                    mess=mes-1
                    mes = '0' + str(mess)
                else:
                    cdias = (dia - 15)*(-1)
                    dia = 30 + cdias
                    mes = int(mes)
                    mess=mes-1
                    mes = '0' + str(mess)
            MENOS_15 = (f"{ano}-{mes}-{dia-15}")
        
            tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware' and data_inicio between %s and %s", (MENOS_15, DATA_ATUAL,))

            tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software' and data_inicio between %s and %s", (MENOS_15, DATA_ATUAL,))

            tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and data_inicio between %s and %s", (MENOS_15, DATA_ATUAL,))

            num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
            num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
            num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (MENOS_15, DATA_ATUAL,))
            num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (MENOS_15, DATA_ATUAL,))
            num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (MENOS_15, DATA_ATUAL,))
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
    
    


            avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (MENOS_15, DATA_ATUAL,))
            avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (MENOS_15, DATA_ATUAL,))
            avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (MENOS_15, DATA_ATUAL,))
            avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (MENOS_15, DATA_ATUAL,))
            avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (MENOS_15, DATA_ATUAL,))

        elif dias_select == '30':
            ano = DATA_ATUAL[:4]
            mes = DATA_ATUAL[5:7]
            dia = int(DATA_ATUAL[8:])
            if (dia - 30 <= 0):
                if int(ano) %4 == 0:
                    if mes == '02':
                        cdias = (dia - 30)*(-1)
                        dia = 29 + cdias
                        mes = '01'
                    else:
                        cdias = (dia - 30)*(-1)
                        dia = 28 + cdias
                        mes = '01'
                elif mes in mescom31:
                    cdias = (dia - 30)*(-1)
                    dia = 31 + cdias
                    mes = int(mes)
                    mess=mes-1
                    mes = '0' + str(mess)
                else:
                    cdias = (dia - 30)*(-1)
                    dia = 30 + cdias
                    mes = int(mes)
                    mess= mes-1
                    mes = '0' + str(mess)
            MENOS_30 = (f"{ano}-{mes}-{dia-30}")
            tipo_hardware=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Hardware' and data_inicio between %s and %s", (MENOS_30, DATA_ATUAL,))

            tipo_software=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Problemas de Software' and data_inicio between %s and %s", (MENOS_30, DATA_ATUAL,))

            tipo_duvida=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Duvidas ou Esclarecimentos' and data_inicio between %s and %s", (MENOS_30, DATA_ATUAL,))
            seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
            seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")

            num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
            num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
            num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (MENOS_30, DATA_ATUAL,))
            num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (MENOS_30, DATA_ATUAL,))
            num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (MENOS_30, DATA_ATUAL,))

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
    


            avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (MENOS_30, DATA_ATUAL,))
            avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (MENOS_30, DATA_ATUAL,))
            avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (MENOS_30, DATA_ATUAL,))
            avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (MENOS_30, DATA_ATUAL,))
            avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (MENOS_30, DATA_ATUAL,))
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
        # p = []
        # z = 0
        # a=[]
        # for s in range(len(data_inicio)):
            
        #     # if s == 0:
        #     #     p.append(data_inicio[0][0])
        #     # elif data_inicio[s][0] != p[0]:
        #     #     p.append(data_inicio[s][0])
        lista=[]
        listaa=[]
        listaaa=[]

        # for n in range(len(data_inicio)):
        #     # temporario = data_inicio[n]
        
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
            # a.append(Cursor.execute("SELECT * FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,)))
            # a.append(Cursor.execute("SELECT * FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,)))
            # a.append(h)
        
        with mysql.cursor()as Cursor:
            oi=Cursor.execute("Select * from solicitacao where not avaliacao is null")
            if oi>0: 
                Cursor.execute("SELECT avg(avaliacao) from solicitacao where not avaliacao is null")
                final=Cursor.fetchone()
                final=round(final[0],1)
            else:
                final=0
        
        if lista or listaa or listaaa == []:
            lista = ['sem registro']
            listaa = ['sem registro']
            listaaa = ['sem registro']
        return render_template("char.html", num_andamentoo=num_andamentoo, num_fechadaa=num_fechadaa,tipo_hardware=tipo_hardware,tipo_software=tipo_software,tipo_duvida=tipo_duvida,num_exec=aporcentoExec,num_analise=num_analise,num_andamento=num_andamento,num_fechada=num_fechada,avaliacao_otimo=avaliacao_otimo,avaliacao_bom=avaliacao_bom,num_user=aporcentoUser,avaliacao_ruim=avaliacao_ruim,avaliacao_pessima=avaliacao_pessima,avaliacao_mediana=avaliacao_mediana,senha = senha , email=email, nome = nome, dataaa=dataaa,aporcentoUsers=aporcentoUsers,aporcentoExecs=aporcentoExecs,aberta=aberta,fecha=fecha,data_final=data_final,data_inicio=data_inicio,final=final,lista=lista,listaa=listaa,listaaa=listaaa)


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