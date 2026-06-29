from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from models import Usuario
from extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(username=username).first()

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Usuário ou senha incorretos.', 'erro')

    return render_template('login.html')

@auth.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form.get('username')
        nome = request.form.get('nome')
        perfil = request.form.get('perfil')
        senha = request.form.get('senha')

        if Usuario.query.filter_by(username=username).first():
            flash('Usuário já existe.', 'erro')
            return render_template('cadastro.html')

        novo = Usuario(
            username=username,
            nome=nome,
            perfil=perfil,
            senha=generate_password_hash(senha)
        )
        db.session.add(novo)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'sucesso')
        return redirect(url_for('auth.login'))

    return render_template('cadastro.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
