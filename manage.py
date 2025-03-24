from app import create_app

app = create_app()

if __name__ == '__main__':
    # Se quiser modo debug local, ative:
    app.run(debug=True)
