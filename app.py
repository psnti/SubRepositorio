from flask import Flask, render_template, send_from_directory, request, redirect, url_for, make_response, flash
from flask_bootstrap import Bootstrap
import folium
import os
import json
import pandas as pd
from time import time
from random import random
from joblib import load
import sklearn
from folium.plugins import MarkerCluster
from datetime import datetime
import numpy as np


app = Flask(__name__)
app.secret_key = 'super clave secreta'
Bootstrap(app)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'pics'),
                               'favicon.png', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def paginaPrincipal():
    return render_template('index.html')


@app.route('/contacto')
def paginaContacto():
    return render_template('contacto.html')

@app.route('/descarga_archivo')
def descarga_archivo():
    p = "contact.png"
    return send_from_directory('static/pics',p,as_attachment = True)


@app.route('/mapas', methods=['GET', 'POST'])
def paginaMapas():
    # df = pd.read_excel('geojson/playasCoordenadas.xlsx')
    df = pd.read_pickle('documentos/listado_playas.pkl')
    # df = df.to_dict()
    if request.method == 'POST':
        # variables
        var = request.form['eleccion']
        fecha = request.form['fecha']
        if 'Ninguna' not in var:
            # Si nose ha metido fecha lanzar mensaje de error
            if fecha == '':
                flash('Introduce una Fecha')
                return redirect(request.url)

            # recojo coordenadas de la playa
            coordenada = [-df['Lat.dec'][var], -df['Long.dec'][var]]
            print(coordenada)
            # agrego marcador al mapa y centro en coordenadas
            folium_map_especifico = folium.Map()
            folium_map_especifico = folium.Map(
                location=[coordenada[0], coordenada[1]], zoom_start=15)
            folium.Marker(
                location=[coordenada[0], coordenada[1]],
                popup=var,
                icon=folium.Icon(color='blue', icon='cloud')
            ).add_to(folium_map_especifico)
            mapa = folium_map_especifico._repr_html_()
            historico = dame_historico(var)
            #resulados
            resultados = genera_resultados(fecha, coordenada)
            playas = df.index.tolist()

            playas.insert(0,"Ninguna")

            return render_template('mapas.html', playas=playas, nombre=var, resultados=resultados, historico=historico, fecha=fecha, mapa=mapa)

    # creo mapa en coordenadas
    print('mapa original')
    folium_map = folium.Map()
    start_coords = (-34.536267, -72.406639)
    folium_map = folium.Map(location=start_coords, zoom_start=5)
    folium_map = anade_playas(folium_map, df)
    # elimino libreria en conflicto
    mapa = arregla_mapa(folium_map._repr_html_())
    return render_template('mapas.html', playas=df.index.values, resultados=None, historico = None, mapa=mapa, fecha = None)


def dame_historico(nombre_playa):
    excel = pd.read_excel('documentos/Datos_Physalia_20171010.xls')
    seleccion = excel.loc[excel['Lugar'] == nombre_playa]
    seleccion = seleccion.loc[excel['Tipo.Abund'] == 'numero']
    seleccion = seleccion.groupby(['Date']).sum().reset_index()

    lista = []
    for i in seleccion.iterrows():
        lista.append({'y':(i[1]['Date']).strftime("%Y-%m-%d"),'v':i[1]['Abundancia']})
    print(lista)
    return lista
    
def anade_playas(fol, playas):
    cluster = MarkerCluster().add_to(fol)
    
    for i in playas.iterrows():
        print()
        print(i[0])
        print()
        #  -i[1][1]],i[0])
        # print('\n{}\n'.format(type(i[1])))
        folium.Marker([-i[1][1], -i[1][2]],
                      popup=i[0],
                      icon=folium.Icon(color='red', icon='info-sign'),
                      ).add_to(cluster)
    return fol

def borra_mapa():
    try:
        os.remove('templates/mapaChile.html')
        print(os.listdir('templates'))
    except:
        print('Aun no existe')


def genera_resultados(fecha, coodenadas):
    # se cogerian los datos de copernicus
    # generar dataframe
    # meterlo al modelo
    modelo = load('static/modelo.joblib')
    # print(modelo)

    lista = [{'y': '2020-1-1', 'v': 1},
             {'y': '2020-2-1', 'v': 10},
             {'y': '2020-1-5', 'v': 5},
             {'y': '2020-3-5', 'v': 2}]
    return lista


# elimina javascrip y css en conflicto
def arregla_mapa(mapa):

    newdata = mapa.replace(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/>', '')
    newdata = newdata.replace(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css"/>', '')
    newdata = newdata.replace(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"/>', '')

    return newdata



if __name__ == '__main__':
    app.run(debug=True)



