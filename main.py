import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Utilidades para evitar división por cero y listas vacías
def safe_div(num, den, default=np.nan):
    try:
        return num / den if den not in (0, 0.0, None) else default
    except Exception:
        return default

def safe_pct(num, den, default=np.nan):
    v = safe_div(num, den, default)
    return v * 100 if not (pd.isna(v)) else default

def ensure_data(df, min_rows=1, msg="No hay datos para los filtros seleccionados."):
    if df is None or getattr(df, "empty", False) or len(df) < min_rows:
        st.info(msg)
        return False
    return True

# Lectura de los datos
@st.cache_data
def carga_datos():
    return pd.read_parquet("Datasets/df_homicidios.parquet")

df_homicidios = carga_datos()


def dashboard():
    poblacion_total = 3120182
    
    df_filtrado = df_homicidios
    
    st.markdown("<h1 style='text-align:center;'>Homicidios en accidentes viales en CABA</h1>",unsafe_allow_html=True,)

    col1, col2, col3 = st.columns([1, 1, 1])
    col4, col5, col6 = st.columns([1, 1, 1])
    col7, col8, col9 = st.columns([1, 1, 1])

    # Filtros
    df_filtrado["FECHA"] = pd.to_datetime(df_filtrado["FECHA"])
    df_filtrado["AÑO"] = df_filtrado["FECHA"].dt.year
    df_filtrado["MES"] = df_filtrado["FECHA"].dt.month
    anos_unicos = df_filtrado["AÑO"].unique()
    meses_unicos = df_filtrado["MES"].unique()
    edades_unicas = sorted(df_filtrado["EDAD"].unique())

    @st.cache_data
    def aplicar_filtros(df, filtros):
        for variable, valor in filtros.items():
            if valor:
                df = df[df[variable].isin(valor)]
        return df

    st.sidebar.header("Filtros")
    ano_min_filtro = st.sidebar.selectbox("Año Mínimo del Accidente", options=[None] + list(anos_unicos))
    ano_max_filtro = st.sidebar.selectbox("Año Máximo del Accidente", options=[None] + list(anos_unicos))
    mes_min_filtro = st.sidebar.selectbox("Mes Mínimo del Accidente", options=[None] + list(meses_unicos))
    mes_max_filtro = st.sidebar.selectbox("Mes Máximo del Accidente", options=[None] + list(meses_unicos))
    edad_min_filtro = st.sidebar.selectbox("Edad Mínima de la Víctima", options=[None] + edades_unicas)
    edad_max_filtro = st.sidebar.selectbox("Edad Máxima de la Víctima", options=[None] + edades_unicas)
    acusados_disponibles = df_filtrado["ACUSADO"].unique()
    if "MOTO" not in acusados_disponibles: 
        acusados_disponibles = [acusado for acusado in acusados_disponibles if acusado != "MOTO"]
    acusado_filtro = st.sidebar.multiselect("Acusado del Homicidio", options=acusados_disponibles)
    victimas_disponibles = df_filtrado["VICTIMA"].unique()
    victima_filtro = st.sidebar.multiselect("Víctima", options=victimas_disponibles)
    if edad_min_filtro is not None and edad_max_filtro is not None: 
        filtro_edad = list(range(edad_min_filtro, edad_max_filtro + 1))
    elif edad_min_filtro is not None: 
        filtro_edad = list(range(edad_min_filtro, max(edades_unicas) + 1))
    elif edad_max_filtro is not None: 
        filtro_edad = list(range(min(edades_unicas), edad_max_filtro + 1))
    else: 
        filtro_edad = None
    if ano_min_filtro is not None and ano_max_filtro is not None: 
        filtro_ano = list(range(ano_min_filtro, ano_max_filtro + 1))
    elif ano_min_filtro is not None: 
        filtro_ano = list(range(ano_min_filtro, max(anos_unicos) + 1))
    elif ano_max_filtro is not None: 
        filtro_ano = list(range(min(anos_unicos), ano_max_filtro + 1))
    else: 
        filtro_ano = None
    if mes_min_filtro is not None and mes_max_filtro is not None: 
        filtro_mes = list(range(mes_min_filtro, mes_max_filtro + 1))
    elif mes_min_filtro is not None: 
        filtro_mes = list(range(mes_min_filtro, max(meses_unicos) + 1))
    elif mes_max_filtro is not None: 
        filtro_mes = list(range(min(meses_unicos), mes_max_filtro + 1))
    else: 
        filtro_mes = None
    filtros = {"AÑO": filtro_ano,"MES": filtro_mes,"EDAD": filtro_edad,"ACUSADO": acusado_filtro,"VICTIMA": victima_filtro,}
    with st.spinner('Cargando datos...'):
        df_filtrado = aplicar_filtros(df_homicidios, filtros)

        if not ensure_data(df_filtrado):
            st.stop()

        st.markdown("<h2 style='text-align:center;'>Gráficos derivados del EDA</h4>",unsafe_allow_html=True,)

        # Gráfico de caja y bigotes Hora del accidente
        st.markdown("<h4 style='text-align:center;'>Gráfico de caja y bigotes Hora del accidente</h4>", unsafe_allow_html=True)
        s_hora = df_filtrado["HORA"].dt.hour.dropna()
        if s_hora.empty:
            st.info("Sin datos de hora para graficar.")
        else:
            fig, ax = plt.subplots(figsize=(8, 3))
            boxplot = ax.boxplot(s_hora,vert=False,labels=[""],medianprops=dict(color="Black", linewidth=3),)
            ax.set_xlabel("Hora del día")
            ax.set_title("Hora de accidente con resultados fatales")
            ax.set_facecolor("lemonchiffon")
            ax.grid(True, color="lightgray", linewidth=0.5, zorder=0)
            quartiles = s_hora.quantile([0.25, 0.5, 0.75])
            for i, quartile in enumerate(quartiles): 
                ax.text(quartile, 1.08, f"{int(quartile)} Hrs", fontsize=7, color='black', ha='center', va='bottom')
            st.pyplot(fig)

        # Gráfico de caja y bigotes Edad del fallecido
        st.markdown("<h4 style='text-align:center;'>Gráfico de caja y bigotes Edad del fallecido</h4>", unsafe_allow_html=True)
        s_edad = df_filtrado["EDAD"].dropna()
        if s_edad.empty:
            st.info("Sin datos de edad para graficar.")
        else:
            fig, ax = plt.subplots(figsize=(8, 3))
            boxplot = ax.boxplot(s_edad,vert=False,labels=[""],medianprops=dict(color="black", linewidth=3),)
            ax.set_xlabel("Edad de la víctima")
            ax.set_title("Edad del fallecido en accidentes con resultados fatales")
            ax.set_facecolor("lemonchiffon")
            ax.grid(True, color="lightgray", linewidth=0.5, zorder=0)
            quartiles = s_edad.quantile([0.25, 0.5, 0.75])
            for i, quartile in enumerate(quartiles): 
                ax.text(quartile, 1.08, f"{int(quartile)} años", fontsize=7, color='black', ha='center', va='bottom')
            st.pyplot(fig)

        # Gráfico de barras Vehículos acusados de homicidios
        st.markdown("<h4 style='text-align:center;'>Gráfico de barras Vehículos acusados de homicidios</h4>", unsafe_allow_html=True)
        top_5_acusados = df_filtrado["ACUSADO"].value_counts(normalize=True).nlargest(5) * 100
        if top_5_acusados.empty:
            st.info("Sin datos para 'Vehículos acusados'.")
        else:
            fig, ax = plt.subplots(figsize=(10, 5))
            top_5_acusados.plot(kind="bar", color="none", edgecolor="black", hatch="//", ax=ax)
            ax.set_title("Vehículos acusados de Homicidios (Top 5)")
            ax.set_xlabel("Tipo de Vehículo")
            ax.set_xticklabels(top_5_acusados.index, rotation=0)
            ax.set_yticklabels([])
            ax.set_yticks([])
            st.set_option('deprecation.showPyplotGlobalUse', False)
            ax.set_facecolor("lemonchiffon")
            max_value = math.ceil(max(top_5_acusados) / 50) * 50
            for i in range(50, max_value, 50): 
                ax.axhline(y=i, color='lightgray', linewidth=0.5, zorder=0)
            for i, valor in enumerate(top_5_acusados): 
                ax.text(i, valor, f"{valor:.2f}%", ha="center", va="bottom")
            plt.tight_layout()
            st.pyplot(fig)

        # Gráfico de barras Transporte que utilizaba el fallecido
        st.markdown("<h4 style='text-align:center;'>Gráfico de barras Transporte que utilizaba el fallecido</h4>", unsafe_allow_html=True)
        top_5_victimas = df_filtrado["VICTIMA"].value_counts(normalize=True).nlargest(5) * 100
        if top_5_victimas.empty:
            st.info("Sin datos para 'Top 5 Víctimas'.")
        else:
            plt.figure(figsize=(10, 5))
            top_5_victimas.plot(kind="bar", color="none", edgecolor="black", hatch="//")
            plt.title("Top 5 Víctimas de accidentes viales fatales")
            plt.xlabel("Tipo de transporte")
            plt.xticks(rotation=0)
            plt.gca().set_facecolor("lemonchiffon")
            plt.gca().set_yticks([])
            for i, valor in enumerate(top_5_victimas):
                plt.text(i, valor, f"{valor:.2f}%", ha="center", va="bottom")
            plt.tight_layout()
            st.pyplot()

        # Histograma Rol de la víctima en relación al acusado
        st.markdown("<h4 style='text-align:center;'>Gráfico de barras Rol de la víctima en relación al acusado</h4>", unsafe_allow_html=True)
        frecuencia_acusado = df_filtrado["ROL"].value_counts(normalize=True) * 100
        if frecuencia_acusado.empty:
            st.info("Sin datos para 'Rol de la víctima'.")
        else:
            fig, ax = plt.subplots(figsize=(10, 5))
            frecuencia_acusado.plot(kind="bar", color="none", edgecolor="black", hatch="//", ax=ax)
            ax.set_title("Rol de la víctima en relación al acusado")
            ax.set_xlabel("Tipo de vehículo acusado")
            ax.set_yticklabels([])
            ax.set_yticks([])
            ax.set_xticklabels(frecuencia_acusado.index, rotation=0)
            ax.set_facecolor("lemonchiffon")
            for i in range(50, math.ceil(max(frecuencia_acusado)), 50): 
                ax.axhline(y=i, color='lightgray', linewidth=0.5, zorder=0)
            for i, valor in enumerate(frecuencia_acusado): 
                ax.text(i, valor, f"{valor:.2f}%", ha="center", va="bottom")
            st.pyplot(fig)

        # Histograma Sexo de la víctima en accidentes fatales
        st.markdown("<h4 style='text-align:center;'>Gráfico de barras Sexo de la víctima en accidentes fatales</h4>", unsafe_allow_html=True)
        frecuencia_victima = df_filtrado["SEXO"].value_counts(normalize=True) * 100
        if frecuencia_victima.empty:
            st.info("Sin datos para 'Sexo de la víctima'.")
        else:
            plt.figure(figsize=(10, 5))
            frecuencia_victima.plot(kind="bar", color="none", edgecolor="black", hatch="//")
            plt.title("Sexo de la víctima en accidentes fatales")
            plt.xlabel("Sexo de la víctima")
            plt.xticks(rotation=0)
            plt.gca().set_facecolor("lemonchiffon")
            plt.gca().set_yticks([])
            max_value = math.ceil(max(frecuencia_victima) / 100) * 100
            for i in range(100, max_value, 100): 
                plt.axhline(y=i, color='lightgray', linewidth=0.5, zorder=0)
            for i, valor in enumerate(frecuencia_victima): 
                plt.text(i, valor, f"{valor:.2f}%", ha="center", va="bottom")
            st.pyplot(plt)

        # Distribución de edades de las víctimas por sexo
        st.markdown("<h4 style='text-align:center;'>Distribución de edades de las víctimas por sexo</h4>", unsafe_allow_html=True)
        df_kde = df_filtrado[["EDAD", "SEXO"]].dropna()
        if df_kde.empty or df_kde["EDAD"].nunique() < 2:
            st.info("Sin datos suficientes para KDE por sexo.")
        else:
            plt.figure(figsize=(8, 4))
            sns.kdeplot(data=df_kde, x='EDAD', hue='SEXO', fill=True, common_norm=False, palette='gray_r')
            plt.xlabel('Edad de la víctima')
            plt.ylabel('Densidad')
            plt.title('Distribución de edades de las víctimas por sexo')
            plt.ylim(0, 0.03)  
            plt.gca().set_facecolor("lemonchiffon")
            for i in np.arange(0, 0.03, 0.005): 
                plt.axhline(y=i, color='lightgray', linewidth=0.5, zorder=0)
            st.pyplot(plt.gcf())

        # Frecuencias de combinaciones de Acusado y Víctima
        st.markdown("<h4 style='text-align:center;'>Frecuencias de combinaciones de Acusado y Víctima</h4>", unsafe_allow_html=True)
        top_acusados = df_filtrado['ACUSADO'].value_counts().nlargest(3).index
        top_victimas = df_filtrado['VICTIMA'].value_counts().nlargest(3).index
        df_filtered = df_filtrado[df_filtrado['ACUSADO'].isin(top_acusados) & df_filtrado['VICTIMA'].isin(top_victimas)]
        if df_filtered.empty:
            st.info("Sin datos para la relación Acusado–Víctima.")
        else:
            frecuencias = df_filtered.groupby(['ACUSADO', 'VICTIMA']).size().unstack(fill_value=0)
            plt.figure(figsize=(10, 6))
            plt.gca().set_facecolor("lemonchiffon")
            sns.countplot(data=df_filtered, x='ACUSADO', hue='VICTIMA', palette='gray_r')
            for p in plt.gca().patches:
                width = p.get_width()
                height = p.get_height()
                x, y = p.get_xy() 
                total_barras = len(df_filtered)
                porcentaje = safe_pct(height, total_barras)
                if not pd.isna(porcentaje) and porcentaje > 0:
                    plt.annotate(f'{porcentaje:.2f}%', (x + width/2, y + height*1.02), ha='center')
            plt.xlabel('Tipo de Acusado')
            plt.ylabel('')
            plt.title('Gráfico de relación entre Acusado y Víctima')
            plt.xticks(rotation=0)
            plt.legend(title='Tipo de Víctima')
            for i in range(0, 100, 20):
                plt.axhline(y=i, color='lightgray', linewidth=0.5, zorder=0)
            plt.gca().set_yticks([])
            plt.tight_layout()
            st.pyplot(plt)

        # Grafico de barras Relación entre el sexo de la víctima y su rol en el accidente
        st.markdown("<h4 style='text-align:center;'>Gráfico de barras Relación entre el sexo de la víctima y su rol en el accidente</h4>", unsafe_allow_html=True)
        if df_filtrado.empty:
            st.info("Sin datos para la relación Sexo–Rol.")
        else:
            plt.figure(figsize=(8, 6))
            plt.gca().set_facecolor("lemonchiffon")
            sns.countplot(x='ROL', hue='SEXO', data=df_filtrado, palette='gray_r')
            plt.title('Relación entre el sexo de la víctima y su rol en el accidente')
            plt.xlabel('Rol de la víctima')
            plt.ylabel('')
            plt.legend(title='Sexo')
            for p in plt.gca().patches:
                width = p.get_width()
                height = p.get_height()
                x, y = p.get_xy() 
                porcentaje = safe_pct(height, len(df_filtrado))
                if not pd.isna(porcentaje) and porcentaje > 0:
                    plt.annotate(f'{porcentaje:.2f}%', (x + width/2, y + height*1.02), ha='center')
            plt.gca().set_yticks([])
            plt.tight_layout()
            st.pyplot()

        # Mostrar los datos filtrados
        st.markdown("<h4 style='text-align:center;'>Tabla de datos</h4>", unsafe_allow_html=True)
        st.write(df_filtrado)

    with col1:
        # moto_homicidio
        df_filtrado["FECHA"] = pd.to_datetime(df_filtrado["FECHA"])
        fecha_mas_reciente = df_filtrado["FECHA"].max()
        fecha_hace_1_anio = fecha_mas_reciente - pd.DateOffset(years=1)
        df_ultimo_anio_moto = df_filtrado[(df_filtrado["FECHA"] >= fecha_hace_1_anio) & (df_filtrado["FECHA"] <= fecha_mas_reciente) & (df_filtrado["VICTIMA"] == "MOTO")]
        moto_homicidio = df_ultimo_anio_moto["N_VICTIMAS"].sum()
        # moto_promedio
        df_filtrado["FECHA"] = pd.to_datetime(df_filtrado["FECHA"])
        years = df_filtrado["FECHA"].dt.year.unique()
        suma_victimas_por_anio = []
        for year in years:
            fecha_inicio = pd.Timestamp(year, 1, 1)
            fecha_fin = pd.Timestamp(year, 12, 31)
            df_ano_actual_moto = df_filtrado[(df_filtrado["FECHA"] >= fecha_inicio) & (df_filtrado["FECHA"] <= fecha_fin) & (df_filtrado["VICTIMA"] == "MOTO")]
            suma_victimas_ano_actual = df_ano_actual_moto["N_VICTIMAS"].sum()
            suma_victimas_por_anio.append(suma_victimas_ano_actual)
        moto_promedio = safe_div(sum(suma_victimas_por_anio), len(suma_victimas_por_anio))
        moto_promedio = 0 if pd.isna(moto_promedio) else round(float(moto_promedio), 2)
        st.markdown("<h4 style='text-align:center;'>Homicidios en Motocicletas</h4>",unsafe_allow_html=True,)
        st.markdown(f"<h5 style='text-align:center;'>Último año: {moto_homicidio} / Promedio: {moto_promedio}</h5>",unsafe_allow_html=True,)

    with col2:
        # total_homicidio
        fecha_mas_reciente = df_filtrado["FECHA"].max()
        fecha_hace_6_meses = fecha_mas_reciente - pd.DateOffset(months=6)
        df_ultimos_6_meses = df_filtrado[df_filtrado["FECHA"] >= fecha_hace_6_meses]
        total_homicidio = df_ultimos_6_meses["N_VICTIMAS"].sum()
        # total_promedio
        fecha_mas_reciente = df_filtrado["FECHA"].max()
        homicidios_por_semestre = []
        fecha_inicio = fecha_mas_reciente
        while fecha_inicio >= df_filtrado["FECHA"].min():
            fecha_fin = fecha_inicio - pd.DateOffset(months=6)
            df_periodo = df_filtrado[(df_filtrado["FECHA"] >= fecha_fin) & (df_filtrado["FECHA"] < fecha_inicio)]
            homicidios_por_semestre.append(df_periodo["N_VICTIMAS"].sum())
            fecha_inicio = fecha_fin
        total_promedio = safe_div(sum(homicidios_por_semestre), len(homicidios_por_semestre))
        total_promedio = 0 if pd.isna(total_promedio) else round(float(total_promedio), 2)
        st.markdown("<h4 style='text-align:center;'>Total Homicidios</h4>",unsafe_allow_html=True,)
        st.markdown(f"<h5 style='text-align:center;'>Este Semestre: {total_homicidio} /Promedio: {total_promedio}</h5>",unsafe_allow_html=True,)

    with col3:
        # conductor_homicidio
        fecha_mas_reciente = df_filtrado["FECHA"].max()
        fecha_hace_6_meses = fecha_mas_reciente - pd.DateOffset(months=6)
        df_ultimos_6_meses = df_filtrado[(df_filtrado["FECHA"] >= fecha_hace_6_meses) & (df_filtrado["ROL"] == "CONDUCTOR")]
        conductor_homicidio = df_ultimos_6_meses["N_VICTIMAS"].sum()
        # conductor_promedio
        fecha_mas_reciente = df_filtrado["FECHA"].max()
        homicidios_por_semestre = []
        fecha_inicio = fecha_mas_reciente
        while fecha_inicio >= df_filtrado["FECHA"].min():
            fecha_fin = fecha_inicio - pd.DateOffset(months=6)
            df_periodo = df_filtrado[(df_filtrado["FECHA"] >= fecha_fin) & (df_filtrado["FECHA"] < fecha_inicio) & (df_filtrado["ROL"] == "CONDUCTOR")]
            homicidios_por_semestre.append(df_periodo["N_VICTIMAS"].sum())
            fecha_inicio = fecha_fin
        conductor_promedio = safe_div(sum(homicidios_por_semestre), len(homicidios_por_semestre))
        conductor_promedio = 0 if pd.isna(conductor_promedio) else round(float(conductor_promedio), 2)
        st.markdown("<h4 style='text-align:center;'>Homicidios Conductor</h4>",unsafe_allow_html=True,)
        st.markdown(f"<h5 style='text-align:center;'>Este semestre: {conductor_homicidio} / Promedio: {conductor_promedio}</h5>",unsafe_allow_html=True,)

    with col4:
        st.markdown("<h4 style='text-align:center;'>Diferencia fallecimiento Moto Anual</h4>",unsafe_allow_html=True,)
        import plotly.graph_objects as go
        df_filtrado["FECHA"] = pd.to_datetime(df_filtrado["FECHA"])
        fecha_hace_un_anio = df_filtrado["FECHA"].max() - pd.DateOffset(years=1)
        fecha_hace_dos_anios = fecha_hace_un_anio - pd.DateOffset(years=1)
        df_ultimo_anio_moto = df_filtrado[(df_filtrado["FECHA"] >= fecha_hace_un_anio) & (df_filtrado["VICTIMA"] == "MOTO")]
        df_anio_anterior_moto = df_filtrado[(df_filtrado["FECHA"] >= fecha_hace_dos_anios) & (df_filtrado["FECHA"] < fecha_hace_un_anio) & (df_filtrado["VICTIMA"] == "MOTO")]
        total_victimas_ultimo_anio_moto = df_ultimo_anio_moto.shape[0]
        total_victimas_anio_anterior_moto = df_anio_anterior_moto.shape[0]
        objetivo = -7
        valor = safe_pct(
            (total_victimas_ultimo_anio_moto - total_victimas_anio_anterior_moto),
            total_victimas_anio_anterior_moto
        )
        if pd.isna(valor):
            valor = 0  # o dejar NaN y mostrar "N/D" si se prefiere
        fig = go.Figure(go.Indicator(domain={"x": [0, 1], "y": [0, 1]},value=valor,mode="gauge+number+delta",title={"text": f"Objetivo: {objetivo}%"},delta={"reference": objetivo,"increasing": {"color": "red"},"decreasing": {"color": "green"},},gauge={"axis": {"range": [86, -100]},"bar": {"color": "orange"},"threshold": {"line": {"color": "white", "width": 4},"thickness": 0.75,"value": -7,},},))
        fig.update_layout(width=250, height=250)
        fig.update_traces(number={"suffix": "%"})
        fig.update_traces(delta={"suffix": "%"})
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        st.markdown("<h4 style='text-align:center;'>Diferencia Tasa Homicidios últimos 6 meses</h4>",unsafe_allow_html=True,)
        import plotly.graph_objects as go
        df_filtrado["FECHA"] = pd.to_datetime(df_filtrado["FECHA"])
        fecha_hace_un_semestre = df_filtrado["FECHA"].max() - pd.DateOffset(months=6)
        fecha_hace_un_anio = fecha_hace_un_semestre - pd.DateOffset(months=6)
        df_ultimo_semestre = df_filtrado[(df_filtrado["FECHA"] >= fecha_hace_un_semestre)]
        df_semestre_anterior = df_filtrado[(df_filtrado["FECHA"] >= fecha_hace_un_anio) & (df_filtrado["FECHA"] < fecha_hace_un_semestre)]
        total_homicidios_ultimo_semestre = df_ultimo_semestre.shape[0]
        total_homicidios_semestre_anterior = df_semestre_anterior.shape[0]
        tasa_homicidios_ultimo_semestre = (total_homicidios_ultimo_semestre / poblacion_total * 100000)
        tasa_homicidios_semestre_anterior = (total_homicidios_semestre_anterior / poblacion_total * 100000)
        objetivo = -10
        valor = safe_pct(
            (tasa_homicidios_ultimo_semestre - tasa_homicidios_semestre_anterior),
            tasa_homicidios_semestre_anterior
        )
        if pd.isna(valor):
            valor = 0
        fig = go.Figure(go.Indicator(domain={"x": [0, 1], "y": [0, 1]},value=valor,mode="gauge+number+delta",title={"text": f"Objetivo: {objetivo}%"},delta={"reference": objetivo,"increasing": {"color": "red"},"decreasing": {"color": "green"},},gauge={"axis": {"range": [80, -100]},"bar": {"color": "orange"},"threshold": {"line": {"color": "white", "width": 4},"thickness": 0.75,"value": -10,},},))
        fig.update_layout(width=250, height=250)
        fig.update_traces(number={"suffix": "%"})
        fig.update_traces(delta={"suffix": "%"})
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        st.markdown("<h4 style='text-align:center;'>Diferencia fallecimiento de conductores anual</h4>",unsafe_allow_html=True,)
        import plotly.graph_objects as go
        df_filtrado["FECHA"] = pd.to_datetime(df_filtrado["FECHA"])
        fecha_hace_un_anio = df_filtrado["FECHA"].max() - pd.DateOffset(years=1)
        fecha_hace_dos_anios = fecha_hace_un_anio - pd.DateOffset(years=1)
        df_ultimo_anio_conductor = df_filtrado[(df_filtrado["FECHA"] >= fecha_hace_un_anio) & (df_filtrado["ROL"] == "CONDUCTOR")]
        df_anio_anterior_conductor = df_filtrado[(df_filtrado["FECHA"] >= fecha_hace_dos_anios) & (df_filtrado["FECHA"] < fecha_hace_un_anio) & (df_filtrado["ROL"] == "CONDUCTOR")]
        total_victimas_ultimo_anio_conductor = df_ultimo_anio_conductor.shape[0]
        total_victimas_anio_anterior_conductor = df_anio_anterior_conductor.shape[0]
        valor = safe_pct(
            (total_victimas_ultimo_anio_conductor - total_victimas_anio_anterior_conductor),
            total_victimas_anio_anterior_conductor
        )
        if pd.isna(valor):
            valor = 0
        objetivo = -25
        fig = go.Figure(go.Indicator(domain={"x": [0, 1], "y": [0, 1]},value=valor,mode="gauge+number+delta",title={"text": f"Objetivo: {objetivo}%"},delta={"reference": objetivo,"increasing": {"color": "red"},"decreasing": {"color": "green"},},gauge={"axis": {"range": [50, -100]},"bar": {"color": "orange"},"threshold": {"line": {"color": "white", "width": 4},"thickness": 0.75,"value": -25,},},))
        fig.update_layout(width=250, height=250)
        fig.update_traces(number={"suffix": "%"})
        fig.update_traces(delta={"suffix": "%"})
        st.plotly_chart(fig, use_container_width=True)

    with col7:
        st.markdown("<h4 style='text-align:center;'>Distribución víctimas</h4>",unsafe_allow_html=True,)
        victima_counts = df_filtrado["VICTIMA"].value_counts()
        if victima_counts.empty or victima_counts.sum() == 0:
            st.info("Sin datos para 'Distribución víctimas'.")
        else:
            top_4_victimas = victima_counts.nlargest(4)
            otros_victimas = victima_counts[~victima_counts.index.isin(top_4_victimas.index)].sum()
            labels = list(top_4_victimas.index) + ["Otros"]
            sizes = list(top_4_victimas.values) + [otros_victimas]
            if sum(sizes) == 0:
                st.info("Sin datos suficientes para el gráfico de torta (víctimas).")
            else:
                colors = sns.color_palette("YlOrBr", len(labels))
                fig, ax = plt.subplots(figsize=(8, 6), facecolor="none")
                wedges, _, autotexts = ax.pie(sizes, colors=colors, autopct="%1.1f%%", startangle=140)
                ax.legend(wedges,labels,loc="center left",bbox_to_anchor=(1, 0, 0.5, 1),frameon=False,labelcolor="white",fontsize=20,)
                plt.setp(autotexts, size=20, weight="bold")
                ax.axis("equal")
                st.pyplot(fig)

    with col8:
        st.markdown("<h4 style='text-align:center;'>Relación Acusado-Víctima</h4>",unsafe_allow_html=True,)
        top_acusado = df_filtrado["ACUSADO"].value_counts().nlargest(3).index.tolist()
        top_victima = df_filtrado["VICTIMA"].value_counts().nlargest(3).index.tolist()
        df_filtered = df_filtrado[df_filtrado["ACUSADO"].isin(top_acusado) & df_filtrado["VICTIMA"].isin(top_victima)]
        contingency_table = pd.crosstab(df_filtered["VICTIMA"], df_filtered["ACUSADO"])
        if contingency_table.size == 0:
            st.info("Sin datos para el mapa de calor Acusado–Víctima.")
        else:
            sns.set_palette("YlOrBr")
            plt.figure(figsize=(10, 8), facecolor="none")
            heatmap = sns.heatmap(contingency_table,annot=True,fmt="d",cmap="YlOrBr",linewidths=0.5,annot_kws={"size": 20},)
            plt.xticks(color="white", fontsize=15)
            plt.yticks(color="white", fontsize=15)
            plt.xlabel("ACUSADO", fontsize=20, color="white")
            plt.ylabel("VICTIMA", fontsize=20, color="white")
            heatmap.figure.axes[-1].tick_params(labelcolor="white")
            st.pyplot(plt)

    with col9:
        st.markdown("<h4 style='text-align:center;'>Distribución Rol víctimas</h4>",unsafe_allow_html=True,)
        victima_counts = df_filtrado["ROL"].value_counts()
        if victima_counts.empty or victima_counts.sum() == 0:
            st.info("Sin datos para 'Distribución Rol víctimas'.")
        else:
            labels = victima_counts.index.tolist()
            sizes = victima_counts.values.tolist()
            if sum(sizes) == 0:
                st.info("Sin datos suficientes para el gráfico de torta (rol).")
            else:
                colors = sns.color_palette("YlOrBr", len(labels))
                fig, ax = plt.subplots(figsize=(8, 6), facecolor="none")
                wedges, _, autotexts = ax.pie(sizes, colors=colors, autopct="%1.1f%%", startangle=140)
                ax.legend(wedges,labels,loc="center left",bbox_to_anchor=(0.9, 0.5),frameon=False,labelcolor="white",fontsize=20,)
                plt.setp(autotexts, size=20, weight="bold")
                ax.axis("equal")
                st.pyplot(fig)


# Ejecutar la aplicación
if __name__ == "__main__":
    # Definir y aplicar el tema personalizado
    custom_theme = """
    [theme]
    base="dark"
    """
    st.markdown(f"<style>{custom_theme}</style>", unsafe_allow_html=True)
    dashboard()
