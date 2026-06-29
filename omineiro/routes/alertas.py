from flask import Blueprint, render_template
from flask_login import login_required
from models import Produto

alertas = Blueprint('alertas', __name__)

@alertas.route('/alertas')
@login_required
def index():
    # Produtos abaixo ou igual ao mínimo
    produtos_alerta = Produto.query.filter(
        Produto.quantidade_atual <= Produto.quantidade_minima
    ).order_by(Produto.nome).all()

    return render_template('alertas.html', produtos=produtos_alerta)
