from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import Produto, Movimentacao
from extensions import db

movimentacoes = Blueprint('movimentacoes', __name__)

@movimentacoes.route('/movimentacoes')
@login_required
def index():
    lista = Movimentacao.query.order_by(Movimentacao.data_hora.desc()).all()
    return render_template('movimentacoes.html', movimentacoes=lista)

@movimentacoes.route('/movimentacoes/nova', methods=['GET', 'POST'])
@login_required
def nova():
    produtos = Produto.query.order_by(Produto.nome).all()

    if request.method == 'POST':
        produto_id = request.form.get('produto_id')
        tipo = request.form.get('tipo')
        quantidade_str = request.form.get('quantidade')

        # Validação dos campos obrigatórios
        if not produto_id or not tipo or not quantidade_str:
            flash('Preencha todos os campos obrigatórios.', 'erro')
            return render_template('movimentacao_form.html', produtos=produtos)

        try:
            produto_id = int(produto_id)
            quantidade = float(quantidade_str)
        except ValueError:
            flash('Quantidade inválida.', 'erro')
            return render_template('movimentacao_form.html', produtos=produtos)

        if quantidade <= 0:
            flash('A quantidade deve ser maior que zero.', 'erro')
            return render_template('movimentacao_form.html', produtos=produtos)

        produto = db.session.get(Produto, produto_id)
        if not produto:
            flash('Produto não encontrado.', 'erro')
            return render_template('movimentacao_form.html', produtos=produtos)

        observacao = request.form.get('observacao', '')

        # Atualizar quantidade do produto
        if tipo == 'entrada':
            produto.quantidade_atual += quantidade
        elif tipo == 'saida':
            if produto.quantidade_atual < quantidade:
                flash(f'Estoque insuficiente! Disponível: {produto.quantidade_atual} {produto.unidade}.', 'erro')
                return render_template('movimentacao_form.html', produtos=produtos)
            produto.quantidade_atual -= quantidade
        else:
            flash('Tipo de movimentação inválido.', 'erro')
            return render_template('movimentacao_form.html', produtos=produtos)

        # Registrar movimentação
        mov = Movimentacao(
            produto_id=produto_id,
            usuario_id=current_user.id,
            tipo=tipo,
            quantidade=quantidade,
            observacao=observacao
        )
        db.session.add(mov)
        db.session.commit()

        flash(f'{tipo.capitalize()} de {quantidade} {produto.unidade} de "{produto.nome}" registrada!', 'sucesso')
        return redirect(url_for('movimentacoes.index'))

    return render_template('movimentacao_form.html', produtos=produtos)
