import os
from flask import Flask
from .config import Config
from .extensions import db
from flask_login import LoginManager

def create_app():
    # Define os diretórios absolutos para templates e static
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(base_dir, '..', 'templates')
    static_dir = os.path.join(base_dir, '..', 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(Config)

    # Inicializa extensões
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'  # Redireciona para a rota de login
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importa e registra as rotas via Blueprint
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Cria as tabelas, se não existirem e cria o usuário fixo se necessário
    with app.app_context():
        db.create_all()
        
        # Criação do usuário permanente 'driveup' com senha 'driveup'
        usuario_fixo = User.query.filter_by(username='driveup').first()
        if not usuario_fixo:
            novo_user = User(username='driveup')
            novo_user.set_password('driveup')
            db.session.add(novo_user)
            db.session.commit()
            print("Usuário 'driveup' criado com a senha 'driveup'.")
        else:
            print("Usuário 'driveup' já existe no banco.")

    return app
