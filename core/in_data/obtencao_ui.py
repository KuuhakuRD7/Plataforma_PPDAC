import streamlit as st
import pandas as pd

from core.in_data.obtencao import *
from core.out_data.exportacao import *
from core.proc_data.exploracao_ui import exploracao_base


def exibir_criacao():

    st.header("Criação de Dataset")

    if "estrutura" not in st.session_state:
        st.session_state.estrutura = {}

    if "df_editor" not in st.session_state:
        st.session_state.df_editor = None

    nome_dataset = st.text_input(
        "Nome do Dataset",
        placeholder="meu_dataset"
    )

    num_colunas = st.number_input(
        "Quantidade de colunas",
        min_value=1,
        max_value=20,
        value=3,
        step=1
    )

    num_linhas = st.number_input(
        "Quantidade de linhas",
        min_value=1,
        max_value=1000,
        value=10,
        step=1
    )

    st.divider()

    st.subheader("Estrutura do Dataset")

    tipos = [
        "string",
        "int",
        "float",
        "bool",
        "date",
        "datetime"
    ]

    with st.form("estrutura_dataset"):

        estrutura = {}

        for i in range(num_colunas):

            col1, col2 = st.columns([2, 1])

            with col1:
                nome_coluna = st.text_input(
                    f"Nome coluna {i+1}",
                    key=f"nome_coluna_{i}"
                )

            with col2:
                tipo = st.selectbox(
                    f"Tipo {i+1}",
                    tipos,
                    key=f"tipo_coluna_{i}"
                )

            if nome_coluna:
                estrutura[nome_coluna] = tipo

        criar_tabela = st.form_submit_button(
            "Criar Tabela"
        )

    if criar_tabela:

        st.session_state.estrutura = estrutura

        dados = {}

        for coluna, tipo in estrutura.items():

            if tipo == "string":
                dados[coluna] = [""] * num_linhas

            elif tipo == "int":
                dados[coluna] = [0] * num_linhas

            elif tipo == "float":
                dados[coluna] = [0.0] * num_linhas

            elif tipo == "bool":
                dados[coluna] = [False] * num_linhas

            elif tipo == "date":
                dados[coluna] = [pd.Timestamp.today().date()] * num_linhas

            elif tipo == "datetime":
                dados[coluna] = [pd.Timestamp.now()] * num_linhas

        st.session_state.df_editor = pd.DataFrame(dados)

    if st.session_state.df_editor is not None:

        st.divider()

        st.subheader("Preenchimento dos Dados")

        df_editado = st.data_editor(
            st.session_state.df_editor,
            num_rows="fixed",
            width='stretch',
            hide_index=True
        )

        if st.button("Gravar"):
            st.session_state.df_editor = df_editado
            st.session_state["datasets"][nome_dataset] = df_editado
            st.success(f"{nome_dataset} gravado com sucesso.")

        st.divider()

        st.subheader("Informações")
        exploracao_base(df_editado)


def exibir_obtencao(arquivo):
    datasets = {}
    temp = None
    col1, col2, col3 = st.columns(3)
    with col1:
        tipo = st.radio(
            "Tipo de carregamento",
            ["Simples", "Conjunto", "Composto"],
            # placeholder="Escolha ao menos um",
            captions=[
                "Arquivo csv simples",
                "Arquivo zip com csv's do mesmo dataset",
                "Arquivo zip com csv's de datasets diferentes"
            ],
            key=f"tipo_{arquivo.name}"

        )

    with col2:
        sep = st.radio(
            "Separador",
            [",", ";", "|"],
            captions=[
                "csv padrão",
                "csv's números com formato brasileiro",
                "csv's de formato misto"
            ],
            key=f"sep_{arquivo.name}",
            # placeholder="Selecione um ou deixe vazio se for zip..."
        )

    with col3:
        encoding = st.radio(
            "Codificação",
            ["utf-8", "latin1", "cp1252"],
            captions=[
                "Padrão Universal",
                "Padrão Latino",
                "Padrão Microsoft"
            ],
            key=f"encoding_{arquivo.name}"
            # placeholder="Selecione um ou deixe vazio se for zip..."
        )

    if tipo == "Simples":
        if arquivo.name.endswith(".zip"):
            caminho = descompactar(arquivo)
            temp = carregar_composto(caminho, sep=sep, encoding=encoding)
            datasets = temp
        else:
            temp = carregar_dataset(arquivo, sep=sep, encoding=encoding)
            datasets[arquivo.stem] = temp
    elif tipo == "Conjunto":
        if arquivo.name.endswith(".zip"):
            caminho = descompactar(arquivo)
            temp = carregar_composto(caminho, sep=sep, encoding=encoding)
            datasets = temp
        else:
            temp = carregar_conjunto(arquivo, sep=sep, encoding=encoding)
            datasets[arquivo.stem] = temp
    elif tipo == "Composto":
        if arquivo.name.endswith(".zip"):
            caminho = descompactar(arquivo)
            temp = carregar_composto(caminho, sep=sep, encoding=encoding)
            datasets = temp
        else:
            temp = carregar_composto(arquivo, sep=sep, encoding=encoding)
            datasets[arquivo.stem] = temp
    if st.button("Carregar Dados", key=f"loaddata_{arquivo.name}"):
        st.session_state["datasets"].update(datasets)
        st.success(f"Carregamento de {arquivo.name} concluido")
