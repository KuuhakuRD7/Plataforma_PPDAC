import streamlit as st
from core.proc_data.visualizacao import *
from wiki_data.wikis_ui import carregar_markdown


def exibir_visualizacao(nome, df):
    df_temp = df.copy()
    st.header("Visualizacao dos Dados")
    with st.expander("Dicas Sobre Gráficos"):
        dicas = carregar_markdown("./wiki_data/dicas_graficos.md")
        st.markdown(dicas)
    tipos_graficos = [
        "barras",
        "linhas",
        "area",
        "pizza",
        "radar",
        "cascata",
        "funil",
        "caixas",
        "dispersao",
        "bolhas",
        "mosaic",
        "sankey"
    ]

    grafico = st.selectbox(
        "Selecione a visualizacao",
        options=tipos_graficos,
        key=f"{nome}_grafico",
        index=None
    )

    if grafico == "barras":
        eixo_x = st.selectbox(
            "Selecione eixo x",
            df_temp.columns,
            key=f"eixo_x_{nome}")
        eixo_y = st.selectbox(
            "Selecione eixo y",
            df_temp.columns,
            key=f"eixo_y_{nome}")
        eixo_z = st.selectbox(
            "Selecione valoracao",
            df_temp.columns,
            index=None,
            key=f"eixo_z_{nome}")
        stacked = st.toggle("Stacked")
        top_n = st.number_input(
            "Top N",
            min_value=1,
            max_value=len(df_temp),
            value=min(10, len(df_temp)),
            step=1,
            key=f"{nome}_bar_top"
        )

        fig = grafico_barra(df_temp, eixo_x, eixo_y,
                            eixo_z, top_n, stacked)
        st.plotly_chart(fig)

    elif grafico == "linhas":

        eixo_x = st.selectbox(
            "Eixo X",
            df_temp.columns,
            key=f"{nome}_linha_x"
        )

        eixo_y = st.selectbox(
            "Eixo Y",
            df_temp.columns,
            key=f"{nome}_linha_y"
        )

        categoria = st.selectbox(
            "Categoria",
            [None] + list(df_temp.columns),
            index=None,
            key=f"{nome}_linha_cat"
        )

        fig = grafico_linha(
            df_temp,
            eixo_x,
            eixo_y,
            categoria
        )

        st.plotly_chart(fig)

    elif grafico == "area":

        eixo_x = st.selectbox(
            "Eixo X",
            df_temp.columns,
            key=f"{nome}_area_x"
        )

        eixo_y = st.selectbox(
            "Eixo Y",
            df_temp.columns,
            key=f"{nome}_area_y"
        )

        categoria = st.selectbox(
            "Categoria",
            [None] + list(df_temp.columns),
            index=None,
            key=f"{nome}_area_cat"
        )

        fig = grafico_area(
            df_temp,
            eixo_x,
            eixo_y,
            categoria
        )

        st.plotly_chart(fig)

    elif grafico == "pizza":

        categoria = st.selectbox(
            "Categoria",
            df_temp.columns,
            key=f"{nome}_pizza_cat"
        )

        numericas = (
            df_temp
            .select_dtypes(include="number")
            .columns
        )

        valor = st.selectbox(
            "Valor",
            numericas,
            key=f"{nome}_pizza_val"
        )

        top_n = st.number_input(
            "Top N",
            min_value=1,
            max_value=len(df_temp),
            value=min(10, len(df_temp)),
            step=1,
            key=f"{nome}_pizza_n"
        )

        fig = grafico_pizza(
            df_temp,
            categoria,
            valor,
            top_n
        )

        st.plotly_chart(fig)

    elif grafico == "dispersao":

        numericas = (
            df_temp
            .select_dtypes(include="number")
            .columns
        )

        x = st.selectbox(
            "X",
            numericas,
            key=f"{nome}_sc_x"
        )

        y = st.selectbox(
            "Y",
            numericas,
            key=f"{nome}_sc_y"
        )

        categoria = st.selectbox(
            "Categoria",
            [None] + list(df_temp.columns),
            index=None,
            key=f"{nome}_sc_cat"
        )

        fig = grafico_scatter(
            df_temp,
            x,
            y,
            categoria
        )

        st.plotly_chart(fig)

    elif grafico == "bolhas":

        numericas = (
            df_temp
            .select_dtypes(include="number")
            .columns
        )

        x = st.selectbox(
            "X",
            numericas,
            key=f"{nome}_bubble_x"
        )

        y = st.selectbox(
            "Y",
            numericas,
            key=f"{nome}_bubble_y"
        )

        tamanho = st.selectbox(
            "Tamanho",
            numericas,
            key=f"{nome}_bubble_size"
        )

        categoria = st.selectbox(
            "Categoria",
            [None] + list(df_temp.columns),
            index=None,
            key=f"{nome}_bubble_cat"
        )

        fig = grafico_bolhas(
            df_temp,
            x,
            y,
            tamanho,
            categoria
        )

        st.plotly_chart(fig)

    elif grafico == "caixas":

        eixo_x = st.selectbox(
            "Categoria",
            df_temp.columns,
            key=f"{nome}_box_x"
        )

        numericas = (
            df_temp
            .select_dtypes(include="number")
            .columns
        )

        eixo_y = st.selectbox(
            "Valor",
            numericas,
            key=f"{nome}_box_y"
        )

        fig = grafico_boxplot(
            df_temp,
            eixo_x,
            eixo_y
        )

        st.plotly_chart(fig)

    elif grafico == "cascata":

        categoria = st.selectbox(
            "Categoria",
            df_temp.columns,
            key=f"{nome}_water_cat"
        )

        numericas = (
            df_temp
            .select_dtypes(include="number")
            .columns
        )

        valor = st.selectbox(
            "Valor",
            numericas,
            key=f"{nome}_water_val"
        )

        top_n = st.number_input(
            "Top N",
            min_value=1,
            max_value=len(df_temp),
            value=min(10, len(df_temp)),
            step=1,
            key=f"{nome}_cascata_n"
        )

        fig = grafico_waterfall(
            df_temp,
            categoria,
            valor,
            top_n
        )

        st.plotly_chart(fig)

    elif grafico == "funil":

        eixo_x = st.selectbox(
            "Categoria",
            df_temp.columns,
            key=f"{nome}_funil_x"
        )

        numericas = (
            df_temp
            .select_dtypes(include="number")
            .columns
        )

        eixo_y = st.selectbox(
            "Valor",
            numericas,
            key=f"{nome}_funil_y"
        )

        top_n = st.number_input(
            "Top N",
            min_value=1,
            max_value=len(df_temp),
            value=min(10, len(df_temp)),
            step=1,
            key=f"{nome}_funil_n"
        )

        fig = grafico_funil(
            df_temp,
            eixo_x,
            eixo_y,
            top_n
        )

        st.plotly_chart(fig)

    elif grafico == "sankey":

        col1 = st.selectbox(
            "Origem",
            df_temp.columns,
            key=f"{nome}_sankey_1"
        )

        col2 = st.selectbox(
            "Destino",
            df_temp.columns,
            key=f"{nome}_sankey_2"
        )

        fig = grafico_sankey(
            df_temp[col1],
            df_temp[col2],
            col1,
            col2
        )

        st.plotly_chart(fig)

    elif grafico == "radar":

        categoria = st.selectbox(
            "Categoria",
            df_temp.columns,
            key=f"{nome}_radar_cat"
        )

        numericas = (
            df_temp
            .select_dtypes(include="number")
            .columns
        )

        valor = st.selectbox(
            "Valor",
            numericas,
            key=f"{nome}_radar_val"
        )

        grupo = st.selectbox(
            "Grupo",
            df_temp.columns,
            key=f"{nome}_radar_grp"
        )

        fig = grafico_radar(
            df_temp,
            categoria,
            valor,
            grupo
        )

        st.plotly_chart(fig)

    elif grafico == "mosaic":

        col1 = st.selectbox(
            "Coluna 1",
            df_temp.columns,
            key=f"{nome}_mos_1"
        )

        col2 = st.selectbox(
            "Coluna 2",
            df_temp.columns,
            key=f"{nome}_mos_2"
        )

        numericas = (
            df_temp
            .select_dtypes(include="number")
            .columns
        )

        valor = st.selectbox(
            "Valor",
            numericas,
            key=f"{nome}_mos_val"
        )

        top_n = st.number_input(
            "Top N",
            min_value=1,
            max_value=len(df_temp),
            value=min(10, len(df_temp)),
            step=1,
            key=f"{nome}_mosaico_n"
        )

        fig = grafico_mosaico(
            df_temp,
            col1,
            col2,
            valor,
            top_n
        )

        st.plotly_chart(fig)
