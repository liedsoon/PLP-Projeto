from flask import Flask, render_template, redirect, url_for, request
from models import Livro, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livros.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Criação das tabelas no banco de dados
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/listar')
def listar_livros():
    livros = Livro.query.all()
    return render_template('listar.html', livros=livros)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        genero = request.form['genero']
        ano_publicacao = request.form['ano_publicacao']
        paginas = request.form['paginas']
        
        novo_livro = Livro(titulo=titulo, autor=autor, genero=genero, ano_publicacao=ano_publicacao, paginas=paginas)
        db.session.add(novo_livro)
        db.session.commit()
        
        return redirect(url_for('home'))
    
    return render_template('adicionar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_livro(id):
    livro = Livro.query.get_or_404(id)  # Busca o livro pelo ID
    if request.method == 'POST':
        # Atualiza os dados do livro
        livro.titulo = request.form['titulo']
        livro.autor = request.form['autor']
        livro.genero = request.form['genero']
        livro.ano_publicacao = request.form['ano_publicacao']
        livro.paginas = request.form['paginas']
        
        db.session.commit()  # Salva as alterações no banco de dados
        return redirect(url_for('listar_livros'))  # Redireciona para a listagem
    return render_template('editar.html', livro=livro)  # Renderiza o formulário de edição


@app.route('/deletar/<int:id>', methods=['POST'])
def deletar_livro(id):
    livro = Livro.query.get_or_404(id)
    db.session.delete(livro)
    db.session.commit()
    return redirect(url_for('listar_livros'))

if __name__ == '__main__':
    app.run(debug=True)
