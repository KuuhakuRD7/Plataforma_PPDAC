import streamlit as st
import pandas as pd
from core.proc_data.exploracao import *


def exploracao_base(df):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Linhas",
            len(df)
        )

    with col2:
        st.metric(
            "Colunas",
            len(df.columns)
        )

    with col3:
        memoria = round(
            df.memory_usage(
                deep=True
            ).sum() / 1024,
            2
        )

        st.metric(
            "Memória (KB)",
            memoria
        )


def exibir_exploracao(nome, df):
    st.header("Exploração dos Dados")
    exploracao_base(df)

    with st.expander("Mostrar descrição", key=f"toggle_{nome}_md"):
        st.subheader(f"Descrição do Dataset:")
        st.dataframe(df.describe())

    with st.expander("Mostrar linhas", key=f"toggle_{nome}_ml"):
        st.subheader(f"Exemplos de Colunas:")
        quantity = st.number_input(
            label="Selecione quantidade de linhas",
            min_value=1,       # Minimum integer boundary
            max_value=100,     # Maximum integer boundary
            value=5,           # Default starting integer
            step=1,            # Increments/decrements by 1
            format="%d"        # Forces integer display formatting
        )
        ord = st.checkbox("Selecionar ultimas linhas")
        ordenado = df.tail(quantity) if ord else df.head(quantity)
        st.dataframe(ordenado)

    # with st.expander("Mostrar informação", key=f"toggle_{nome}_mi"):
    #     st.subheader(f"Informações do Dataset:")
    #     st.dataframe(df.info())

    with st.expander("Mostrar tipos", key=f"toggle_{nome}_mt"):
        st.subheader(f"Tipos das Colunas:")
        st.dataframe(mostrar_tipos(df))

    with st.expander("Mostrar nulos", key=f"toggle_{nome}_mn"):
        st.subheader(f"Numero de Nulos:")
        st.dataframe(analisar_nulos(df))

    with st.expander("Mostrar valores das colunas",
                     key=f"toggle_{nome}_mc"):
        coluna = st.radio(
            "Colunas a mostrar",
            df.columns
        )
        valores, unicos = analisar_colunas(df, coluna)
        st.subheader(f"Valores da(s) coluna(s): {coluna}")
        st.dataframe(valores)
        # st.dataframe(unicos)
