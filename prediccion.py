import xarray as xr
import pandas as pd
from joblib import load
import os
import math
from datetime import datetime,timedelta
from sklearn import preprocessing

def redondeo(coordenadas, base=1/12):
    """
    Devuelve las coordenadas pasadas redondeadas
    
    Parametros:
    coordenadas -- lista de latitud y longitud
    base -- base del redondeo
    """
    return  base * round(coordenadas/base)

def genera_fechas(f):
    lista_fechas = []
    for i in range(5):
        fecha= datetime.strptime(f, '%Y-%m-%d')
        fecha += timedelta(days=i)
        lista_fechas.append(str(fecha))
    return lista_fechas

def dame_lista(df):
    Row_list = []
    for index, rows in df.iterrows(): 
        my_list =[rows.mlotst, rows.zos, rows.bottomT, rows.thetao, rows.so,
                 rows.uo, rows.vo] 
        Row_list.append(my_list) 

    # Print the list 
    return Row_list

def busca_archivo(fecha):
    """
    Devuelve el archivo .nc de la fecha pasada por parametro
    
    Parametros:
    fecha -- fecha en formato AñoMesDia (20140105)
    """
    listado_archivos = os.listdir('C:\\Users\pablo\Desktop\medusas\documentos\copernicus') # Listo todos los archivos de Copernicus
    texto ='_{}_'.format(str(fecha).split()[0].replace('-',''))
    archivo = [x for x in listado_archivos if str(texto) in x]
    data = xr.open_dataset('C:\\Users\pablo\Desktop\medusas\documentos\copernicus\{}'.format(archivo[0])) # cargo el archivo
    return data # devuelvo dataset

def dame_coordenadas(c):
    paso = 1/12
    return [[c[0],c[1]],
            [c[0],c[1]-paso],[c[0]+paso,c[1]-paso],[c[0]+(paso*2),c[1]-paso],[c[0]-paso,c[1]-paso],[c[0]-(paso*2),c[1]-paso],
           [c[0],c[1]-(2*paso)],[c[0]+paso,c[1]-(2*paso)],[c[0]+(paso*2),c[1]-(2*paso)],[c[0]-paso,c[1]-(2*paso)],[c[0]-(paso*2),c[1]-(2*paso)]]

def comprueba_datos(latitud,longitud,ds):
    """
    Comprueba si el dataset contiene valores en las coordenadas pasadas
    
    Devuelve las coordenadas mas cercanas con datos 
    
    Parametros:
    latitud -- latitud
    longitud -- longitud
    ds -- dataset del que extraer los valores
    """
    salto = 1/12
    valor = dame_datos(latitud,longitud,ds)
    while math.isnan(valor.mlotst[0]):
        longitud = longitud - salto
        valor = dame_datos(latitud,longitud,ds)
    return latitud,longitud # devuelvo las coordenadas con datos

def dame_datos(latitud,longitud,ds):
    """
    Devuelve los datos del dataset en las coordenadas pasadas
    
    Parametros:
    latitud -- latitud 
    longitud -- longitud
    ds -- dataset del que extraer los valores
    """
    return ds.sel({'latitude':latitud,'longitude': longitud})

def normaliza_min_max(df_atributos):
    """
    Normaliza los datos del dataframe pasado
    """
    X = df_atributos.values.tolist()
    n = load('normalizador.pkl') 
    x_normalizado_2 = n.transform(X)
    df_norm = pd.DataFrame(x_normalizado_2,columns=list(range(231)))
    return df_norm

def genera_estructura(f,c):
    dataframe = pd.DataFrame(columns=list(range(231)))
    fechas = genera_fechas(f)
    for index,dia in enumerate(fechas):
        listado_variables = []
        # cargo el dataset
        ds =busca_archivo(dia) # cambiar para cada dia
        c = comprueba_datos(c[0],c[1],ds)
        coord = dame_coordenadas(c)

        for j in coord:
            variables1 = ds.sel({'latitude':coord[0][0],'longitude': coord[0][1], 'depth' : 0 },method='nearest').to_dataframe()
            l1 = dame_lista(variables1)[0]
            variables2 = ds.sel({'latitude':coord[1][0],'longitude': coord[1][1], 'depth' : 5 },method='nearest').to_dataframe()
            l2 = dame_lista(variables2)[0]
            variables3 = ds.sel({'latitude':coord[2][0],'longitude': coord[2][1], 'depth' : 10},method='nearest').to_dataframe()
            l3 = dame_lista(variables3)[0]
            l1+=l2
            l1+=l3
            listado_variables+=(l1)
        dataframe.loc[index] = listado_variables
    return dataframe

def genera_resultados(fecha, coordenadas):
    # se cogerian los datos de copernicus
    # generar dataframe
    #normalizarlo
    # meterlo al modelo
    modelo = load('C:\\Users\pablo\Desktop\medusas\static\modelo.joblib')
    df,fechas = genera_estructura(fecha,coordenadas)
    df = normaliza_min_max(df)
    salida = modelo.predict(df)
    print(salida,fechas)
    lista_salida = []
    for avist,date in zip(salida,fechas):
        lista_salida.append({'y':date,'v':int(avist)})
    return lista_salida
