from datetime import datetime
from faker import Faker

import streamlit as st
import pandas as pd

from core.model.dataset import Dataset, DatasetHistorico
from core.in_data.obtencao import *
from core.out_data.exportacao import *
from core.proc_data.exploracao_ui import ExploradorUI


class CriadorUI:
    """
        Classe responsavel pela interação da interface
        com o desenvolvimento de datasets, por meio de:
        - Criação Manual ou Automática
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

        self.faker = Faker("pt_BR") # seed_instance(32)

    # ---------------------------------------------------------
    def _gerar_valores_faker(self, coluna, tipo):
        coluna_normalizada = coluna.lower().strip()

        string_faker = {
            "nome": self.faker.name,
            "email": self.faker.email,
            "telefone": self.faker.phone_number,
            "endereço": self.faker.address,
            "cidade": self.faker.city,
            "estado": self.faker.state,
            "companhia": self.faker.company,
            "emprego": self.faker.job,
            "cpf": self.faker.cpf,
            "cnpj": self.faker.cnpj,
            "texto": lambda: self.faker.text(max_nb_chars=30),
            "palavra": self.faker.word
        }
        int_faker = {
            "idade": lambda: self.faker.random_int(min=0, max=120)
        }

        float_faker = {
            "salario": lambda:  self.faker.pyfloat(left_digits=4,right_digits=2,positive=True),
        }

        if tipo == "string" and coluna_normalizada in string_faker:
            return string_faker[coluna_normalizada]()

        if tipo == "int" and coluna_normalizada in int_faker:
            return int_faker[coluna_normalizada]()

        if tipo == "float" and coluna_normalizada in float_faker:
            return float_faker[coluna_normalizada]()

        if tipo == "string":
            return self.faker.text(max_nb_chars=30)
        elif tipo == "int":
             return self.faker.random_int(min=0, max=120)
        elif tipo == "float":
            return self.faker.pyfloat(left_digits=4,right_digits=2,positive=True)
        elif tipo == "bool":
            return self.faker.boolean()

        elif tipo == "date":
            return self.faker.date_object()

        elif tipo == "datetime":
            return self.faker.date_time()

        return None

    # ---------------------------------------------------------
    def _gerar_dataset_faker(self):
        dados = {}
        estrutura = st.session_state.estrutura
        for coluna, tipo in estrutura.items():
            dados[coluna] = [
                self._gerar_valores_faker(coluna, tipo)
                for _ in range(self.num_linhas)
            ]
        st.session_state.df_editor = pd.DataFrame(dados)


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

        if criar_tabela:
            self._tipos_colunas()

        st.divider()

        if st.session_state.df_editor is not None:

            operacao = "Manual"
            self._povoar_dataset()


            if st.button("Gerar Automaticamente"):
                self._gerar_dataset_faker()
                operacao = "Automatica"


            st.divider()

            if st.button("Gravar"):
                novo_dataset = Dataset(
                        nome=self.nome_dataset,
                        df=self.df_editado,
                        origem="CriadorUI"
                )

                novo_dataset.metadata.linhas = self.df_editado.shape[0]
                novo_dataset.metadata.colunas = self.df_editado.shape[1]
                novo_dataset.metadata.criado_em = datetime.now()

                historico_criacao = DatasetHistorico(
                        modulo="CriadorUI",
                        operacao=f"Criação {operacao} de tabela",
                        parametros={"colunas": list(self.estrutura.keys())}
                )
                novo_dataset.historico.append(historico_criacao)

                st.session_state.df_editor = self.df_editado
                st.session_state["datasets"][self.nome_dataset] = novo_dataset

                st.success(f"{self.nome_dataset} gravado com sucesso.")

                st.divider()

                st.subheader("Informações")
                ExploradorUI.exploracao_base(self.df_editado)
