from flask import Blueprint,render_template,request,redirect

from db import mysql

user_blueprint= Blueprint('user', __name__ , template_folder='templates')

@user_blueprint.route('/')
def MainHome():
    return redirect('/usuario/menu')

@user_blueprint.route('/usuario/solicitacao', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        Details = request.form
        titulo = Details['titulo']
        descricao = Details['descricao']
        tipo = Details['tipo']
        condicao = 'Aberta'
        comentario= ''

        with mysql.cursor()as Cursor:
            Cursor.execute("INSERT INTO requisicao(titulo, descricao,tipo,condicao,comentario) VALUES(%s,%s,%s,%s,%s)",(titulo,descricao,tipo,condicao,comentario))
            mysql.commit()
            
        return redirect("/usuario/menu")
    return render_template('/nova-requisicao-user.html')


@user_blueprint.route('/usuario/menu')
def home():
    with mysql.cursor()as Cursor:
        aberta= Cursor.execute("SELECT * FROM requisicao")
        cont_hardware=Cursor.execute("SELECT tipo FROM requisicao WHERE tipo='Problemas de Hardware'")
        cont_software= Cursor.execute("SELECT tipo FROM requisicao WHERE tipo='Problemas de Software'")
        cont_duv= Cursor.execute("SELECT tipo FROM requisicao WHERE tipo='Duvidas ou Esclarecimentos'")
        leitoraberto= Cursor.execute("SELECT * FROM requisicao WHERE condicao='Aberta'")
        leitorfechado= Cursor.execute("SELECT * FROM requisicao WHERE condicao='Fechada'")
        Values = Cursor.execute("SELECT * FROM requisicao")
    if Values > 0:
        Details = Cursor.fetchall()
        return render_template('/home-user.html', Details=Details,Values=Values,aberta=aberta,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto=leitoraberto,leitorfechado=leitorfechado)
    else:
        return render_template('/home-user.html', Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv)

@user_blueprint.route('/usuario/<id>', methods=['POST'])
def delete(id):
    with mysql.cursor()as Cursor:
        Cursor.execute("DELETE FROM requisicao WHERE id_requisicao=%s",(id,))
        mysql.commit()
        Cursor.close
    return redirect('/usuario/menu')