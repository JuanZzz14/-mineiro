from flask import Blueprint, render_template
from flask_login import login_required
from models import Produto, Movimentacao
from datetime import datetime, timedelta

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def index():
    total_produtos = Produto.query.count()
    alertas = Produto.query.filter(
        Produto.quantidade_atual <= Produto.quantidade_minima
    ).count()

    # Movimentações de hoje
    hoje = datetime.utcnow().date()
    movimentacoes_hoje = Movimentacao.query.filter(
        db.func.date(Movimentacao.data_hora) == hoje
    ).count()

    # Últimas 5 movimentações
    ultimas = Movimentacao.query.order_by(
        Movimentacao.data_hora.desc()
    ).limit(5).all()

    return render_template('dashboard.html',
        total_produtos=total_produtos,
        alertas=alertas,
        movimentacoes_hoje=movimentacoes_hoje,
        ultimas=ultimas
    )

# Importar db aqui para evitar circular import
from extensions import db
