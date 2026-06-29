from flask import Flask
from extensions import db, login_manager
from models import Usuario


def create_app():
    import os

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "omineiro-secreto-2024"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///estoque.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para acessar."

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registrar blueprints (rotas)
    from routes.auth import auth
    from routes.dashboard import dashboard
    from routes.produtos import produtos
    from routes.movimentacoes import movimentacoes
    from routes.alertas import alertas

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(produtos)
    app.register_blueprint(movimentacoes)
    app.register_blueprint(alertas)

    # Criar tabelas e usuários padrão
    with app.app_context():
        db.create_all()
        criar_usuarios_padrao()

    return app


def criar_usuarios_padrao():
    """Cria os dois usuários fixos se não existirem."""
    from models import Usuario
    from werkzeug.security import generate_password_hash

    if not Usuario.query.filter_by(username="admin").first():
        admin = Usuario(
            username="admin",
            nome="Gestor",
            perfil="gestor",
            senha=generate_password_hash("admin123"),
        )
        db.session.add(admin)

    if not Usuario.query.filter_by(username="funcionario").first():
        func = Usuario(
            username="funcionario",
            nome="Funcionário",
            perfil="funcionario",
            senha=generate_password_hash("func123"),
        )
        db.session.add(func)

    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
