from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "chave_secreta"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livros.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo do Livro
class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50), nullable=False)

# Rota principal (listar livros)
@app.route('/')
def lista_livros():
    livros = Livro.query.all()
    return render_template('lista.html', livros=livros)

# Rota para editar livro
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_livro(id):
    livro = Livro.query.get_or_404(id)
    if request.method == 'POST':
        # Atualizar os dados do livro
        livro.titulo = request.form['titulo']
        livro.autor = request.form['autor']
        livro.genero = request.form['genero']
        try:
            db.session.commit()
            flash('Livro atualizado com sucesso!', 'success')
            return redirect(url_for('lista_livros'))
        except:
            flash('Erro ao atualizar o livro.', 'danger')
    return render_template('editar.html', livro=livro)

# Rota para deletar livro
@app.route('/deletar/<int:id>', methods=['POST'])
def deletar_livro(id):
    livro = Livro.query.get_or_404(id)
    try:
        db.session.delete(livro)
        db.session.commit()
        flash('Livro excluído com sucesso!', 'success')
    except:
        flash('Erro ao excluir o livro.', 'danger')
    return redirect(url_for('lista_livros'))

if __name__ == '__main__':
    app.run(debug=True)
