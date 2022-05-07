from flask import Blueprint,render_template,request,redirect
from db import mysql


executor_blueprint= Blueprint('executor',__name__, template_folder='templates')

@executor_blueprint.route('/executor/solicitacao', methods=['GET','POST'])
def novaExecutor():
    if request.method == 'POST':
        Details = request.form
        titulo = Details['titulo']
        tipo = Details['tipo']
        descricao = Details['descricao']
        condicao = 'Aberta'
        with mysql.cursor()as Cursor:
            Cursor.execute("INSERT INTO requisicao_exec(titulo, descricao,tipo,condicao) VALUES(%s,%s,%s,%s)",(titulo,descricao,tipo,condicao))
            mysql.commit()
            Cursor.close()
        return redirect("/executor/menu")
    return render_template('/nova-requisicao-exec.html')


@executor_blueprint.route('/executor/menu' , methods=['GET','POST'])
def executor():
    with mysql.cursor()as Cursor:
        aberta= Cursor.execute("SELECT * FROM requisicao_exec")
        cont_hardware= Cursor.execute("SELECT tipo FROM requisicao_exec WHERE tipo='Problemas de Hardware'")
        cont_software= Cursor.execute("SELECT tipo FROM requisicao_exec WHERE tipo='Problemas de Software'")
        cont_duv= Cursor.execute("SELECT tipo FROM requisicao_exec WHERE tipo='Duvidas ou Esclarecimentos'")
        leitoraberto= Cursor.execute("SELECT * FROM requisicao_exec WHERE condicao='Aberta'")
        leitorfechado= Cursor.execute("SELECT * FROM requisicao_exec WHERE condicao='Fechada'")
        Values = Cursor.execute("SELECT * FROM requisicao_exec")
    if Values > 0:
        Details = Cursor.fetchall()
        Cursor.close()
        return render_template('/home-exec.html', Details=Details,Values=Values,aberta=aberta,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto=leitoraberto,leitorfechado=leitorfechado)
    return render_template('/home-exec.html',Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv)


@executor_blueprint.route('/executor/chamadas-exec', methods=['GET','POST'])
def ExecChamada():
    with mysql.cursor()as Cursor:
        leitoraberto= Cursor.execute("SELECT * FROM requisicao WHERE condicao='Aberta'")
        leitorandamento= Cursor.execute("SELECT * FROM requisicao WHERE condicao='Andamento'")
        leitorfechado= Cursor.execute("SELECT * FROM requisicao WHERE condicao='Fechada'")
        cont_hardware=Cursor.execute("SELECT tipo FROM requisicao WHERE tipo='Problemas de Hardware'")
        cont_software= Cursor.execute("SELECT tipo FROM requisicao WHERE tipo='Problemas de Software'")
        cont_duv= Cursor.execute("SELECT tipo FROM requisicao WHERE tipo='Duvidas ou Esclarecimentos'")
        Values=Cursor.execute("SELECT * FROM requisicao")
    if Values > 0:
        Details = Cursor.fetchall()
        Cursor.close()
        return render_template('/chamadas-exec.html', Details=Details,Values=Values,cont_hardware = cont_hardware,cont_software=cont_software,cont_duv=cont_duv,leitoraberto = leitoraberto ,leitorfechado = leitorfechado ,leitorandamento =leitorandamento)
    return render_template('/chamadas-exec.html',Values=Values,cont_hardware=cont_hardware,cont_software=cont_software,cont_duv=cont_duv)

@executor_blueprint.route('/aceitando/<id>', methods=['POST'])
def aceitar(id):
    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE requisicao SET condicao ='Andamento' WHERE id_requisicao = %s",(id,))
        mysql.commit()
        Cursor.close()
    return redirect ('/executor/chamadas-exec')

@executor_blueprint.route('/recusando/<id>', methods=['POST'])
def recusando(id):
    formulario= request.form
    comentario= formulario['codigo']
    if comentario != None:
        with mysql.cursor()as Cursor:
            Cursor.execute("UPDATE requisicao SET comentario=%s  WHERE id_requisicao = %s",(comentario,id,))
            mysql.commit()
            Cursor.close()
    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE requisicao SET condicao ='Fechada'  WHERE id_requisicao = %s",(id,))
        mysql.commit()
        Cursor.close()
    return redirect ('/executor/chamadas-exec')

@executor_blueprint.route('/andamento/<id>', methods=['POST'])
def fechamento(id):
    formulario= request.form
    comentario = formulario['comentario']
    if comentario != None:
        with mysql.cursor()as Cursor:
            Cursor.execute("UPDATE requisicao SET comentario=%s  WHERE id_requisicao = %s",(comentario,id,))
            mysql.commit()
            Cursor.close()
    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE requisicao SET condicao ='Fechada'  WHERE id_requisicao = %s",(id,))
        mysql.commit()
        Cursor.close()
    return redirect ('/executor/chamadas-exec')

@executor_blueprint.route('/executor/<id>', methods=['POST'])
def delete(id):
    with mysql.cursor()as Cursor:
        Cursor.execute("DELETE FROM requisicao_exec WHERE id_requisicao=%s",(id,))
        mysql.commit()
        Cursor.close()
    return redirect('/executor/menu')
