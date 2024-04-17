import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Lectura de los datos
df_homicidios = pd.read_parquet("Datasets/df_homicidios.parquet")


def dashboard():

    # Definir la población total
    poblacion_total = 3120182
    df_filtrado = df_homicidios
    st.markdown(
        "<h1 style='text-align:center;'>Homicidios en accidentes viales en CABA</h1>",
        unsafe_allow_html=True,
    )

    # Crear la grilla de 3 filas por 3 columnas
    col1, col2, col3 = st.columns([1, 1, 1])  # Primera fila
    col4, col5, col6 = st.columns([1, 1, 1])  # Segunda fila
    col7, col8, col9 = st.columns([1, 1, 1])  # Tercera fila

    # Filtros

    df_filtrado["FECHA"] = pd.to_datetime(df_filtrado["FECHA"])
    df_filtrado["AÑO"] = df_filtrado["FECHA"].dt.year
    df_filtrado["MES"] = df_filtrado["FECHA"].dt.month

    anos_unicos = df_filtrado["AÑO"].unique()
    meses_unicos = df_filtrado["MES"].unique()

    # Obtener las edades únicas para el filtro
    edades_unicas = sorted(df_filtrado["EDAD"].unique())

    # Función para aplicar filtros dinámicos
    def aplicar_filtros(df, filtros):
        for variable, valor in filtros.items():
            if valor:
                df = df[df[variable].isin(valor)]
        return df

    # Widget para seleccionar los variables y valores de filtro
    st.sidebar.header("Filtros")
    ano_min_filtro = st.sidebar.selectbox(
        "Año Mínimo del Accidente", options=[None] + list(anos_unicos)
    )
    ano_max_filtro = st.sidebar.selectbox(
        "Año Máximo del Accidente", options=[None] + list(anos_unicos)
    )
    mes_min_filtro = st.sidebar.selectbox(
        "Mes Mínimo del Accidente", options=[None] + list(meses_unicos)
    )
    mes_max_filtro = st.sidebar.selectbox(
        "Mes Máximo del Accidente", options=[None] + list(meses_unicos)
    )
    edad_min_filtro = st.sidebar.selectbox(
        "Edad Mínima de la Víctima", options=[None] + edades_unicas
    )
    edad_max_filtro = st.sidebar.selectbox(
        "Edad Máxima de la Víctima", options=[None] + edades_unicas
    )

    # Eliminar valores inexistentes de los filtros
    acusados_disponibles = df_filtrado["ACUSADO"].unique()
    if "MOTO" not in acusados_disponibles:
        acusados_disponibles = [
            acusado for acusado in acusados_disponibles if acusado != "MOTO"
        ]
    acusado_filtro = st.sidebar.multiselect(
        "Acusado del Homicidio", options=acusados_disponibles
    )

    victimas_disponibles = df_filtrado["VICTIMA"].unique()
    victima_filtro = st.sidebar.multiselect("Víctima", options=victimas_disponibles)

    # Ajustar el filtro de edad para tener en cuenta valores "None"
    if edad_min_filtro is not None and edad_max_filtro is not None:
        filtro_edad = list(range(edad_min_filtro, edad_max_filtro + 1))
    elif edad_min_filtro is not None:
        filtro_edad = list(range(edad_min_filtro, max(edades_unicas) + 1))
    elif edad_max_filtro is not None:
        filtro_edad = list(range(min(edades_unicas), edad_max_filtro + 1))
    else:
        filtro_edad = None

    # Ajustar el filtro de año para tener en cuenta valores "None"
    if ano_min_filtro is not None and ano_max_filtro is not None:
        filtro_ano = list(range(ano_min_filtro, ano_max_filtro + 1))
    elif ano_min_filtro is not None:
        filtro_ano = list(range(ano_min_filtro, max(anos_unicos) + 1))
    elif ano_max_filtro is not None:
        filtro_ano = list(range(min(anos_unicos), ano_max_filtro + 1))
    else:
        filtro_ano = None

    # Ajustar el filtro de mes para tener en cuenta valores "None"
    if mes_min_filtro is not None and mes_max_filtro is not None:
        filtro_mes = list(range(mes_min_filtro, mes_max_filtro + 1))
    elif mes_min_filtro is not None:
        filtro_mes = list(range(mes_min_filtro, max(meses_unicos) + 1))
    elif mes_max_filtro is not None:
        filtro_mes = list(range(min(meses_unicos), mes_max_filtro + 1))
    else:
        filtro_mes = None

    # Aplicar filtros al DataFrame
    filtros = {
        "AÑO": filtro_ano,
        "MES": filtro_mes,
        "EDAD": filtro_edad,
        "ACUSADO": acusado_filtro,
        "VICTIMA": victima_filtro,
    }
    df_filtrado = aplicar_filtros(df_filtrado, filtros)

    # Mostrar los datos filtrados
    st.write(df_filtrado)

    with col1:
        # moto_homicidio
        df_filtrado["FECHA"] = pd.to_datetime(df_filtrado["FECHA"])
        fecha_mas_reciente = df_filtrado["FECHA"].max()
        fecha_hace_1_anio = fecha_mas_reciente - pd.DateOffset(years=1)
        df_ultimo_anio_moto = df_filtrado[
            (df_filtrado["FECHA"] >= fecha_hace_1_anio)
            & (df_filtrado["FECHA"] <= fecha_mas_reciente)
            & (df_filtrado["VICTIMA"] == "MOTO")
        ]
        moto_homicidio = df_ultimo_anio_moto["N_VICTIMAS"].sum()

        # moto_promedio
        df_filtrado["FECHA"] = pd.to_datetime(df_filtrado["FECHA"])
        years = df_filtrado["FECHA"].dt.year.unique()
        suma_victimas_por_anio = []
        for year in years:
            fecha_inicio = pd.Timestamp(year, 1, 1)
            fecha_fin = pd.Timestamp(year, 12, 31)
            df_ano_actual_moto = df_filtrado[
                (df_filtrado["FECHA"] >= fecha_inicio)
                & (df_filtrado["FECHA"] <= fecha_fin)
                & (df_filtrado["VICTIMA"] == "MOTO")
            ]
            suma_victimas_ano_actual = df_ano_actual_moto["N_VICTIMAS"].sum()
            suma_victimas_por_anio.append(suma_victimas_ano_actual)
        moto_promedio = (
            sum(suma_victimas_por_anio) / len(suma_victimas_por_anio)
        ).round(2)

        st.markdown(
            "<h4 style='text-align:center;'>Homicidios en Motocicletas</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h5 style='text-align:center;'>Último año: {moto_homicidio} / Promedio: {moto_promedio}</h5>",
            unsafe_allow_html=True,
        )

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
            df_periodo = df_filtrado[
                (df_filtrado["FECHA"] >= fecha_fin)
                & (df_filtrado["FECHA"] < fecha_inicio)
            ]
            homicidios_por_semestre.append(df_periodo["N_VICTIMAS"].sum())
            fecha_inicio = fecha_fin
        total_promedio = (
            sum(homicidios_por_semestre) / len(homicidios_por_semestre)
        ).round(2)

        st.markdown(
            "<h4 style='text-align:center;'>Total Homicidios</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h5 style='text-align:center;'>Este Semestre: {total_homicidio} /Promedio: {total_promedio}</h5>",
            unsafe_allow_html=True,
        )

    with col3:
        # conductor_homicidio
        fecha_mas_reciente = df_filtrado["FECHA"].max()
        fecha_hace_6_meses = fecha_mas_reciente - pd.DateOffset(months=6)
        df_ultimos_6_meses = df_filtrado[
            (df_filtrado["FECHA"] >= fecha_hace_6_meses)
            & (df_filtrado["ROL"] == "CONDUCTOR")
        ]
        conductor_homicidio = df_ultimos_6_meses["N_VICTIMAS"].sum()

        # conductor_promedio
        fecha_mas_reciente = df_filtrado["FECHA"].max()
        homicidios_por_semestre = []
        fecha_inicio = fecha_mas_reciente
        while fecha_inicio >= df_filtrado["FECHA"].min():
            fecha_fin = fecha_inicio - pd.DateOffset(months=6)
            df_periodo = df_filtrado[
                (df_filtrado["FECHA"] >= fecha_fin)
                & (df_filtrado["FECHA"] < fecha_inicio)
                & (df_filtrado["ROL"] == "CONDUCTOR")
            ]
            homicidios_por_semestre.append(df_periodo["N_VICTIMAS"].sum())
            fecha_inicio = fecha_fin
        conductor_promedio = (
            sum(homicidios_por_semestre) / len(homicidios_por_semestre)
        ).round(2)

        st.markdown(
            "<h4 style='text-align:center;'>Homicidios Conductor</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h5 style='text-align:center;'>Este semestre: {conductor_homicidio} / Promedio: {conductor_promedio}</h5>",
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            "<h4 style='text-align:center;'>Diferencia fallecimiento Moto Anual</h4>",
            unsafe_allow_html=True,
        )

        import plotly.graph_objects as go

        df_filtrado["FECHA"] = pd.to_datetime(df_filtrado["FECHA"])
        fecha_hace_un_anio = df_filtrado["FECHA"].max() - pd.DateOffset(years=1)
        fecha_hace_dos_anios = fecha_hace_un_anio - pd.DateOffset(years=1)
        df_ultimo_anio_moto = df_filtrado[
            (df_filtrado["FECHA"] >= fecha_hace_un_anio)
            & (df_filtrado["VICTIMA"] == "MOTO")
        ]
        df_anio_anterior_moto = df_filtrado[
            (df_filtrado["FECHA"] >= fecha_hace_dos_anios)
            & (df_filtrado["FECHA"] < fecha_hace_un_anio)
            & (df_filtrado["VICTIMA"] == "MOTO")
        ]
        total_victimas_ultimo_anio_moto = df_ultimo_anio_moto.shape[0]
        total_victimas_anio_anterior_moto = df_anio_anterior_moto.shape[0]

        objetivo = -7
        valor = (
            (total_victimas_ultimo_anio_moto - total_victimas_anio_anterior_moto)
            / total_victimas_anio_anterior_moto
            * 100
        )

        fig = go.Figure(
            go.Indicator(
                domain={"x": [0, 1], "y": [0, 1]},
                value=valor,
                mode="gauge+number+delta",
                title={"text": f"Objetivo: {objetivo}%"},
                delta={
                    "reference": objetivo,
                    "increasing": {"color": "red"},
                    "decreasing": {"color": "green"},
                },
                gauge={
                    "axis": {"range": [86, -100]},
                    "bar": {"color": "orange"},
                    "threshold": {
                        "line": {"color": "white", "width": 4},
                        "thickness": 0.75,
                        "value": -7,
                    },
                },
            )
        )

        fig.update_layout(width=250, height=250)
        fig.update_traces(number={"suffix": "%"})
        fig.update_traces(delta={"suffix": "%"})
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        st.markdown(
            "<h4 style='text-align:center;'>Diferencia Tasa Homicidios últimos 6 meses</h4>",
            unsafe_allow_html=True,
        )

        import plotly.graph_objects as go

        df_filtrado["FECHA"] = pd.to_datetime(df_filtrado["FECHA"])
        fecha_hace_un_semestre = df_filtrado["FECHA"].max() - pd.DateOffset(months=6)
        fecha_hace_un_anio = fecha_hace_un_semestre - pd.DateOffset(months=6)
        df_ultimo_semestre = df_filtrado[
            (df_filtrado["FECHA"] >= fecha_hace_un_semestre)
        ]
        df_semestre_anterior = df_filtrado[
            (df_filtrado["FECHA"] >= fecha_hace_un_anio)
            & (df_filtrado["FECHA"] < fecha_hace_un_semestre)
        ]
        total_homicidios_ultimo_semestre = df_ultimo_semestre.shape[0]
        total_homicidios_semestre_anterior = df_semestre_anterior.shape[0]

        poblacion_total = 3120182  # Supongamos que esta es la población total

        tasa_homicidios_ultimo_semestre = (
            total_homicidios_ultimo_semestre / poblacion_total * 100000
        )
        tasa_homicidios_semestre_anterior = (
            total_homicidios_semestre_anterior / poblacion_total * 100000
        )

        objetivo = -10
        valor = (
            (tasa_homicidios_ultimo_semestre - tasa_homicidios_semestre_anterior)
            / tasa_homicidios_semestre_anterior
        ) * 100

        # Crear la figura del gráfico de indicadores
        fig = go.Figure(
            go.Indicator(
                domain={"x": [0, 1], "y": [0, 1]},
                value=valor,
                mode="gauge+number+delta",
                title={"text": f"Objetivo: {objetivo}%"},
                delta={
                    "reference": objetivo,
                    "increasing": {"color": "red"},
                    "decreasing": {"color": "green"},
                },
                gauge={
                    "axis": {"range": [80, -100]},
                    "bar": {"color": "orange"},
                    "threshold": {
                        "line": {"color": "white", "width": 4},
                        "thickness": 0.75,
                        "value": -10,
                    },
                },
            )
        )

        # Actualizar la figura y mostrar el gráfico
        fig.update_layout(width=250, height=250)
        fig.update_traces(number={"suffix": "%"})
        fig.update_traces(delta={"suffix": "%"})
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        st.markdown(
            "<h4 style='text-align:center;'>Diferencia fallecimiento de conductores anual</h4>",
            unsafe_allow_html=True,
        )

        import plotly.graph_objects as go

        # Supongamos que df_filtrado es tu DataFrame

        # Convertir la columna FECHA a tipo datetime si aún no lo está
        df_filtrado["FECHA"] = pd.to_datetime(df_filtrado["FECHA"])

        # Obtener la fecha del año más reciente y del año anterior
        fecha_hace_un_anio = df_filtrado["FECHA"].max() - pd.DateOffset(years=1)
        fecha_hace_dos_anios = fecha_hace_un_anio - pd.DateOffset(years=1)

        # Filtrar los datos para el año más reciente donde el ROL es CONDUCTOR
        df_ultimo_anio_conductor = df_filtrado[
            (df_filtrado["FECHA"] >= fecha_hace_un_anio)
            & (df_filtrado["ROL"] == "CONDUCTOR")
        ]

        # Filtrar los datos para el año anterior donde el ROL es CONDUCTOR
        df_anio_anterior_conductor = df_filtrado[
            (df_filtrado["FECHA"] >= fecha_hace_dos_anios)
            & (df_filtrado["FECHA"] < fecha_hace_un_anio)
            & (df_filtrado["ROL"] == "CONDUCTOR")
        ]

        # Calcular el total de víctimas para el año más reciente y el año anterior
        total_victimas_ultimo_anio_conductor = df_ultimo_anio_conductor.shape[0]
        total_victimas_anio_anterior_conductor = df_anio_anterior_conductor.shape[0]

        # Calcular la diferencia porcentual entre el año más reciente y el año anterior
        diferencia_porcentual = (
            (
                total_victimas_ultimo_anio_conductor
                - total_victimas_anio_anterior_conductor
            )
            / total_victimas_anio_anterior_conductor
            * 100
        )
        valor = diferencia_porcentual
        objetivo = -25
        # Configurar el gráfico de indicadores
        fig = go.Figure(
            go.Indicator(
                domain={"x": [0, 1], "y": [0, 1]},
                value=valor,
                mode="gauge+number+delta",
                title={"text": f"Objetivo: {objetivo}%"},
                delta={
                    "reference": objetivo,
                    "increasing": {"color": "red"},
                    "decreasing": {"color": "green"},
                },
                gauge={
                    "axis": {"range": [50, -100]},
                    "bar": {"color": "orange"},
                    "threshold": {
                        "line": {"color": "white", "width": 4},
                        "thickness": 0.75,
                        "value": -25,
                    },
                },
            )
        )

        # Actualizar la figura y mostrar el gráfico
        fig.update_layout(width=250, height=250)
        fig.update_traces(number={"suffix": "%"})
        fig.update_traces(delta={"suffix": "%"})
        st.plotly_chart(fig, use_container_width=True)

    with col7:
        st.markdown(
            "<h4 style='text-align:center;'>Distribución víctimas</h4>",
            unsafe_allow_html=True,
        )

        victima_counts = df_filtrado["VICTIMA"].value_counts()
        top_4_victimas = victima_counts.nlargest(4)
        otros_victimas = victima_counts[
            ~victima_counts.index.isin(top_4_victimas.index)
        ].sum()
        labels = list(top_4_victimas.index) + ["Otros"]
        sizes = list(top_4_victimas.values) + [otros_victimas]
        colors = sns.color_palette("YlOrBr", len(labels))
        fig, ax = plt.subplots(figsize=(8, 6), facecolor="none")  # Fondo transparente
        wedges, _, autotexts = ax.pie(
            sizes, colors=colors, autopct="%1.1f%%", startangle=140
        )
        ax.legend(
            wedges,
            labels,
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            frameon=False,
            labelcolor="white",
            fontsize=20,
        )
        plt.setp(autotexts, size=20, weight="bold")
        ax.axis("equal")
        st.pyplot(fig)

    with col8:
        st.markdown(
            "<h4 style='text-align:center;'>Relación Acusado-Víctima</h4>",
            unsafe_allow_html=True,
        )

        top_acusado = df_filtrado["ACUSADO"].value_counts().nlargest(3).index.tolist()
        top_victima = df_filtrado["VICTIMA"].value_counts().nlargest(3).index.tolist()
        df_filtered = df_filtrado[
            df_filtrado["ACUSADO"].isin(top_acusado)
            & df_filtrado["VICTIMA"].isin(top_victima)
        ]
        contingency_table = pd.crosstab(df_filtered["VICTIMA"], df_filtered["ACUSADO"])
        sns.set_palette("YlOrBr")
        plt.figure(figsize=(10, 8), facecolor="none")
        heatmap = sns.heatmap(
            contingency_table,
            annot=True,
            fmt="d",
            cmap="YlOrBr",
            linewidths=0.5,
            annot_kws={"size": 20},
        )
        plt.xticks(color="white", fontsize=15)
        plt.yticks(color="white", fontsize=15)
        plt.xlabel("ACUSADO", fontsize=20, color="white")
        plt.ylabel("VICTIMA", fontsize=20, color="white")
        heatmap.figure.axes[-1].tick_params(labelcolor="white")
        st.pyplot(plt)

    with col9:
        st.markdown(
            "<h4 style='text-align:center;'>Distribución Rol víctimas</h4>",
            unsafe_allow_html=True,
        )

        victima_counts = df_filtrado["ROL"].value_counts()
        labels = victima_counts.index.tolist()
        sizes = victima_counts.values.tolist()
        colors = sns.color_palette("YlOrBr", len(labels))
        fig, ax = plt.subplots(figsize=(8, 6), facecolor="none")
        wedges, _, autotexts = ax.pie(
            sizes, colors=colors, autopct="%1.1f%%", startangle=140
        )
        ax.legend(
            wedges,
            labels,
            loc="center left",
            bbox_to_anchor=(0.9, 0.5),
            frameon=False,
            labelcolor="white",
            fontsize=20,
        )
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
