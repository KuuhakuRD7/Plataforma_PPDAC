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
        "barra",
        "linha",
        "area",
        "pizza",
        "radar",
        "cascata",
        "funil",
        "caixa",
        "dispersao",
        "bolha",
        "mosaic",
        "sankey"
    ]

    # graficos_comparar = ["barra", "radar", "pizza"]
    # graficos_mudancas = ["linha", "area", "cascata"]
    # graficos_organizar = ["mosaic", "funil"]
    # graficos_relacoes = ["dispersao", "bolha", "caixa", "sankey"]

    grafico = st.selectbox(
        "Selecione a visualizacao",
        options=tipos_graficos,
        key=f"{nome}_grafico",
        index=None
    )
    numericas = (
        df_temp
        .select_dtypes(include="number")
        .columns
    )
    # ---------------------------------
    if grafico in [
        "barra",
        "linha",
        "area",
        "mosaic",
        "sankey"
    ]:
        eixo_x = st.selectbox(
            "Selecione eixo x",
            df_temp.columns,
            key=f"eixo_x_{nome}"
        )

        eixo_y = st.selectbox(
            "Selecione eixo y",
            df_temp.columns,
            key=f"eixo_y_{nome}"
        )

    if grafico in [
        "barra",
        "pizza",
        "cascata",
        "funil",
        "mosaic"
    ]:
        top_n = st.number_input(
            "Top N",
            min_value=1,
            max_value=len(df_temp),
            value=min(10, len(df_temp)),
            step=1,
            key=f"{nome}_top_n"
        )

    if grafico in [
        "linha",
        "area",
        "dispersao",
        "bolha",
        "barra",
        "cascata",
        "radar"
    ]:
        eixo_z = st.selectbox(
            "Categoria",
            df_temp.columns,
            index=None,
            key=f"{nome}_cat_z"
        )

    if grafico in [
        "dispersao",
        "bolha"
    ]:
        eixo_x = st.selectbox(
            "X",
            numericas,
            key=f"{nome}_num_x"
        )

        eixo_y = st.selectbox(
            "Y",
            numericas,
            key=f"{nome}_num_y"
        )

    if grafico in [
        "pizza",
        "cascata",
        "bolha",
        "radar",
        "mosaic",
        "funil",
        "caixa"
    ]:
        valor = st.selectbox(
            "Valor",
            numericas,
            key=f"{nome}_valor"
        )

    if grafico in ["barra"]:
        stacked = st.toggle("Stacked")

    if grafico in ["radar"]:
        grupo = st.selectbox(
            "Grupo",
            df_temp.columns,
            key=f"{nome}_radar_grp"
        )
    # ---------------------------------

    fig = go.Figure()

    if grafico is None:
        return

    if grafico == "barra":
        fig = grafico_barra(
            df_temp,
            eixo_x,
            eixo_y,
            eixo_z,
            top_n,
            stacked
        )

    elif grafico == "linha":
        fig = grafico_linha(
            df_temp,
            eixo_x,
            eixo_y,
            eixo_z
        )

    elif grafico == "area":
        fig = grafico_area(
            df_temp,
            eixo_x,
            eixo_y,
            eixo_z
        )

    elif grafico == "pizza":
        fig = grafico_pizza(
            df_temp,
            eixo_z,
            valor,
            top_n
        )

    elif grafico == "dispersao":
        fig = grafico_dispersao(
            df_temp,
            eixo_x,
            eixo_y,
            eixo_z
        )

    elif grafico == "bolha":
        fig = grafico_bolhas(
            df_temp,
            eixo_x,
            eixo_y,
            valor,
            eixo_z
        )

    elif grafico == "caixa":
        fig = grafico_caixas(
            df_temp,
            eixo_z,
            valor
        )

    elif grafico == "cascata":
        fig = grafico_cascata(
            df_temp,
            eixo_z,
            valor,
            top_n
        )

    elif grafico == "funil":
        fig = grafico_funil(
            df_temp,
            eixo_z,
            valor,
            top_n
        )

    elif grafico == "sankey":
        fig = grafico_sankey(
            df_temp,
            eixo_x,
            eixo_y
        )

    elif grafico == "radar":
        fig = grafico_radar(
            df_temp,
            eixo_z,
            valor,
            grupo
        )

    elif grafico == "mosaic":
        fig = grafico_mosaico(
            df_temp,
            eixo_x,
            eixo_y,
            valor,
            top_n
        )

    st.plotly_chart(fig)
