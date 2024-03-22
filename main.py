''' Correr api localmente con uvicorn main:app --reload'''
''' Llamar Online con https://pi01-misael-garcia-torres.onrender.com'''
''' Modificar con https://dashboard.render.com/web/srv-cnos3i6d3nmc73do7n9g/deploys/dep-cnosgdud3nmc73do9em0'''

import pandas as pd
from fastapi import FastAPI

app = FastAPI()

# lectura de los datos
df_PlayTimeGenre = pd.read_csv('df_PlayTimeGenre.csv', header=0)
df_UserForGenre = pd.read_csv('df_UserForGenre.csv', header=0)
df_UsersRecommend = pd.read_csv('df_UsersRecommend.csv', header=0)
df_UsersNotRecommend = pd.read_csv('df_UsersNotRecommend.csv', header=0)
df_sentiment_analysis = pd.read_csv('df_sentiment_analysis.csv', header=0)
df_recomendacion_juego = pd.read_csv('df_recomendacion_juego.csv', header=0)
df_recomendacion_usuario = pd.read_csv('df_recomendacion_usuario.csv', header=0)

# Endpoints de la API
# @profile
@app.get('/PlayTimeGenre/{genero}')
async def PlayTimeGenre(genero: str):
    """
    Devuelve el año con mas horas jugadas para dicho género.
    Devuelve mensaje de error de no encontrar un registro

    Parametros
    ----------
    genero : str
        El género para el que se quiere encontrar el año con más horas jugadas.

    Devuelve
    -------
    dict
        Un diccionario que contiene el año de lanzamiento con más horas jugadas para el género dado.

    Ejemplo
    --------
    \>\>\> PlayTimeGenre("FPS")

    >\> {'Año de lanzamiento con más horas jugadas para Género FPS': '2014'}

    Consultas de Ejemplo
    --------
    "Action", "Casual" o "Indie".
    """
    genero_original = genero
    genero = genero.lower()
    fila = df_PlayTimeGenre[df_PlayTimeGenre['genero'].str.lower() == genero]
    if len(fila) == 1:
        año = fila['año'].iloc[0]
        return {"Año de lanzamiento con más horas jugadas para Género {}: {}".format(genero_original, año)}
    else:
        return {"No se encontraron datos para el género {}".format(genero_original)}

@app.get('/UserForGenre/{genero}')
async def UserForGenre(genero: str):
    """
    Devuelve el usuario que acumula más horas jugagas para el genero dado.
    Devuelve una lista de acumulación de horas jugadas por dicho usuario.
    Devuelve mensaje de error de no encontrar un registro

    Parametros
    ----------
    genero : str
        El género para el cual se quiere encontrar el usuario con más horas jugadas y la lista de horas jugadas por año.

    Devuelve
    -------
    dict
        Un diccionario que contiene el usuario con más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

    Ejemplo
    --------
    \>\>\> PUserForGenre("FPS")
    
    >\> {'Usuario con más horas jugadas para Género Shooter:': 'us213ndjss09sdf', 'Horas jugadas': [{'Año': 2013, 'Horas': 203}, {'Año': 2012, 'Horas': 100}, {'Año': 2011, 'Horas': 23}]}
    
    Consultas de Ejemplo
    --------
    "Action", "Casual" o "Indie".
    """
    genero_original = genero
    genero = genero.lower()
    df_genero = df_UserForGenre[df_UserForGenre['genero'] == genero]
    if df_genero.empty:
        return {"No se encontraron datos para el género {}".format(genero_original)}
    usuario = df_genero.groupby('user_id')['horas_jugadas'].sum().idxmax()
    horas = df_genero.groupby('año')['horas_jugadas'].sum().reset_index().to_dict(orient='records')
    return {f'Usuario con más horas jugadas para el Género {genero_original}:': usuario, 'Horas jugadas': horas}

@app.get('/UsersRecommend/{anio}')
async def UsersRecommend(anio: int):   
    """
    Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.
    Devuelve mensaje de error de no encontrar un registro
    
    Parametros
    ----------
    anio : int
        El año para el cual se desea obtener el top 3 de juegos más recomendados.
    
    Devuelve
    ----------
    list
        Una lista de diccionarios que contiene los juegos más recomendados para el año dado.
    
    Ejemplo
    --------
    \>\>\> UsersRecommend(2023)
    
    >\> [{'Puesto 1': 'The Witcher 3'}, {'Puesto 2': 'Red Dead Redemption 2'}, {'Puesto 3': 'Grand Theft Auto V'}]
    
    Consultas de Ejemplo
    --------
    2012, 2015 o 2017.
    """
    df_año = df_UsersRecommend[df_UsersRecommend['año'] == anio]
    if df_año.empty:
        return {"No se encontraron datos para el año {}".format(anio)}
    top = df_año.head(3)
    return [{'Puesto ' + str(row['puesto']): row['juego']} for _, row in top.iterrows()]

@app.get('/UsersNotRecommend/{anio}')
async def UsersNotRecommend(anio: int):
    """
    Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.
    Devuelve mensaje de error de no encontrar un registro
    
    Parametros
    ----------
    anio : int
        El año para el cual se desea obtener el top 3 de juegos menos recomendados.
    
    Devuelve
    ----------
    list
        Una lista de diccionarios que contiene los juegos menos recomendados para el año dado
    
    Ejemplo
    --------
    \>\>\> UsersNotRecommend(2023)
    
    >\> [{'Puesto 1': 'The Witcher 3'}, {'Puesto 2': 'Red Dead Redemption 2'}, {'Puesto 3': 'Grand Theft Auto V'}]
    
    Consultas de Ejemplo
    --------
    2012, 2015 o 2017.
    """
    df_año = df_UsersNotRecommend[df_UsersNotRecommend['año'] == anio]
    if df_año.empty:
        return {"No se encontraron datos para el año {}".format(anio)}
    top = df_año.head(3)
    return [{'Puesto ' + str(row['puesto']): row['juego']} for _, row in top.iterrows()]

@app.get('/sentiment_analysis/{anio}')
async def sentiment_analysis(anio: int):
    """
    Devuelve una lista con la cantidad de registros de reseñas positivos, neutrales y negativos según el año de lanzamiento, categorizados según análisis de sentimiento.
    Devuelve mensaje de error de no encontrar un registro
    
    Parametros
    ----------
    anio : int
        El año para el cual se quiere la información del análisis de sentimiento.

    Devuelve
    -------
    dict
        Un diccionario que contiene la cantidad de registros para cada categoría de sentimiento.

    Ejemplo
    --------
    \>\>\> sentiment_analysis(2023)
    
    >\> {'Negative': 182, 'Neutral': 120, 'Positive': 278}
    
    Consultas de Ejemplo
    --------
    2012, 2015 o 2017.
    """
    df_año = df_sentiment_analysis[df_sentiment_analysis['año'] == anio]
    if df_año.empty:
        return {"No se encontraron datos para el año {}".format(anio)}
    return df_año.groupby('categoria')['cantidad'].sum().to_dict()

@app.get('/recomendacion_juego/{id_juego}')
async def recomendacion_juego(id_juego: int):
    """
    Devuelve una Lista de recomendación con 5 juegos similares al ingresado.
    Devuelve mensaje de error de no encontrar un registro
    
    Parametros
    ----------
    id : int
        El id del juego para el cual se desea obtener la recomendación de 5 juegos.

    Devuelve
    -------
    dict
        Un diccionario que contiene los 5 juegos recomendados.

    Ejemplo
    --------
    \>\>\> recomendacion_juego(04958)
    
    >\> {'Juegos recomendados para el juego Call Of Duty: Modern Warfare 3:': {'Call Of Duyty World War II', 'Battlefield One',  'Medal of Honor Allied Assault',  'Call Of Duty 4 Modern Warfare',  '',  '', }]}
    
    Consultas de Ejemplo
    --------
    123456, 456456 o 777999.
    """
    df_id_juego = df_recomendacion_juego[df_recomendacion_juego['id_juego'] == id_juego]
    if df_id_juego.empty:
        return {"No se encontraron datos para el id {}".format(id_juego)}
    top = df_id_juego.head(5)
    nombre_juego = df_id_juego['nombre_juego'].iloc[0]
    juegos_recomendados = {'Juegos recomendados para el juego {}:'.format(nombre_juego): set(top['juego'])}
    return juegos_recomendados

@app.get('/recomendacion_usuario/{id_usuario}')
async def recomendacion_usuario(id_usuario: str):
    """
    Devuelve una Lista de recomendación con 5 juegos recomendados para dicho usuario.
    Devuelve mensaje de error de no encontrar un registro
    
    Parametros
    ----------
    id : int
        El id del usuario para el cual se desea obtener la recomendación de 5 juegos.

    Devuelve
    -------
    dict
        Un diccionario que contiene los 5 juegos recomendados.

    Ejemplo
    --------
    \>\>\> recomendacion_juego(04958)
    
    >\> {'Juegos recomendados para el usuario Aspirina180mg:': {'Call Of Duyty World War II', 'Battlefield One',  'Medal of Honor Allied Assault',  'Call Of Duty 4 Modern Warfare',  '',  '', }]}
    
    Consultas de Ejemplo
    --------
    "pepito", "juanito" o "sabito".
    """
    id_original = id_usuario
    id_usuario = id_usuario.lower()
    df_id_usuario = df_recomendacion_usuario[df_recomendacion_usuario['id_usuario'] == id_usuario]
    if df_id_usuario.empty:
        return {"No se encontraron datos para el usuario {}".format(id_original)}
    top = df_id_usuario.head(5)
    juegos_recomendados = {'Juegos recomendados para el usuario {}:'.format(id_original): set(top['juego'])}
    return juegos_recomendados