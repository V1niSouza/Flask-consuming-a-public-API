from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Gato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    raca = db.Column(db.String(150))
    caracter = db.Column(db.String(150))

    def __init__(self, nome, raca, caracter):
            self.nome = nome
            self.raca = raca
            self.caracter = caracter