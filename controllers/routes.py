from flask import render_template, request, redirect, url_for
# Essa biblioteca serve para ler uma determinada URL
import urllib
# Converte dados para o formato json
import json



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