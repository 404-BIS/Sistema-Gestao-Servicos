from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL



app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admim'
app.config['MYSQL_DB'] = 'sistema_solicitacao'
 
mysql = MySQL(app)

@app.route('/')
def MainHome():
    return redirect('/usuario/menu')
#---------------------------------------------------------------------------------------USUARIO----------------------------
@app.route('/usuario/solicitacao', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        Details = request.form
        titulo = Details['titulo']
        descricao = Details['descricao']
        tipo = Details['tipo']
        condicao = 'Aberta'
        comentari= ''
        Cursor = mysql.connection.cursor()
        Cursor.execute("INSERT INTO requisicao(titulo, descricao,tipo,condicao,comentario) VALUES(%s,%s,%s,%s,%s)",(titulo,descricao,tipo,condicao,comentari))
        mysql.connection.commit()
        Cursor.close()
        return redirect("/usuario/menu")
    return render_template('user/nova-requisicao-user.html')


@app.route('/usuario/menu')
def home():
    Cursor=mysql.connection.cursor()
    aberta= Cursor.execute("SELECT * FROM requisicao")
    prob= Cursor.execute("SELECT tipo FROM requisicao WHERE tipo='Problemas de Hardware'")
    prob1= Cursor.execute("SELECT tipo FROM requisicao WHERE tipo='Problemas de Software'")
    prob2= Cursor.execute("SELECT tipo FROM requisicao WHERE tipo='Duvidas ou Esclarecimentos'")
    leitoraberto= Cursor.execute("SELECT * FROM requisicao WHERE condicao='Aberta'")
    leitorfechado= Cursor.execute("SELECT * FROM requisicao WHERE condicao='Fechada'")
    Values = Cursor.execute("SELECT * FROM requisicao")
    if Values > 0:
        Details = Cursor.fetchall()
        return render_template('user/home-user.html', Details=Details,Values=Values,aberta=aberta,prob=prob,prob1=prob1,prob2=prob2,leitoraberto=leitoraberto,leitorfechado=leitorfechado)
    else:
        return render_template('user/home-user.html', Values=Values)


#---------------------------------------------------------------------------------------EXECUTOR---------------------------

@app.route('/executor/solicitacao', methods=['GET','POST'])
def novaExecutor():
    if request.method == 'POST':
        Details = request.form
        titulo = Details['titulo']
        tipoE = Details['tipo']
        descricao = Details['descricao']
        condicao = 'Aberta'

        Cursor = mysql.connection.cursor()
        Cursor.execute("INSERT INTO requisicao_exec(titulo, descricao,tipo,condicao) VALUES(%s,%s,%s,%s)",(titulo,descricao,tipoE,condicao))
        mysql.connection.commit()
        Cursor.close()
        return redirect("/executor/menu")
    return render_template('exec/nova-requisicao-exec.html')

@app.route('/executor/menu',methods=['GET','POST'])
def executor():
    Cursor=mysql.connection.cursor()
    aberta= Cursor.execute("SELECT * FROM requisicao_exec")
    prob= Cursor.execute("SELECT tipo FROM requisicao_exec WHERE tipo='Problemas de Hardware'")
    prob1= Cursor.execute("SELECT tipo FROM requisicao_exec WHERE tipo='Problemas de Software'")
    prob2= Cursor.execute("SELECT tipo FROM requisicao_exec WHERE tipo='Duvidas ou Esclarecimentos'")
    leitoraberto= Cursor.execute("SELECT * FROM requisicao_exec WHERE condicao='Aberta'")
    leitorfechado= Cursor.execute("SELECT * FROM requisicao_exec WHERE condicao='Fechada'")
    Values = Cursor.execute("SELECT * FROM requisicao_exec")
    if Values > 0:
        Details = Cursor.fetchall()
        return render_template('exec/home-exec.html', Details=Details,Values=Values,aberta=aberta,prob=prob,prob1=prob1,prob2=prob2,leitoraberto=leitoraberto,leitorfechado=leitorfechado)
    return render_template('exec/home-exec.html', Values=Values)

#----------------------------------------------------------------------------------Minha Requisao Executor-------------------------

@app.route('/executor/chamadas-exec', methods=['GET','POST'])
def ExecChamada():
    Cursor=mysql.connection.cursor()
    leitoraberto= Cursor.execute("SELECT * FROM requisicao WHERE condicao='Aberta'")
    leitorandamento= Cursor.execute("SELECT * FROM requisicao WHERE condicao='Andamento'")
    leitorfechado= Cursor.execute("SELECT * FROM requisicao WHERE condicao='Fechada'")
    prob= Cursor.execute("SELECT tipo FROM requisicao WHERE tipo='Problemas de Hardware'")
    prob1= Cursor.execute("SELECT tipo FROM requisicao WHERE tipo='Problemas de Software'")
    prob2= Cursor.execute("SELECT tipo FROM requisicao WHERE tipo='Duvidas ou Esclarecimentos'")
    Values=Cursor.execute("SELECT * FROM requisicao")
    if Values > 0:
        Details = Cursor.fetchall()
        return render_template('exec/chamadas-exec.html', Details=Details,Values=Values,prob=prob,prob1=prob1,prob2=prob2,leitoraberto = leitoraberto ,leitorfechado = leitorfechado ,leitorandamento =leitorandamento)
    return render_template('exec/chamadas-exec.html',Values=Values)
# ---------------------------------------------update------------------------------------------------------------------------------

@app.route('/aceitando/<id>', methods=['POST'])
def aceitar(id):
    Cursor= mysql.connection.cursor()
    Cursor.execute("UPDATE requisicao SET condicao ='Andamento' WHERE id_requisicao = %s",(id,))
    Cursor.connection.commit()
    Cursor.close
    return redirect ('/executor/chamadas-exec')

@app.route('/recusando/<id>', methods=['POST'])
def fechada(id):
    formulario= request.form
    comentario= formulario['codigo']
    if comentario != None:
        Cursor= mysql.connection.cursor()
        Cursor.execute("UPDATE requisicao SET comentario=%s  WHERE id_requisicao = %s",(comentario,id,))
        Cursor.connection.commit()
        Cursor.close
    Cursor= mysql.connection.cursor()
    Cursor.execute("UPDATE requisicao SET condicao ='Fechada'  WHERE id_requisicao = %s",(id,))
    Cursor.connection.commit()
    Cursor.close
    return redirect ('/executor/chamadas-exec')

@app.route('/andamento/<id>', methods=['POST'])
def fechada1(id):
    inform= request.form
    comentario = inform['comentario']
    if comentario != None:
        Cursor= mysql.connection.cursor()
        Cursor.execute("UPDATE requisicao SET comentario=%s  WHERE id_requisicao = %s",(comentario,id,))
        Cursor.connection.commit()
        Cursor.close
    Cursor= mysql.connection.cursor()
    Cursor.execute("UPDATE requisicao SET condicao ='Fechada'  WHERE id_requisicao = %s",(id,))
    Cursor.connection.commit()
    Cursor.close
    return redirect ('/executor/chamadas-exec')


#----------------------------------------------------------------------------------DELETE------------------------------------------


@app.route('/usuario/<id>', methods=['POST'])
def delete(id):
    Cursor= mysql.connection.cursor()
    Cursor.execute("DELETE FROM requisicao WHERE id_requisicao=%s",(id,))
    Cursor.connection.commit()
    Cursor.close
    return redirect('/usuario/menu')

@app.route('/executor/<id>', methods=['POST'])
def delete2(id):
    Cursor= mysql.connection.cursor()
    Cursor.execute("DELETE FROM requisicao_exec WHERE id_requisicao=%s",(id,))
    Cursor.connection.commit()
    Cursor.close
    return redirect('/executor/menu')



if __name__ == "__main__":
    app.run(debug=True)

