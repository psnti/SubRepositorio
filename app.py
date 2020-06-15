from flask import Flask, render_template, send_from_directory, request, redirect, url_for, make_response, flash
from flask_bootstrap import Bootstrap
import folium
import os
import json
import pandas as pd
from time import time
from random import random


app = Flask(__name__)
app.secret_key = 'super clave secreta'
Bootstrap(app)

folium_map = folium.Map()


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


@app.route('/mapas', methods=['GET', 'POST'])
def paginaMapas():
    df = pd.read_excel('geojson/playasCoordenadas.xlsx')
    df = df.to_dict()
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
            coordenada = df[var]
            print(coordenada)
            # agrego marcador al mapa y centro en coordenadas
            folium_map = folium.Map(
                location=[coordenada[0], coordenada[1]], zoom_start=15)
            folium.Marker(
                location=[coordenada[0], coordenada[1]],
                popup=var,
                icon=folium.Icon(color='blue', icon='cloud')
            ).add_to(folium_map)
            # guardo mapa
            folium_map.save('templates/mapaChile.html')
            arregla_mapa()
            #resulados
            resultados = genera_resultados(fecha, coordenada)
            return render_template('mapas.html', playas=df.keys(), nombre=var, resultados=resultados, fecha=fecha)

    # creo mapa en coordenadas
    start_coords = (-34.536267, -72.406639)
    folium_map = folium.Map(location=start_coords, zoom_start=5)
    # guardo mapa
    folium_map.save('templates/mapaChile.html')
    # elimino libreria en conflicto
    arregla_mapa()
    return render_template('mapas.html', playas=df.keys(), resultados=None)


def genera_resultados(fecha, coodenadas):
    # se cogerian los datos de copernicus
    # generar dataframe
    # meterlo al modelo
    lista = [{'year': '2020-1-1', 'value': 1},
             {'year': '2020-2-1', 'value': 10},
             {'year': '2020-1-5', 'value': 5},
             {'year': '2020-3-5', 'value': 2}]
    return lista


# @app.route('/data', methods=["GET", "POST"])
# def data():
#     global contador
#     try:
#         data = lista[contador]
#         contador += 1
#         response = make_response(json.dumps(data))
#         response.content_type = 'application/json'
#         print(response)
#         return response
#     except:
#         contador = 0
#         return None


# elimina javascrip y css en conflicto
def arregla_mapa():
    f = open('./templates/mapaChile.html', 'r')
    print(f)
    filedata = f.read()
    f.close()

    newdata = filedata.replace(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/>', '')
    newdata = newdata.replace(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css"/>', '')
    newdata = newdata.replace(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"/>', '')

    f = open('./templates/mapaChile.html', 'w')
    f.write(newdata)
    f.close()


if __name__ == '__main__':

    app.run(debug=True, port=1000)
