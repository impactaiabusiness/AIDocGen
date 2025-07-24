from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Defesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    nacionalidade = db.Column(db.String(50), nullable=False)
    estado_civil = db.Column(db.String(20), nullable=False)
    profissao = db.Column(db.String(50), nullable=False)
    rg = db.Column(db.String(20), nullable=False)
    orgao = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    rua = db.Column(db.String(100), nullable=False)
    numero_e_complemento = db.Column(db.String(50), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    ddd = db.Column(db.String(4), nullable=True)
    telefone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(150), nullable=True)
