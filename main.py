import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Lectura de los datos
df_homicidios = pd.read_parquet("Datasets/df_homicidios.parquet")

# Función para calcular KPIs
def calcular_kpis(df_homicidios):
    # KPI 1: Reducción en un 10% de la tasa de homicidios en siniestros viales
    # de los últimos seis meses en CABA, en comparación con el semestre anterior.
    homicidios_ultimo_semestre = df_homicidios[df_homicidios['FECHA'].dt.month.isin([1, 2, 3, 4, 5, 6])]
    homicidios_anterior_semestre = df_homicidios[df_homicidios['FECHA'].dt.month.isin([7, 8, 9, 10, 11, 12])]

    tasa_homicidios_ultimo_semestre = len(homicidios_ultimo_semestre) / len(homicidios_anterior_semestre) * 100

    # KPI 2: Reducción en un 7% de la cantidad de accidentes mortales de motociclistas
    # en el último año en CABA, respecto al año anterior.
    accidentes_ultimo_anio = df_homicidios[df_homicidios['FECHA'].dt.year == df_homicidios['FECHA'].dt.year.max()]
    accidentes_anio_anterior = df_homicidios[df_homicidios['FECHA'].dt.year == df_homicidios['FECHA'].dt.year.max() - 1]

    motociclistas_ultimo_anio = accidentes_ultimo_anio[accidentes_ultimo_anio['VICTIMA'] == 'MOTO']
    motociclistas_anio_anterior = accidentes_anio_anterior[accidentes_anio_anterior['VICTIMA'] == 'MOTO']

    reduccion_motociclistas = (len(motociclistas_anio_anterior) - len(motociclistas_ultimo_anio)) / len(motociclistas_anio_anterior) * 100

    # KPI 3: Tasa de homicidios en siniestros viales por grupo de edad
    homicidios_por_grupo_edad = df_homicidios.groupby(pd.cut(df_homicidios['EDAD'], bins=np.arange(0, 101, 10), include_lowest=True, right=False).astype(str))['ID'].count()


    return tasa_homicidios_ultimo_semestre, reduccion_motociclistas, homicidios_por_grupo_edad

# Función para mostrar el dashboard
def mostrar_dashboard():
    # Título
    st.title("Dashboard de Homicidios en Siniestros Viales")

    # Mostrar KPIs
    st.header("KPIs")
    kpi1, kpi2, kpi3 = calcular_kpis(df_homicidios)
    st.write(f"KPI 1: Reducción del 10% en la tasa de homicidios en siniestros viales en los últimos seis meses: {kpi1:.2f}%")
    st.write(f"KPI 2: Reducción del 7% en la cantidad de accidentes mortales de motociclistas en el último año: {kpi2:.2f}%")
    st.write("KPI 3: Tasa de homicidios en siniestros viales por grupo de edad")
    st.bar_chart(kpi3)

    # Mostrar datos
    st.header("Datos de Homicidios")
    st.write(df_homicidios)

# Ejecutar la aplicación
if __name__ == "__main__":
    mostrar_dashboard()



# Dashboard:
# Crea un dashboard funcional y coherente con el storytelling.
# Incluye filtros interactivos para explorar detalladamente los datos.
# Diseña el dashboard de manera que facilite la interpretación de la información.
# Utiliza una presentación clara de los datos y elige gráficos adecuados según
# las variables a visualizar.

# KPIs:
# Grafica y mide los 2 KPIs propuestos:
# Reducción en un 10% de la tasa de homicidios en siniestros viales de
# los últimos seis meses, en CABA, en comparación con el semestre anterior.
# Reducción en un 7% de la cantidad de accidentes mortales de motociclistas
# en el último año, en CABA, respecto al año anterior.
# Propón, mide y grafica un tercer KPI relevante para la temática.
