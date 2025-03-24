import pytest
from app import create_app, db
from app.models import User

@pytest.fixture(scope="function")
def client():
    # Cria a aplicação com configurações de teste
    app = create_app()
    app.config['TESTING'] = True
    # Utiliza um banco de dados SQLite em memória para testes
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            # Garante que o banco esteja limpo antes de criar as tabelas
            db.drop_all()
            db.create_all()
            # Cria um usuário de teste
            user = User(username='test')
            user.set_password('test123')
            db.session.add(user)
            db.session.commit()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_login_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Login' in response.data  # Verifica se a página de login contém "Login"

def test_valid_login(client):
    response = client.post(
        '/', 
        data={'usuario': 'test', 'senha': 'test123'},
        follow_redirects=True
    )
    # Verifica se a mensagem de sucesso de login aparece na resposta
    assert b'Login realizado com sucesso!' in response.data
    # Também verifica se o redirecionamento para a home ocorreu
    assert b'home' in response.data.lower()

def test_invalid_login(client):
    response = client.post(
        '/', 
        data={'usuario': 'test', 'senha': 'wrongpassword'},
        follow_redirects=True
    )
    # Verifica se a mensagem de erro aparece na resposta
    assert b'Usu\xc3\xa1rio ou senha incorretos!' in response.data
