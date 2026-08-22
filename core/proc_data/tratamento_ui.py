import copy
from datetime import datetime
import re
import streamlit as st

from core.model.dataset import Dataset, DatasetHistorico
from core.proc_data.tratamento import Tratador


class TratadorUI:

    # ----------------------------------------------------------------
    def exibir_tratamento(self, nome, dataset):
        df = dataset.df

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
                df_temp = Tratador.limpar_colunas(df_temp)

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

        df_temp = Tratador.preparar_dataset(
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
            nome_tratado = f"{dataset.nome}_tratado"
            dataset_tratado = copy.deepcopy(dataset)
            dataset_tratado.nome = nome_tratado
            dataset_tratado.df = df_temp

            dataset_tratado.metadata.atualizado_em = datetime.now()
            dataset_tratado.metadata.linhas = df_temp.shape[0]
            dataset_tratado.metadata.colunas = df_temp.shape[1]

            tratamentos_executados = {
                "Padronizar Colunas": limparCols,
                "Remover Colunas": colunas_remover,
                "Renomear Colunas": renomeacoes,
                "Substituir Invalidos": invalidos,
                "Substituir valores": substituicoes,
                "Converter Numericos": colunas_numericas,
                "Converter Datas": colunas_datas,
                "Limita Valores": limites,
            }

            for operacao, parametros in tratamentos_executados.items():
                if parametros:
                    registro_historico = DatasetHistorico(
                        modulo="TratadorUI",
                        operacao=operacao,
                        parametros=parametros,
                    )
                    dataset_tratado.historico.append(registro_historico)

            dataset.variacoes.append(nome_tratado)

            st.session_state["datasets-tratado"][nome_tratado] = dataset_tratado

            st.success(f"Dataset '{nome_tratado}' gerado com sucesso!")
            st.dataframe(dataset_tratado.df.head())
