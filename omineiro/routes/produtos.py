from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import Produto
from extensions import db

produtos = Blueprint('produtos', __name__)

@produtos.route('/produtos')
@login_required
def index():
    lista = Produto.query.order_by(Produto.nome).all()
    return render_template('produtos.html', produtos=lista)

@produtos.route('/produtos/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if not current_user.is_gestor():
        flash('Acesso negado. Apenas o gestor pode cadastrar produtos.', 'erro')
        return redirect(url_for('produtos.index'))

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        unidade = request.form.get('unidade', '').strip()
        quantidade_atual = request.form.get('quantidade_atual', '0')
        quantidade_minima = request.form.get('quantidade_minima', '0')

        if not nome or not unidade:
            flash('Nome e unidade são obrigatórios.', 'erro')
            return render_template('produto_form.html', produto=None)

        try:
            quantidade_atual = float(quantidade_atual)
            quantidade_minima = float(quantidade_minima)
        except ValueError:
            flash('Quantidades inválidas.', 'erro')
            return render_template('produto_form.html', produto=None)

        # Verificar se produto já existe
        if Produto.query.filter_by(nome=nome).first():
            flash(f'Já existe um produto com o nome "{nome}".', 'erro')
            return render_template('produto_form.html', produto=None)

        produto = Produto(
            nome=nome,
            unidade=unidade,
            quantidade_atual=quantidade_atual,
            quantidade_minima=quantidade_minima
        )
        db.session.add(produto)
        db.session.commit()
        flash(f'Produto "{nome}" cadastrado com sucesso!', 'sucesso')
        return redirect(url_for('produtos.index'))

    return render_template('produto_form.html', produto=None)

@produtos.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    if not current_user.is_gestor():
        flash('Acesso negado.', 'erro')
        return redirect(url_for('produtos.index'))

    produto = db.session.get(Produto, id)
    if not produto:
        flash('Produto não encontrado.', 'erro')
        return redirect(url_for('produtos.index'))

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        unidade = request.form.get('unidade', '').strip()
        quantidade_minima = request.form.get('quantidade_minima', '0')

        if not nome or not unidade:
            flash('Nome e unidade são obrigatórios.', 'erro')
            return render_template('produto_form.html', produto=produto)

        try:
            quantidade_minima = float(quantidade_minima)
        except ValueError:
            flash('Quantidade mínima inválida.', 'erro')
            return render_template('produto_form.html', produto=produto)

        produto.nome = nome
        produto.unidade = unidade
        produto.quantidade_minima = quantidade_minima
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'sucesso')
        return redirect(url_for('produtos.index'))

    return render_template('produto_form.html', produto=produto)

@produtos.route('/produtos/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    if not current_user.is_gestor():
        flash('Acesso negado.', 'erro')
        return redirect(url_for('produtos.index'))

    produto = db.session.get(Produto, id)
    if not produto:
        flash('Produto não encontrado.', 'erro')
        return redirect(url_for('produtos.index'))

    db.session.delete(produto)
    db.session.commit()
    flash(f'Produto "{produto.nome}" removido.', 'sucesso')
    return redirect(url_for('produtos.index'))
