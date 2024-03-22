# Proyecto de Ciencia de Datos para Steam

Este proyecto de ciencia de datos se centra en el análisis de datos relacionados con Steam, la plataforma de distribución de videojuegos de Valve Corporation. El objetivo principal es realizar análisis y extracciones de información relevante para la recomendación de juegos al usuario, entregando más valor a su experiencia en la plataforma, los resultados de estos análisis serán cargados en una API

## Video de demostración
[![Watch the video](https://img.youtube.com/vi/wPvSoBxv7Og/maxresdefault.jpg)](https://www.youtube.com/watch?v=wPvSoBxv7Og)

https://youtu.be/wPvSoBxv7Og
 
# Tabla de contenidos
1. [Cómo Ejecutar el Proyecto](#ejecutar)
2. [Guía de uso rápido](#usorapido)
3.  [Data Engineering](#dataengineer)
    1. [Repositorio y Conjuntos de Datos](#datos)
    2. [Preprocesamiento de Datos](#preprocesamiento)
    3. [Descripción del Proyecto](#descripcion)
4. [Funciones de la API](#funciones)
5. [Deployment y la API](#deploy)
6. [Archivos Generados](#archivos)
7. [Contribuciones y Colaboraciones](#contribuciones)
8. [Links](#links)
9. [Licencia](#licencia)
10. [Contacto](#contacto)
11. [Menciones y agradecimientos](#menciones)
------------------------------------------------------------------------------------------------------------------------------------
<a name="ejecutar"></a>

## Cómo Ejecutar el Proyecto 

Para ejecutar el proyecto localmente, sigue estos pasos:

1. Clona el repositorio desde [GitHub](https://github.com/Aspirina180mg/PI01_Misael_Garcia_Torres).
2. Instala las dependencias del proyecto utilizando el archivo `requirements_jupyter.txt`, abriendo el terminal en la carpeta raíz del proyecto y corriendo el comando `> pip install -r requirements_jupyter.txt` en la consola
    1. Nota que el proyecto fué creado con Python 3.11.6, se recomienda usar la misma versión.
3. Ejecuta el archivo `PI01_Misael_Garcia_Torres.ipynb` en un entorno de Jupyter Notebook o Google Colab, éste llamara los archivos csv almacenados en `PI MLOps - STEAM.zip`, si deseas modificar los archivos se recomienda mantener la estructura original para simplificar la operación.
4. Explora y ejecuta las celdas según sea necesario para realizar análisis y obtener resultados.
    1. Nota que puedes ejecutar las distintas celdas en el orden que desees y las veces que desees.
    2. El proyecto fue creado usando Google Colab y la limitación principal era que sólo se contaba con 12.7 GB de memoria RAM.
5. Prueba la api, utilizando el comando `uvicorn main:app -reload` en la carpeta raíz del proyecto, una vez realizado esto podrás ingresar al localhost para ver la documentación sobre su funcionamiento y probar algunas búsquedas.
    1. Para probar la api debes ingresar a tu [localhost (127.0.0.1:8000/docs)](127.0.0.1:8000/docs)
6. Hacer deploy en Render, si posees o te creas una cuenta en [Render](https://render.com/), puedes hacer tu propio deploy de la API.Los ajustes usados para hacer el deploy son los siguientes
    1. Repositorio de github, debes ingresar el enlace del clon que hiciste al repositorio original.
    2. Branch del repositori, si no haz modificado esto en el repositorio, será main.
    3. Directorio Raíz, debes dejarlo en blanco, ya que es el mismo que el propio directorio raíz del repositorio.
    4. Comando de armado (Build Command), debes escribir `pip install -r requirements.txt` para que lea el archivo requirements.txt del repositorio enlacado en el punto 5.1.
    5. Comando previo al deploy, no hay, déjalo en blanco
    6. Comando de inicio, usarás `uvicorn main:app --host 0.0.0.0 --port $PORT` para que el puerto sea dinámico.


<a name="usorapido"></a>

## Guía de uso rápido

Se recomienda sólo agregar información a los archivos originales del proyecto, puedes cargar tus propios archivos csv con bases de datos similares a las encontradas en este repositorio, pero la carga a los dataframes del proyecto los tendrás que hacer maunualmente.
Una vez hayas finalizado la ejecución del archivo `PI01_Misael_Garcia_Torres.ipynb` podrás cargar la api de manera local, o hacer un deploy en Render.

<a name="dataengineer"></a>

## Data Engineering

<a name="datos"></a>

### Repositorio y Conjuntos de Datos

- El repositorio original del proyecto se encuentra disponible en [GitHub](https://github.com/soyHenry/PI_ML_OPS/tree/PT?tab=readme-ov-file).
- Los conjuntos de datos utilizados se encuentran disponibles en [Google Drive](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj).

<a name="preprocesamiento"></a>

### Preprocesamiento y análisis de Datos

- Se realiza la carga y limpieza de los conjuntos de datos utilizando Python y las siguientes librerías:
  - ast
  - nltk
  - pandas
  - numpy
  - matplotlib
  - wordcloud
  - sklearn
  - seaborn
  
  puedes revisar más en detalle los pasos realizados dentro del archivo [`PI01_Misael_Garcia_Torres.ipynb`](https://colab.research.google.com/drive/1fNHTxOLO9_OX4gVw3RFdsqvvzBtRrjLS#scrollTo=WKs6ccEbpP9J)

<a name="descripcion"></a>

### Descripción del Proyecto

El proyecto se divide en las siguientes secciones principales:

1. **Exploración de Datos:** Análisis inicial de los conjuntos de datos para comprender su estructura y características.
2. **Limpieza de Datos:** Proceso de limpieza y preprocesamiento de los datos para eliminar valores nulos, duplicados y realizar correcciones.
3. **Transformación de Datos:** Conversión de tipos de datos, extracción de información relevante y preparación de los datos para su análisis.
4. **Análisis de Sentimientos:** Utilización de análisis de sentimientos para evaluar las opiniones de los usuarios en las reseñas de juegos, se utiliza la librería nltk y el vader_lexicon
5. **Generación de Reportes:** Creación de visualizaciones y reportes estadísticos para identificar patrones y tendencias en los datos.

<a name="funciones"></a>

## Funciones de la API

El proyecto también incluye la implementación de una API para proporcionar acceso a datos procesados y funcionalidades específicas. Esta fue desarrollada en el archivo `main.py`.
Las principales funciones de la API incluyen:

1. **PlayTimeGenre():** Devuelve el año con más horas jugadas para un género específico.
2. **UserForGenre():** Devuelve el usuario con más horas jugadas para un género específicoy el detalle de la acumulación de horas anual para este usuario.
3. **UsersRecommend():** Devuelve un top 3 con los juegos más recomendados por usuarios para un año dado.
4. **UsersNotRecommend():** Devuelve un top 3 con los juegos menos recomendados por usuarios para un año dado.
5. **SentimentAnalysis():** devuelve la cantidad de comentarios positivos, neutrales y negativos para un año dado.
6. **recomendacion_juegos():** Devuelve un top 5 de los juegos similares al juego dado.
7. **recomendacion_usuario():** Devuelve un top 5 de los juegos recomendados para el usuario dado.

para más información se puede consultar la documentación de la api en :
[https://pi01-misael-garcia-torres.onrender.com/docs](https://pi01-misael-garcia-torres.onrender.com/docs)

<a name="deploy"></a>

## Deployment
La API puede ser probada en local utilizando uvicorn con el siguiente comando dentro de la carpeta raíz del proyecto:

```bash
uvicorn main:app --reload
```

la API está deployada en Render, cada modificación hecha en el archivo `main.py` se verá de forma automática en uvicorn, pero debe ser actualizada manualmente en el Deploy de Render.

<a name="archivos"></a>

## Archivos Generados

El proyecto genera un archivo para cada función de la API, con datos preprocesados y resultados de análisis para su consulta.

- `df_PlayTimeGenre`: tiene la estructura {genero,año}
- `df_UserForGenre`: tiene la estructura {genero,user_id,año,horas_jugadas}
- `df_UsersRecommend`: tiene la estructura {año,puesto,juego}
- `df_UsersNotRecommend`: tiene la estructura {año,puesto,juego}
- `df_SentimentAnalysis`: tiene la estructura {año,categoria,cantidad}
- `df_recomendacion_juegos`: tiene la estructura {id_juego,nombre_juego, puesto, juego}
- `df_recomendacion_usuario`: tiene la estructura {id_usuario, puesto, juego}

*Nota* los resultados de df_recomendacion_juegos y df_recomendacion_usuario fueron creados aplicando el modelo de similitud del coseno.
*Nota 2* durante el proceso estándar se desempaquetan los archivos `Diccionario de Datos STEAM.xlsx`, `steam_games.son.gz`, `user_reviews.json.gz` y `user_items.json.gz` en la carpeta `PI MLOps - STEAM`.

<a name="contribuciones"></a>

## Contribuciones y Colaboraciones

Se aceptan contribuciones al proyecto, puede enviar una solicitud de extracción (pull request) o abrir un problema (issue) en el repositorio de GitHub.

<a name="links"></a>

## Links

Proyecto Original: https://github.com/soyHenry/PI_ML_OPS/tree/PT?tab=readme-ov-file
Repositorio: https://github.com/Aspirina180mg/PI01_Misael_Garcia_Torres
Seguimiento de problemas: https://github.com/Aspirina180mg/PI01_Misael_Garcia_Torres/issues
  - En caso de bugs sensibles como vulnerabilidades de seguridad, por favor
    contacte directamente al correo misagtor@gmail.com en lugar de abrir un 
    problema (issue), esto para agilizar el proceso de resolución.

<a name="licencia"></a>

## Licencia

Este proyecto se distribuye bajo la [licencia MIT](https://choosealicense.com/licenses/mit/). Consulta el archivo `LICENSE.txt` para obtener más detalles.

<a name="contacto"></a>

## Contacto

Para obtener más información o realizar preguntas sobre el proyecto, puedes ponerte en contacto con el autor:

- Nombre: Misael García Torres
- Teléfono: +56 931 854 247
- Correo Electrónico: [misagtor@gmail.com)
- LinkedIn: [linkedin.com/in/mgarciat](https://www.linkedin.com/in/mgarciat/)

<a name="menciones"></a>

## Menciones y agradecimientos

Para la realización de este proyecto se utilizaron los conocimientos adquiridos en el Bootcamp de Data Science del Equipo de "[Henry](https://web.soyhenry.com/about-us)", agradezco también a mis TAs Rafael Alvarez y Roberto Schaefer, quienes me acompañaron durante todo el proceso, son unos cracks, el agradecimiento final va a mi señora Kimberly Moya y a mi hijo Javier García, por apoyarme y aguantarme durante la realziación de este y todos mis proyectos.
