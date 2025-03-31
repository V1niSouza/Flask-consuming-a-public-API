from flask import render_template, request, redirect, url_for
# Essa biblioteca serve para ler uma determinada URL
import urllib
# Converte dados para o formato json
import json
# Importando o Model
from models.database import db, Gato



gatos = []
gatolist = []


def init_app(app):
    
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/catlists', methods=['GET', 'POST'])
    def catlists():
        if request.method == 'POST':
            if request.form.get('gato'):
                gatos.append(request.form.get('gato'))
                return redirect(url_for('catlists'))

        return render_template('catlists.html',
                               gatos=gatos)
    
    @app.route('/catDictionary', methods=['GET', 'POST'])
    def catDictionary():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            gatolist.append(form_data)
            return (redirect(url_for('catDictionary')))
        return render_template('catDictionary.html', gatolist=gatolist)
    

    @app.route('/apicats', methods=['GET', 'POST'])
    
    @app.route('/apicats/<string:id>', methods=['GET', 'POST'])   # Passando parâmetros para a rota
    def apicats(id=None):     # Definindo que o parâmetro é opcional
        url = 'https://api.thecatapi.com/v1/breeds'
        res = urllib.request.urlopen(url)
        # print(res)
        data = res.read()
        gatosjson = json.loads(data)

        if id:
            ginfo = []
            for g in gatosjson:
                if g['id'] == id:
                    ginfo = g
                    break
            if ginfo:
                return render_template('catinfo.html', ginfo=ginfo)
            else:
                return f'Gato com a ID {id} não foi encontrado.'

        return render_template('apicats.html',
                               gatosjson=gatosjson)

    # CRUD - Listagem, Cadastro e Exclusão
    @app.route('/gatoBanco', methods=['GET', 'POST'])
    @app.route('/gatoBanco/delete/<int:id>')
    def gatoBanco(id=None):
        if id:
            gato = Gato.query.get(id)
            #Deleta o cadastro pela ID
            db.session.delete(gato)
            db.session.commit()
            return redirect(url_for('gatoBanco'))
    # Cadastra um novo gato
        if request.method == 'POST':
            newgato = Gato(request.form['nome'], request.form['raca'], request.form['caracter'])
            db.session.add(newgato)
            db.session.commit()
            return redirect(url_for('gatoBanco'))
        else:
            page = request.args.get('page', 1, type=int)
            per_page = 3
            gatos_page = Gato.query.paginate(page=page,per_page=per_page)
            return render_template('gatoBanco.html', gatosBanco=gatos_page)
    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        g = Gato.query.get(id)
        if request.method == 'POST':
            g.nome = request.form['nome']
            g.raca = request.form['raca']
            g.caracter = request.form['caracter']
            db.session.commit()
            return redirect(url_for('gatoBanco'))
        return render_template('editGato.html', g=g)