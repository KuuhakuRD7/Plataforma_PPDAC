import streamlit as st
import re
from core.proc_data.tratamento import *


def exibir_tratamento(nome, df):
    df_temp = df.copy()
    st.header("Tratamento dos Dados")

    limparCols = False
    colunas_remover = []
    renomeacoes = {}
    invalidos = {}
    substituicoes = {}
    colunas_numericas = []
    colunas_datas = []
    limites = {}

    with st.expander("Padronizar Colunas", key=f"toggle_{nome}_lpc"):
        limparCols = st.toggle("Limpar colunas", key=f"toggle_{nome}_lc")
        if limparCols:
            df_temp = limpar_colunas(df_temp)

    with st.expander(
            "Remover Colunas", key=f"toggle_{nome}_sv"):
        colunas_remover = st.multiselect(
            "Colunas para remover",
            df_temp.columns
        )

    with st.expander("Renomear Colunas", key=f"toggle_{nome}_sr"):
        colunas_renomear = st.multiselect(
            "Colunas para renomear",
            df_temp.columns
        )

        for coluna in colunas_renomear:
            novo_nome = st.text_input(
                f"Novo nome para {coluna}",
                key=f"rename_{coluna}"
            )
            if novo_nome:
                renomeacoes[coluna] = novo_nome

    with st.expander("Substituir Invalidos", key=f"toggle_{nome}_si"):
        colunas_invalidas = st.multiselect(
            "Colunas com valores inválidos",
            df_temp.columns
        )

        for coluna in colunas_invalidas:

            valores = st.text_input(
                f"Inválidos para {coluna}",
                key=f"invalid_{coluna}"
            )

            if valores:

                invalidos[coluna] = [
                    v.strip()
                    for v in valores.split(",")
                ]

    with st.expander(
            "Substituir valores", key=f"toggle_{nome}_ss"):
        colunas_subs = st.multiselect(
            "Colunas para substituição",
            df_temp.columns
        )

        for coluna in colunas_subs:
            valores = st.text_input(
                f"Valores para substituir em {coluna}",
                key=f"sub_old_{coluna}"
            )

            novo = st.text_input(
                f"Novo valor para {coluna}",
                key=f"sub_new_{coluna}"
            )

            if valores and novo:

                substituicoes[coluna] = [
                    [v.strip() for v in valores.split(",")],
                    novo
                ]

    with st.expander("Converter Numericos", key=f"toggle_{nome}_sn"):
        colunas_numericas = st.multiselect(
            "Colunas Numéricas",
            df_temp.columns
        )

    with st.expander("Converter Datas", key=f"toggle_{nome}_sd"):
        colunas_datas = st.multiselect(
            "Colunas de Data",
            df_temp.columns
        )

    with st.expander("Limita Valores", key=f"toggle_{nome}_sl"):
        colunas_limite = st.multiselect(
            "Colunas com limites",
            df_temp.columns
        )

        for coluna in colunas_limite:

            minimo = st.number_input(
                f"Mínimo {coluna}",
                key=f"min_{coluna}"
            )

            maximo = st.number_input(
                f"Máximo {coluna}",
                key=f"max_{coluna}"
            )

            limites[coluna] = (
                minimo,
                maximo
            )

    df_temp = preparar_dataset(
        df=df.copy(),
        limpar_cols=limparCols,
        colunas_remover=colunas_remover,
        mapa_colunas=renomeacoes,
        invalidos=invalidos,
        substituicoes=substituicoes,
        colunas_numericas=colunas_numericas,
        colunas_datas=colunas_datas,
        limites=limites
    )

    col1, col2 = st.columns(2)
    with col1:
        st.write("Dataframe Original")
        st.dataframe(df.head())

    with col2:
        st.write("Dataframe em Tratamento")
        st.dataframe(df_temp.head())

    if st.button("Aplicar Tratamentos", key=f"btnt_{nome}"):
        df = df_temp
        st.session_state["datasets-tratado"][nome] = df_temp
        st.success("Tratamento aplicado.")
        st.dataframe(df.head())
