# Proyecto de Data Analytics para Observatorio de Movilidad y Seguridad Vial (OMSV)

Este proyecto de análisis de datos se centra en la creación de un dashboard y en la toma de decisiones sobre datos de homicidios en siniestros viales registrados en la Ciudad Autónoma de Buenos Aires (CABA) durante el periodo de 2016 a 2021, el objetivo principal es el de disminuir la cantidad de fictimas fatales.
Los resultados de éste análisis serán cargados en un Dashboard interactivo en un enlace público.

# Tabla de contenidos
1. [Cómo Ejecutar el Proyecto](#ejecutar)
2. [Guía de uso rápido](#usorapido)
3.  [Data Analytics](#dataengineer)
    1. [Repositorio y Conjuntos de Datos](#datos)
    2. [Preprocesamiento de Datos](#preprocesamiento)
    3. [Descripción del Proyecto](#descripcion)
4. [Análisis de datos](#analisis)
5. [KPIs](#kpis)
6. [Pánel de control o Dashboard](#dashboard)
7. [Contribuciones y Colaboraciones](#contribuciones)
8. [Links](#links)
9. [Licencia](#licencia)
10. [Contacto](#contacto)
11. [Menciones y agradecimientos](#menciones)
------------------------------------------------------------------------------------------------------------------------------------
<a name="ejecutar"></a>

## Cómo Ejecutar el Proyecto 

Para ejecutar el proyecto localmente, sigue estos pasos:

1. Clona el repositorio desde [GitHub](https://github.com/Aspirina180mg/PI02_Misael_Garcia_Torres).
2. Instala las dependencias del proyecto utilizando el archivo `requirements.txt`, abriendo el terminal en la carpeta raíz del proyecto y corriendo el comando `> pip install -r requirements.txt` en la consola
    1. Nota que el proyecto fué creado con Python 3.11.6, se recomienda usar la misma versión.
3. Ejecuta el archivo `ETL.ipynb` en un entorno de Jupyter Notebook o Google Colab, éste llamara los archivos xlsx almacenados en la carpeta `Datasets`, realizará limpieza de datos y los exportará en la misma carpeta con formato .parquet, si deseas modificar los archivos se recomienda mantener la estructura original para simplificar la operación.
4. Ejecuta el archivo `EDA.ipynb` en un entorno de Jupyter Notebook o Google Colab, éste llamara los archivos parquet almacenados en la carpeta `Datasets` y realizará gráficos que entregan información significativa de la exploración de datos, se recomienda obviar las conclusiones descritas en el docmento si se va a modificar los datos en el paso anterior.
5. Prueba el dashboard, ejecutando el archivo main.py, si ejecuta de manera correcta, entregará el mensaje de correr el comando `streamlit run z:/PI02_Misael_Garcia_Torres/main.py [ARGUMENTS]` en la carpeta raíz del proyecto, una vez realizado esto podrás ingresar al localhost para visualizar el dashboard interactivo.
    1. Para poder visualizar el dashboard puedes debes seguir los enlaces que te mostrará la terminal, normalmente utilizando el [localhost (127.0.0.1:8501)](127.0.0.1:8501)
6. Hacer deploy en streamlit, si posees o te creas una cuenta en [Streamlit](https://streamlit.io/), puedes hacer tu propio deploy de la API

<a name="usorapido"></a>

## Guía de uso rápido

Se recomienda sólo agregar información a los archivos originales del proyecto, puedes cargar tus propios archivos xlsx con bases de datos similares a las encontradas en este repositorio, pero la carga a los dataframes del proyecto los tendrás que hacer maunualmente.
Una vez hayas finalizado la ejecución del archivo `ETL.ipynb` podrás cargar el dashboard (main.py) de manera local, o hacer un deploy en Streamlit.

<a name="dataengineer"></a>

## Data Analytics

<a name="datos"></a>

### Repositorio y Conjuntos de Datos

- El repositorio original del proyecto se encuentra disponible en [GitHub](https://github.com/soyHenry/PI_DA/tree/Full_Time).
- Los conjuntos de datos utilizados se encuentran disponibles en el portal oficial de [Buenos Aires Data (BA Data)](https://data.buenosaires.gob.ar/dataset/victimas-siniestros-viales).

<a name="preprocesamiento"></a>

### Preprocesamiento de datos

- Se realiza la carga y limpieza de los conjuntos de datos utilizando Python y las siguientes librerías:
  - numpy
  - pandas
  
  puedes revisar más en detalle los pasos realizados dentro del archivo [`ETL.ipynb`](https://github.com/Aspirina180mg/PI02_Misael_Garcia_Torres/blob/main/ETL.ipynb)

<a name="descripcion"></a>

### Descripción del Proyecto

El proyecto se divide en las siguientes secciones principales:

1. **ETL:** Exploración, transformación y carga de los conjuntos de datos, realizando los primeros análisis y preparándolos para ser procesados en mayor profundidad.
2. **EDA:** Análisis exploratorio, proceso para comprender los datos y sacar conclusiones de los mismos, en este caso, para decidir qué información mostrar en el dashboard.
3. **Creación de Dashboard:** Se genera un pánel con la información que se estima necesaria para poder comprender los datos de manera rápida, éste no sólo muestra gráficos, sino que es interactivo y permite filtrar la información de manera dinámica.

<a name="analisis"></a>

## Análisis de datos

Los datos se cargaron en el dataframe df_homicidios, el cual cuenta con 18 columnas, de las cuales se determinó que las columnas principales son 6, HORA, EDAD, ACUSADO, VICTIMA, ROL y SEXO, ésto fue determinado analisando los gráficos de los datos por separado, aún pese a determinarse como datos principales, no se descartan las demás columnas del dataframe.

Se realizaron análisis monovariados y bivariados, en búsqueda de conclusiones que denotaran una imágen más clara sobre los motivos de la alta fatalidad en accidentes víales, o sobre los focos de acción para evitarlos.

### **Análisis Monovariados**

*   HORA

Se identificó un foco de accidentes en el horario de entre las 6 y las 11 am, éste foco es leve y no es algo significativo.
Se puede determinar que hay fatalidades durante todas las horas del día, contradiciendo la hipótesis de que habría más accidentes fatales durante la noche.

*   EDAD

Se identifica un fuerte foco en las edades entre 25 y 35 años, lo que podría indicar que los conductores jóvenes sufren más accidentes fatales en la vía, esto puede deberse a sobre-confianza o a la inexperiencia al volante.

*   ACUSADO

Se observa que la mayor cantidad de accidentes son en Autos, lo que se justifica considerando que los vehículos personales son los que más circulan en la ciudad.

*   VICTIMA

El tipo de transporte con más Víctimas fatales son las motocicletas, observación lógica, considerando que frente a los autos, una moto no ofrece protección para su conductor o su pasajero.

*   ROL

El Rol más común de las víctimas es el de conductor, llamando la atención que esta medida sobrepasa a los peatones, quienes no tienen la protección del vehículo ante accidentes.

*   SEXO

Al comparar Hombres y Mujeres, sus estadísticas se contrastan fuertemente, los hombres fallecen 3 veces más que las mujeres.

### **Análisis Bivariados**

*   Relación entre EDAD y SEXO

Se observa que al comparar los fallecimientos de hombres vs mujeres, al ordenarlos por edad, los hombres fallecen a edades más jóvenes que las mujeres.
También se observa que hay una forma de campana en los datos, significando que hay una distribución normal.

*   Relación entre ACUSADO y VÍCTIMA

Llama la atención que por sobre todos los otros Acusados, los vehículos de pasajeros, con víctimas de peatones, son la combinación con mayor frecuencia, incluso por sobre los accidentes en Auto, podría deberse a la forma de conducir de los transportes públicos, claramente un dato en el que se puede profundizar con más información.

*   Relación entre SEXO y ROL

Lo más llamativo de toda la investigación, el análisis acusa que los conductores hombres fallecen 15 veces más que las conductoras mujeres.


*Conclusión*
Que los hombres fallezcan 15 veces más que las mujeres al estar conduciendo indica claramente que la diferencia de edad en los fallecimientos entre ambos sexos no es una coincidencia, se puede concluir que la edad del conductor juega un rol primordial sobre la forma de conducción y el cuidado al volante, los hombres parecen tener tendencias más temerarias, lo que lleva a más accidentes, también se puede complementar con las observaciones anteriores, si se considera que es más común ver hombres, conduciendo vehículos de transporte público.

<a name="kpis"></a>

## KPIs

Se determinaron 3 KPIs que supervisar que ayudarán a disminuir la cantidad de fallecimientos totales.

1. Tasa de homicidios

La tasa de homicidios tiene relación con la cantidad de muertes por cada 100.000 habitantes, es el KPI principal, ya que si disminuye, indica que la población está teniendo un mayor cuidado al volante.

2. Cantidad de Fallecimientos en Moto

Como el transporte con más Fallecidos, se justifica la monitorización de este KPI, si disminuye significa que se está respetando tanto a los conductores de motocicletas, como las leyes de tránsito, ya que las motos son más propensas a accidentes por no respetar la señalética de tránsito, por ejemplo.

3. Conductores Involucrados en accidentes fatales

Este KPI se deriva en parte del anterior, puede indicar una falta de uso de cinturón de seguridad, así como poco cuidado en la conducción, si disminuye tendría un gran impacto en la cantidad total de accidentes fatales.

<a name="dashboard"></a>

## Pánel de datos o Dashboard

El dashboard ofrece una manera rápida para hacer seguimiento a los KPIs, se seleccionó, además, indicadores relacionados que pueden ayudar a la comprensión de los mismos, y apoyar en la toma de desiciones.

El dashboard cuenta con los siguientes indicadores:
*   Homicidios en motocicletas el último año y en promedio
*   Homicidios totales este semestre y en promedio
*   Homicidios de Conductores este semestre y en promedio
*   Diferencia de homicidios en moto este año vs el anterior
*   Diferencia en Tasa de homicidios este semestre vs el anterior
*   Diferencia homicidios de conductores este año vs el anterior
*   Distribución de víctimas
*   Relación Acusado-víctima
*   Distribución de Rol de las víctimas

![Dashboard](/SRC/image.png)

El dashboard cuenta con filtros, los que actualizan en tiempo real los gráficos que se púeden observar, es posible que algunas combinaciones de datos den errores ya que los gráficos necesitan entre 1 y 2 años de datos para realizar los cálculos, un error común es la división por cero, afortunadamente el dashboard no se crashea, sino que sólo entrega un aviso de error, si se corrigen los filtros, todo vuelve a funcionar normal, se recomienda que ante cualquier error en la graficación, se reinicien todos los filtros.

<a name="contribuciones"></a>

## Contribuciones y Colaboraciones

Se aceptan contribuciones al proyecto, puede enviar una solicitud de extracción (pull request) o abrir un problema (issue) en el repositorio de GitHub.

<a name="links"></a>

## Links

Proyecto Original: https://github.com/soyHenry/PI_DA/tree/Full_Time?tab=readme-ov-file

Repositorio: https://github.com/Aspirina180mg/PI02_Misael_Garcia_Torres/blob/main/ETL.ipynb


Seguimiento de problemas: https://github.com/Aspirina180mg/PI02_Misael_Garcia_Torres/issues
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

Para la realización de este proyecto se utilizaron los conocimientos adquiridos en el Bootcamp de Data Science del Equipo de "[Henry](https://web.soyhenry.com/about-us)", agradezco también a mis TAs Rafael Alvarez y Roberto Schaefer, quienes me acompañaron durante todo el proceso, son unos cracks,
a javier Bengolea, mi compañero TA, de pocas palabras, pero infinita sabiduría, el agradecimiento final va a mi señora, Kimberly Moya, y a mi hijo Javier García, por apoyarme y aguantarme durante la realziación de este y todos mis proyectos.
