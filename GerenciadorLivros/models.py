from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    autor = db.Column(db.String(120), nullable=False)
    genero = db.Column(db.String(120), nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=False)
    paginas = db.Column(db.Integer, nullable=False)
