from flask import Flask, render_template, send_from_directory
from flask_bootstrap import Bootstrap
import folium
import os
import json
import pandas as pd


app = Flask(__name__)
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


@app.route('/mapas')
def paginaMapas():
    start_coords = (-34.536267, -72.406639)
    folium_map = folium.Map(location=start_coords, zoom_start=5)
    print(os.getcwd())
    print('')
    folium_map.save('templates\\mapaChile.html')
    arregla_mapa()
    return render_template('mapas.html')


@app.route('/pruebas')
def paginaprueba():
    start_coords = (-37.25, -73.58333333333333)
    folium_map = folium.Map(location=start_coords, zoom_start=10)
    gjson = os.path.join(app.root_path, 'geojson/prueba.geojson')
    file = open(gjson, encoding='utf-8')
    geo_data = json.load(file)
    file.close()
    # print(geo_data)
    # imprimir playas
    w = geo_data['geometry']
    df_0083 = pd.read_excel('geojson\\playas0083_1.xlsx')
    df_025 = pd.read_excel('geojson\\playas025_1.xlsx')
    df = pd.read_excel('geojson\\playasSinRedondeoCoord.xlsx')

    # for x,y in enumerate(w['coordjuinates']):
    for x, y in df_0083.iterrows():
        # print('-----------------------------------',x,y)
        folium.Marker(
            # location=[y[0],y[1]],
            # popup=w["nombre"][x]
            location=[str(df_0083.loc[x]['Latitud']).replace(',', '.'),
                      str(df_0083.loc[x]['Longitud']).replace(',', '.')],
            popup="0,083" + str(df_0083.loc[x]['Latitud']).replace(',', '.') + \
            ''+'' + str(df_0083.loc[x]['Longitud']).replace(',', '.'),
            icon=folium.Icon(color='red', icon='cloud')
        ).add_to(folium_map)
    for x, y in df_025.iterrows():
        # print('-----------------------------------',x,y)
        folium.Marker(
            # location=[y[0],y[1]],
            # popup=w["nombre"][x]
            location=[str(df_025.loc[x]['Latitud']).replace(',', '.'),
                      str(df_025.loc[x]['Longitud']).replace(',', '.')],
            popup="0,25" + str(df_025.loc[x]['Latitud']).replace(',', '.') + \
            ''+'' + str(df_025.loc[x]['Longitud']).replace(',', '.'),
            icon=folium.Icon(color='blue')
        ).add_to(folium_map)

    for x, y in df.iterrows():
        # print('-----------------------------------',x,y)
        folium.Marker(
            # location=[y[0],y[1]],
            # popup=w["nombre"][x]
            location=[str(df.loc[x]['Latitud']).replace(',', '.'),
                      str(df.loc[x]['Longitud']).replace(',', '.')],
            popup="Original" + str(df.loc[x]['Latitud']).replace(',', '.') + \
            ''+'' + str(df.loc[x]['Longitud']).replace(',', '.'),
            icon=folium.Icon(color='green')
        ).add_to(folium_map)
    folium_map.save('templates\\mapaChile.html')

    arregla_mapa()

    return render_template('mapas.html')


@app.route('/pruebas2')
def paginaprueba2():
    start_coords = (-37.25, -73.58333333333333)
    folium_map = folium.Map(location=start_coords, zoom_start=10)
    gjson = os.path.join(app.root_path, 'geojson/prueba.geojson')
    file = open(gjson, encoding='utf-8')
    geo_data = json.load(file)
    file.close()
    # print(geo_data)
    # imprimir playas
    w = geo_data['geometry']
    df_0083 = pd.read_excel('geojson\\playas0083_2.xlsx')
    df_025 = pd.read_excel('geojson\\playas025_2.xlsx')
    df = pd.read_excel('geojson\\playasSinRedondeoCoord.xlsx')

    # for x,y in enumerate(w['coordjuinates']):

    for x, y in df_025.iterrows():
        # print('-----------------------------------',x,y)
        folium.Marker(
            # location=[y[0],y[1]],
            # popup=w["nombre"][x]
            location=[str(df_025.loc[x]['Latitud']-0.001).replace(',', '.'),
                      str(df_025.loc[x]['Longitud']-0.001).replace(',', '.')],
            popup="0,25" + str(df_025.loc[x]['Latitud']).replace(',', '.') + \
            ''+'' + str(df_025.loc[x]['Longitud']).replace(',', '.'),
            icon=folium.Icon(color='blue')
        ).add_to(folium_map)

    for x, y in df_0083.iterrows():
        # print('-----------------------------------',x,y)
        folium.Marker(
            # location=[y[0],y[1]],
            # popup=w["nombre"][x]
            location=[str(df_0083.loc[x]['Latitud']).replace(',', '.'),
                      str(df_0083.loc[x]['Longitud']).replace(',', '.')],
            popup="0,083" + str(df_0083.loc[x]['Latitud']).replace(',', '.') + \
            ''+'' + str(df_0083.loc[x]['Longitud']).replace(',', '.'),
            icon=folium.Icon(color='red', icon='cloud')
        ).add_to(folium_map)

    for x, y in df.iterrows():
        # print('-----------------------------------',x,y)
        folium.Marker(
            # location=[y[0],y[1]],
            # popup=w["nombre"][x]
            location=[str(df.loc[x]['Latitud']).replace(',', '.'),
                      str(df.loc[x]['Longitud']).replace(',', '.')],
            popup="Original" + str(df.loc[x]['Latitud']).replace(',', '.') + \
            ''+'' + str(df.loc[x]['Longitud']).replace(',', '.'),
            icon=folium.Icon(color='green')
        ).add_to(folium_map)
    folium_map.save('templates\\mapaChile.html')

    arregla_mapa()

    return render_template('mapas.html')


def arregla_mapa():
    f = open('templates\\mapaChile.html', 'r')
    filedata = f.read()
    f.close()

    newdata = filedata.replace(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/>', '')
    newdata = newdata.replace(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css"/>', '')
    newdata = newdata.replace(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"/>', '')
    # newdata = newdata.replace('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css"/>','')

    f = open('templates\\mapaChile.html', 'w')
    f.write(newdata)
    f.close()


if __name__ == '__main__':
    app.run(debug=True)
