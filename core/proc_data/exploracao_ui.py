import streamlit as st
import pandas as pd
from core.proc_data.exploracao import Explorador


class ExploradorUI:
    # ----------------------------------------------------------------
    @staticmethod
    def exploracao_base(df):
        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.metric("Linhas",len(df))

        with col2:
            with st.container(border=True):
                st.metric("Colunas",len(df.columns))

        with col3:
            memoria = round(
                df.memory_usage(deep=True).sum() / 1024,2
            )
            with st.container(border=True):
                st.metric("Memória (KB)",memoria)

    # ----------------------------------------------------------------
    def exibir_exploracao(self, nome, dataset):
        df = dataset.df

        st.header("Exploração dos Dados")
        ExploradorUI.exploracao_base(df)

        painel_dados, painel_diagnostico = st.columns([1.3, 1])
        with painel_dados:
            with st.container(border=True):
                qtd_linhas, ord_linhas = st.columns(2)
                with qtd_linhas:
                    quantity = st.number_input(
                        label="Selecione quantidade de linhas",
                        min_value=1,       # Minimum integer boundary
                        max_value=100,     # Maximum integer boundary
                        value=min(10,len(df)),           # Default starting integer
                        step=1,            # Increments/decrements by 1
                        format="%d"        # Forces integer display formatting
                    )
                with ord_linhas:
                    ordem = st.toggle("Selecionar ultimas linhas")
                    ordenado = df.tail(
                        quantity) if ordem else df.head(quantity)
                st.dataframe(ordenado)

        with painel_diagnostico:
            with st.container(border=True):
                tab_estrutura, tab_resumo, tab_coluna = st.tabs([
                    "Tipos & Nulos",
                    "Resumo Estátistico",                    "Inspecionar Coluna",
                ])
        with tab_resumo:
            st.subheader(f"Descrição do Dataset:")
            st.dataframe(df.describe())


        with tab_estrutura:
            col_tipo, col_nulos = st.columns(2)

            with col_tipo:
                st.subheader(f"Tipos das Colunas:")
                st.dataframe(Explorador.mostrar_tipos(df))

            with col_nulos:
                st.subheader(f"Numero de Nulos:")
                st.dataframe(Explorador.analisar_nulos(df))

        with tab_coluna:
            coluna = st.radio(
                "Colunas a mostrar",
                df.columns
            )
            valores, unicos = Explorador.analisar_colunas(df, coluna)
            st.subheader(f"Valores da(s) coluna(s): {coluna}")
            st.dataframe(valores)
            # st.dataframe(unicos)
