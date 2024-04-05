"""
Main.py - Dashboard Interactivo de Incidentes

Este archivo contiene una aplicación Streamlit que muestra un dashboard 
interactivo con datos de incidentes, incluyendo homicidios y lesiones.

Uso:
    Para ejecutar esta aplicación, utiliza el siguiente comando en la terminal:
        streamlit run main.py

Descripción:
    La aplicación muestra un dashboard interactivo con dos tipos de incidentes: 
    homicidios y lesiones. Permite al usuario seleccionar el tipo de incidente 
    a visualizar a través de una barra lateral y muestra los datos 
    correspondientes en función de la selección.

DataFrames:
    La aplicación utiliza dos DataFrames:
    - df_homicidios: DataFrame que contiene datos sobre homicidios.
    - df_lesiones: DataFrame que contiene datos sobre lesiones.

Requisitos:
    - Los datos deben estar disponibles en los DataFrames df_homicidios y 
    df_lesiones antes de ejecutar la aplicación.

"""

import streamlit as st
import pandas as pd

# lectura de los datos
df_homicidios = pd.read_parquet("Datasets/df_homicidios.parquet")
df_lesiones = pd.read_parquet("Datasets/df_lesiones.parquet")


def mostrar_dataframe(incidente):
    """_summary_

    Args:
        incidente (_type_): _description_
    """
    if incidente == "Homicidios":
        st.subheader("Datos de Homicidios")
        st.write(df_homicidios)
    else:
        st.subheader("Datos de Lesiones")
        st.write(df_lesiones)


def main():
    """_summary_"""
    # Aquí escribe tu aplicación Streamlit
    st.title("Dashboard Interactivo")

    # Sidebar para seleccionar el tipo de incidente a visualizar
    incidente_seleccionado = st.sidebar.selectbox(
        "Selecciona el tipo de incidente:", ["Homicidios", "Lesiones"]
    )

    # Mostrar el dataframe correspondiente al tipo de incidente seleccionado
    mostrar_dataframe(incidente_seleccionado)


if __name__ == "__main__":
    main()


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
