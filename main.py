import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Lectura de los datos
df_homicidios = pd.read_parquet("Datasets/df_homicidios.parquet")

def dashboard():
    # Definir la población total
    poblacion_total = 3120182

    st.markdown("<h1 style='text-align:center;'>Homicidios en accidentes viales en CABA</h1>", unsafe_allow_html=True)

    # Crear la grilla de 3 filas por 3 columnas
    col1, col2, col3 = st.columns([1, 1, 1])  # Primera fila
    col4, col5, col6 = st.columns([1, 1, 1])  # Segunda fila
    col7, col8, col9 = st.columns([1, 1, 1])  # Tercera fila

    # Filtros
    # implementar filtros, por ahora sólo usar la totalidad de los datos
    # hay que permitir seleccionar los datos a placer, y que los gráficos se actualicen a demanda
    # por ahora utilziar df_filtrado, pero sin filtrar
    df_filtrado = df_homicidios

    # Elementos para la primera fila
    with col1:
        #creación de variables
        moto_homicidio = 89
        moto_promedio = 91
        # Título
        st.markdown("<h4 style='text-align:center;'>Homicidios en Motocicletas</h4>", unsafe_allow_html=True)
        
        # Información
        st.markdown(f"<h5 style='text-align:center;'>Este Mes: {moto_homicidio}</h5>", unsafe_allow_html=True)
        st.markdown(f"<h5 style='text-align:center;'>Promedio: {moto_promedio}</h5>", unsafe_allow_html=True)


    with col2:
        #creación de variables
        total_homicidio = 180
        total_promedio = 182
        # Título
        st.markdown("<h4 style='text-align:center;'>Total Homicidios </h4>", unsafe_allow_html=True)
        
        # Información
        st.markdown(f"<h5 style='text-align:center;'>Este Mes: {total_homicidio}</h5>", unsafe_allow_html=True)
        st.markdown(f"<h5 style='text-align:center;'>Promedio: {total_promedio}</h5>", unsafe_allow_html=True)

    with col3:
        #creación de variables
        conductor_homicidio = 120
        conductor_promedio = 123
        # Título
        st.markdown("<h4 style='text-align:center;'>Homicidios Conductores</h4>", unsafe_allow_html=True)
        
        # Información
        st.markdown(f"<h5 style='text-align:center;'>Este Mes: {conductor_homicidio}</h5>", unsafe_allow_html=True)
        st.markdown(f"<h5 style='text-align:center;'>Promedio: {conductor_promedio}</h5>", unsafe_allow_html=True)

    # Elementos para la segunda fila
    with col4:
        st.markdown("<h4 style='text-align:center;'>Diferencia fallecimiento Moto Anual</h4>", unsafe_allow_html=True)

    with col5:
        st.markdown("<h4 style='text-align:center;'>Diferencia Tasa Homicidios últimos 6 meses</h4>", unsafe_allow_html=True)

    with col6:
        st.markdown("<h4 style='text-align:center;'>Diferencia fallecimiento de conductores anual</h4>", unsafe_allow_html=True)

    # Elementos para la tercera fila
    with col7:
        st.markdown("<h4 style='text-align:center;'>Distribución víctimas</h4>", unsafe_allow_html=True)
                
        victima_counts = df_filtrado['VICTIMA'].value_counts()
        top_4_victimas = victima_counts.nlargest(4)
        otros_victimas = victima_counts[~victima_counts.index.isin(top_4_victimas.index)].sum()
        labels = list(top_4_victimas.index) + ['Otros']
        sizes = list(top_4_victimas.values) + [otros_victimas]
        colors = sns.color_palette('YlOrBr', len(labels))
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='none')  # Fondo transparente
        wedges, _, autotexts = ax.pie(sizes, colors=colors, autopct='%1.1f%%', startangle=140)
        ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), frameon=False, labelcolor='white', fontsize=20)
        plt.setp(autotexts, size=20, weight="bold")
        ax.axis('equal')
        st.pyplot(fig)

    with col8:
        st.markdown("<h4 style='text-align:center;'>Relación Acusado-Víctima</h4>", unsafe_allow_html=True)

        top_acusado = df_filtrado['ACUSADO'].value_counts().nlargest(3).index.tolist()
        top_victima = df_filtrado['VICTIMA'].value_counts().nlargest(3).index.tolist()
        df_filtered = df_filtrado[df_filtrado['ACUSADO'].isin(top_acusado) & df_filtrado['VICTIMA'].isin(top_victima)]
        contingency_table = pd.crosstab(df_filtered['VICTIMA'], df_filtered['ACUSADO'])
        sns.set_palette('YlOrBr')
        plt.figure(figsize=(10, 8), facecolor='none')
        heatmap = sns.heatmap(contingency_table, annot=True, fmt='d', cmap='YlOrBr', linewidths=.5, annot_kws={"size": 20})
        plt.xticks(color='white', fontsize=15)
        plt.yticks(color='white', fontsize=15)
        plt.xlabel('ACUSADO', fontsize=20, color='white')
        plt.ylabel('VICTIMA', fontsize=20, color='white')
        heatmap.figure.axes[-1].tick_params(labelcolor='white')
        st.pyplot(plt)


    with col9:
        st.markdown("<h4 style='text-align:center;'>Distribución Rol víctimas</h4>", unsafe_allow_html=True)

        victima_counts = df_filtrado['ROL'].value_counts()
        labels = victima_counts.index.tolist()
        sizes = victima_counts.values.tolist()
        colors = sns.color_palette('YlOrBr', len(labels))
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='none')
        wedges, _, autotexts = ax.pie(sizes, colors=colors, autopct='%1.1f%%', startangle=140)
        ax.legend(wedges, labels, loc="upper left", bbox_to_anchor=(0.9, 0.5), frameon=False, labelcolor='white', fontsize=20)
        plt.setp(autotexts, size=20, weight="bold")  # Aumentar tamaño del texto autopct
        ax.axis('equal')
        st.pyplot(fig)

# Ejecutar la aplicación
if __name__ == "__main__":
    # Definir y aplicar el tema personalizado
    custom_theme = """
    [theme]
    base="dark"
    primaryColor="#ffff00"
    """
    st.markdown(f'<style>{custom_theme}</style>', unsafe_allow_html=True)

    dashboard()