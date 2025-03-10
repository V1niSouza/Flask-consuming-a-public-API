from flask import render_template

def init_app(app):
    @app.route('/')
    # View function -> função de visualização
    def home():
        return render_template('index.html')
