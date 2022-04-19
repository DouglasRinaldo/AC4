from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/pedidos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
 
db = SQLAlchemy(app)
 
#Classe
class Pedidos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50))
    pedidos = db.Column(db.Integer)
    itens_id = db.Column(db.String(100))
    valor = db.Column(db.Float)
    pag_dinheiro = db.Column(db.Integer, default = 0)
    pag_cartao = db.Column(db.Integer, default = 0)
 
 
    def __init__(self, nome, pedidos, itens_id, valor, pag_dinheiro, pag_cartao):
 
        self.nome = nome
        self.pedidos = pedidos
        self.itens_id = itens_id
        self.valor = valor
        self.pag_dinheiro = pag_dinheiro
        self.pag_cartao = pag_cartao



@app.route('/')
def Index():
    all_pedidos = Pedidos.query.order_by('pedidos').all()
 
    return render_template("index.html", pedidos = all_pedidos)
 
 
#Inserir dados
@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        nome = request.form['nome']
        pedidos = request.form['pedidos']
        itens_id = request.form['itens_id'] 
        valor = request.form['valor']
        tipo_pag = request.form.get('tipo_pag')

        valor_cartao = '0'
        valor_dinheiro = '0'
        if tipo_pag != 'naopago':
            if tipo_pag == 'cartao':
                valor_cartao = '1'
            elif tipo_pag == 'dinheiro':
                valor_dinheiro = '1'



        my_data = Pedidos(nome, pedidos, itens_id, valor, valor_dinheiro, valor_cartao)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Pedido Inserido com Sucesso")
 
        return redirect(url_for('Index'))
 
 

@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_data = Pedidos.query.get(request.form.get('id'))
 
        my_data.nome = request.form['nome']
        my_data.pedidos = request.form['pedidos']
        my_data.itens_id = request.form['itens_id']
        my_data.valor = request.form['valor']

        valor_cartao = '0'
        valor_dinheiro = '0'
        tipo_pag = request.form.get('tipo_pag')
        if tipo_pag != 'naopago':
            if tipo_pag == 'cartao':
                valor_cartao = '1'
            elif tipo_pag == 'dinheiro':
                valor_dinheiro = '1'


        my_data.pag_cartao = valor_cartao
        my_data.pag_dinheiro = valor_dinheiro
        db.session.commit()
        flash("Pedido Atualizado com Sucesso")
 
        return redirect(url_for('Index'))

#@app.route('/pay', methods =['GET','POST'])
#def pay():

 

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Pedidos.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Pedido Deletado com Sucesso")
 
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)