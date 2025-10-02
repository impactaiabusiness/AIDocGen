from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .models import Defesa, User
from .extensions import db
import os

# Importa as funções específicas de cada serviço
from .services_procuracao import preencher_procuracao_jacquelline, preencher_procuracao_jose

# Cria o blueprint para agrupar as rotas
main_bp = Blueprint('main', __name__)

# Rota para login
@main_bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        username = request.form.get('usuario')
        password = request.form.get('senha')
        current_app.logger.debug(f"Tentativa de login: usuario={username}")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Usuário ou senha incorretos!', 'danger')
            return render_template('login.html')
    return render_template('login.html')

# Rota para a página inicial após login
@main_bp.route('/home')
@login_required
def home():
    return render_template('home.html')

# --------- PROCURAÇÃO DRA. JAQUELLINE ---------
@main_bp.route('/procuracao')
@login_required
def procuracao():
    return render_template('index.html')

@main_bp.route('/gerar_procuracao', methods=['POST'])
@login_required
def gerar_procuracao():
    dados = {key: request.form.get(key) for key in request.form.keys()}
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        docx_path = preencher_procuracao_jacquelline(dados, base_dir)
        return send_file(docx_path, as_attachment=True)
    except Exception as e:
        current_app.logger.error(f"Erro ao gerar procuração: {e}")
        flash('Ocorreu um erro ao gerar a procuração. Por favor, tente novamente.', 'danger')
        return redirect(url_for('main.home')), 500

# --------- LOGOUT ---------
@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('main.login'))
