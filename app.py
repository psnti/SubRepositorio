from flask import Flask,render_template,send_from_directory
from flask_bootstrap import Bootstrap
import folium
import os
import json
import pandas as pd


app = Flask(__name__)
Bootstrap(app)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static','pics'),
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
    start_coords = (-34.536267, -72.406639)
    folium_map = folium.Map(location=start_coords, zoom_start=5)
    gjson = os.path.join(app.root_path, 'geojson/prueba.geojson')
    file = open(gjson,encoding='utf-8')
    geo_data = json.load(file)
    file.close()
    #print(geo_data)
    #imprimir playas
    w = geo_data['geometry']
    df = pd.read_excel('geojson\\playas.xlsx')
    #for x,y in enumerate(w['coordjuinates']):
    for x,y in df.iterrows():
        #print('-----------------------------------',x,y)
        folium.Marker(
            #location=[y[0],y[1]],
            #popup=w["nombre"][x]
            location = [str(df.loc[x]['Latitud']).replace(',','.'),str(df.loc[x]['Longitud']).replace(',','.')],
            popup=str(df.loc[x]['Latitud']).replace(',','.') +''+''+ str(df.loc[x]['Longitud']).replace(',','.')
        ).add_to(folium_map)
        
    folium_map.save('templates\\mapaChile.html')
    
    arregla_mapa()

    return render_template('mapas.html')


def arregla_mapa():
    f = open('templates\\mapaChile.html','r')
    filedata = f.read()
    f.close()

    newdata = filedata.replace('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/>','')
    newdata = newdata.replace('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css"/>','')
    newdata = newdata.replace('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"/>','')
    # newdata = newdata.replace('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css"/>','')

    f = open('templates\\mapaChile.html','w')
    f.write(newdata)
    f.close()

if __name__ == '__main__':
    app.run(debug = True)


