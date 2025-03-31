from flask import Flask, render_template
from controllers import routes
from models.database import db
import os

# Criando a instância do Flask na variável app
app = Flask(__name__, template_folder='views')  # Representa o nome do arquivo
routes.init_app(app)

# Permite ler o diretório de um determinado arquivo
dir = os.path.abspath(os.path.dirname(__file__))

# Passamos o diretório ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/gatos.sqlite3')

# Iniciar o servidor
if __name__ == '__main__':
    db.init_app(app=app)
    # Verifica no inicio da aplicação se o BD já existe. Caso contrário ele  criará o BD.
    with app.test_request_context():
        db.create_all()
    app.run(host='0.0.0.0', port=4000, debug=True)