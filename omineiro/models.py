from extensions import db
from flask_login import UserMixin
from datetime import datetime

class Usuario(UserMixin, db.Model):
    """Usuário do sistema (Gestor ou Funcionário)."""
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    perfil = db.Column(db.String(20), nullable=False)  # 'gestor' ou 'funcionario'
    senha = db.Column(db.String(200), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    movimentacoes = db.relationship('Movimentacao', backref='usuario', lazy=True)

    def is_gestor(self):
        return self.perfil == 'gestor'


class Produto(db.Model):
    """Produto do estoque."""
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), default='CEASA')
    unidade = db.Column(db.String(20), nullable=False)  # kg, litro, unidade
    quantidade_atual = db.Column(db.Float, default=0)
    quantidade_minima = db.Column(db.Float, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    movimentacoes = db.relationship('Movimentacao', backref='produto', lazy=True)

    def esta_em_alerta(self):
        """Retorna True se o estoque estiver abaixo do mínimo."""
        return self.quantidade_atual <= self.quantidade_minima


class Movimentacao(db.Model):
    """Registro de entrada ou saída de produto."""
    __tablename__ = 'movimentacoes'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # 'entrada' ou 'saida'
    quantidade = db.Column(db.Float, nullable=False)
    observacao = db.Column(db.String(200))
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
