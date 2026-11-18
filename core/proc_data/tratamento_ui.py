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

        padronizar_colunas = False
        colunas_preencher = {}
        colunas_remover = []
        renomeacoes = {}
        invalidos = {}
        substituicoes = {}
        colunas_numericas = []
        colunas_datas = []
        limites = {}

        painel_controles, painel_preview = st.columns([1.15,1.45])

        with painel_controles:
            with st.container(border=True):
                tab_est, tab_val, tab_tip = st.tabs([
                    "Estrutura",
                    "Valores & Nulos",
                    "Tipos & Limites"
                ])


        with tab_est:
            padronizar_colunas = st.toggle("Limpar colunas", key=f"toggle_{nome}_lc")
            if padronizar_colunas:
                df_temp = Tratador.padronizar_colunas(df_temp)

            colunas_remover = st.multiselect(
                "Colunas para remover",
                df_temp.columns
            )

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

        with tab_val:
            colunas = st.multiselect(
                "Colunas com valores nulos",
                df_temp.columns
            )

            for coluna in colunas:

                tipo = st.radio(
                    "Tipo de Preenchimento",
                    ["Media", "Moda", "Mediana"],
                    # placeholder="Escolha ao menos um",
                    key=f"preenchimento_{nome}"

                )

                if tipo == "Media":
                    valor = df_temp[coluna].mean()
                elif tipo == "Moda":
                    valor = df_temp[coluna].mode()
                elif tipo == "Mediana":
                    valor = df_temp[coluna].median()
                colunas_preencher[coluna] = valor


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

        with tab_tip:
            colunas_numericas = st.multiselect(
                "Colunas Numéricas",
                df_temp.columns
            )


            colunas_datas = st.multiselect(
                "Colunas de Data",
                df_temp.columns
            )

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
            padronizar_colunas=padronizar_colunas,
            colunas_preencher=colunas_preencher,
            colunas_remover=colunas_remover,
            mapa_colunas=renomeacoes,
            invalidos=invalidos,
            substituicoes=substituicoes,
            colunas_numericas=colunas_numericas,
            colunas_datas=colunas_datas,
            limites=limites
        )

        with painel_preview:
            with st.container(border=True):

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
                    "Padronizar Colunas": padronizar_colunas,
                    "Preencher Colunas": colunas_preencher,
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
