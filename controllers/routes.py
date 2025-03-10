from flask import render_template, request, redirect, url_for
# Essa biblioteca serve para ler uma determinada URL
import urllib
# Converte dados para o formato json
import json

gatos = []
gatolist = [{'nome': 'Farofa',
             'raca': 'Vira lata',
             'idade': 10}]


def init_app(app):
    @app.route('/')
    # View function -> função de visualização
    def home():
        return render_template('index.html')

    @app.route('/catlists', methods=['GET', 'POST'])
    def catlists():
        if request.method == 'POST':
            if request.form.get('gato'):
                gatos.append(request.form.get('gato'))
                return redirect(url_for('catlists'))

        return render_template('catlist.html',
                               gatos=gatos)
    
    @app.route('/catDictionary', methods=['GET', 'POST'])
    def catDictionary():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            gatolist.append(form_data)
            return (redirect(url_for('catDictionary')))
        return render_template('catDictionary.html', gatolist=gatolist)
    

    @app.route('/apigatos', methods=['GET', 'POST'])
    # Passando parâmetros para a rota
    @app.route('/apigatos/<string:id>', methods=['GET', 'POST'])
    # Definindo que o parâmetro é opcional
    def apigatos(id=None):
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
                return render_template('gatoinfo.html', ginfo=ginfo)
            else:
                return f'Gato com a ID {id} não foi encontrado.'

        return render_template('apigatos.html',
                               gatosjson=gatosjson)