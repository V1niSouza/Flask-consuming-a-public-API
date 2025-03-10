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