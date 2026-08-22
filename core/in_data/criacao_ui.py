from datetime import datetime

import streamlit as st
import pandas as pd

from core.model.dataset import Dataset, DatasetHistorico
from core.in_data.obtencao import *
from core.out_data.exportacao import *
from core.proc_data.exploracao_ui import ExploradorUI


class CriadorUI:
    """
        Classe responsavel pela interação da interface
        com o carregamento de datasets, por meio de:
        - Carregamento de arquivos
    """

    def __init__(self):
        self.nome_dataset = None
        self.num_colunas = None
        self.num_linhas = None
        self.estrutura = {}
        self.df_editado = None
        self.tipos = [
            "string",
            "int",
            "float",
            "bool",
            "date",
            "datetime"
        ]

    # ---------------------------------------------------------

    def _base_inicial(self):
        nome_dataset = st.text_input(
            "Nome do Dataset",
            placeholder="meu_dataset"
        )
        self.nome_dataset = nome_dataset

        num_colunas = st.number_input(
            "Quantidade de colunas",
            min_value=1,
            max_value=20,
            value=3,
            step=1
        )
        self.num_colunas = num_colunas

        num_linhas = st.number_input(
            "Quantidade de linhas",
            min_value=1,
            max_value=1000,
            value=10,
            step=1
        )
        self.num_linhas = num_linhas

    # ---------------------------------------------------------
    def _estruturar_dataset(self):
        with st.form("estrutura_dataset"):
            for i in range(self.num_colunas):

                col1, col2 = st.columns([2, 1])

                with col1:
                    nome_coluna = st.text_input(
                        f"Nome coluna {i+1}",
                        key=f"nome_coluna_{i}"
                    )

                with col2:
                    tipo = st.selectbox(
                        f"Tipo {i+1}",
                        self.tipos,
                        key=f"tipo_coluna_{i}"
                    )

                if nome_coluna:
                    self.estrutura[nome_coluna] = tipo

            return st.form_submit_button(
                "Criar Tabela"
            )

    # ---------------------------------------------------------

    def _tipos_colunas(self):
        st.session_state.estrutura = self.estrutura

        dados = {}

        for coluna, tipo in self.estrutura.items():

            if tipo == "string":
                dados[coluna] = [""] * self.num_linhas

            elif tipo == "int":
                dados[coluna] = [0] * self.num_linhas

            elif tipo == "float":
                dados[coluna] = [0.0] * self.num_linhas

            elif tipo == "bool":
                dados[coluna] = [False] * self.num_linhas

            elif tipo == "date":
                dados[coluna] = [pd.Timestamp.today().date()] * self.num_linhas

            elif tipo == "datetime":
                dados[coluna] = [pd.Timestamp.now()] * self.num_linhas

        st.session_state.df_editor = pd.DataFrame(dados)

    # ---------------------------------------------------------
    def _povoar_dataset(self):
        self.df_editado = st.data_editor(
            st.session_state.df_editor,
            num_rows="fixed",
            width='stretch',
            hide_index=True
        )

    # ----------------------------------------------------------------
    def exibir_criacao(self):

        st.subheader("Configurar Base")
        self._base_inicial()
        st.divider()

        st.subheader("Configurar Colunas")
        criar_tabela = self._estruturar_dataset()
        st.divider()

        if criar_tabela:
            self._tipos_colunas()

        if st.session_state.df_editor is not None:

            st.subheader("Preenchimento dos Registros")
            self._povoar_dataset()

            if st.button("Gravar"):
                novo_dataset = Dataset(
                    nome=self.nome_dataset,
                    dataframe=self.df_editado,
                    origem="CriadorUI"
                )

                novo_dataset.metadata.linhas = self.df_editado.shape[0]
                novo_dataset.metadata.colunas = self.df_editado.shape[1]
                novo_dataset.metadata.criado_em = datetime.now()

                historico_criacao = DatasetHistorico(
                    modulo="CriadorUI",
                    operacao="Criação manual de tabela",
                    parametros={"colunas": list(self.estrutura.keys())}
                )
                novo_dataset.historico.append(historico_criacao)

                st.session_state.df_editor = self.df_editado
                st.session_state["datasets"][self.nome_dataset] = novo_dataset

                st.success(f"{self.nome_dataset} gravado com sucesso.")

            st.divider()

            st.subheader("Informações")
            ExploradorUI.exploracao_base(self.df_editado)
