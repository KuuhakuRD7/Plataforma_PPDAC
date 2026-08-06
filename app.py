import streamlit as st
import shutil

from pathlib import Path

from wiki_data.wikis_ui import exibir_wikis

from core.in_data.obtencao import DIRETORIOS, UPLOAD_DIR, OUTPUT_DIR

from core.in_data.obtencao_ui import exibir_carregamento
from core.in_data.obtencao_ui import exibir_criacao
from core.out_data.exportacao_ui import exibir_exportacao

from core.proc_data.exploracao_ui import exibir_exploracao
from core.proc_data.tratamento_ui import exibir_tratamento
from core.proc_data.visualizacao_ui import exibir_visualizacao
from core.proc_data.analise_ui import exibir_analise


def exibir_inicio():
    st.write("inicio")


def configurar_layout():
    st.set_page_config(page_title="Plataforma PPDAC", layout="wide")


def inicializar_estados():
    if "datasets" not in st.session_state:
        st.session_state["datasets"] = {}
    if "datasets-tratado" not in st.session_state:
        st.session_state["datasets-tratado"] = {}
    if "datasets-analisado" not in st.session_state:
        st.session_state["datasets-analisado"] = {}
    if "estrutura" not in st.session_state:
        st.session_state.estrutura = {}
    if "df_editor" not in st.session_state:
        st.session_state.df_editor = None


def resetar_diretorios():
    # Percorre todos os arquivos e pastas dentro do diretório

    diretorios = [UPLOAD_DIR, OUTPUT_DIR]
    for diretorio in diretorios:
        for item in diretorio.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)


def resetar_estados(sessio_id: str):
    st.session_state["datasets"] = None
    st.session_state["datasets-tratado"] = None
    st.session_state["datasets-analisado"] = None
    st.session_state["resultado_atual"] = None
    st.session_state.estrutura = None
    st.session_state.df_editor = None

    resetar_diretorios()
    print(f"Encerrando: {sessio_id}")


@st.cache_resource(on_release=resetar_estados, scope="session")
def reset_session():
    return "ID_DA_SESS0"


def carregar_paginas():
    paginas = {
        "Início": (
            "titulo",
            "texto",
            exibir_inicio
        ),
        "Wikis": (
            "titulo",
            "texto",
            exibir_wikis
        ),
        "Criação": (
            "titulo",
            "texto",
            exibir_criacao
        ),
        "Carregamento": (
            "titulo",
            "texto",
            exibir_carregamento
        ),
        "Exploração": (
            "titulo",
            "texto",
            exibir_exploracao
        ),
        "Tratamento": (
            "titulo",
            "texto",
            exibir_tratamento
        ),
        "Análise": (
            "titulo",
            "texto",
            exibir_analise
        ),
        "Visualização": (
            "titulo",
            "texto",
            exibir_visualizacao
        ),
        "Exportação": (
            "titulo",
            "texto",
            exibir_exportacao
        ),
    }

    abas = st.tabs(list(paginas.keys()))

    for aba, nome_aba in zip(abas, paginas.keys()):
        titulo, texto, func_exibir = paginas[nome_aba]
        carregar_aba(nome_aba, aba, titulo, texto, func_exibir)


def carregar_aba(nome_aba: str, aba, titulo: str, texto: str, func_exibir):

    abas_base = ["Início", "Wikis", "Carregamento", "Criação"]

    with aba:
        st.title(titulo)
        st.write(texto)
        if nome_aba not in abas_base:
            nome_df, df = escolher_fonte_e_dataset(f"{nome_aba}_data_select")
            if df is not None:
                func_exibir(nome_df, df)
        else:
            func_exibir()


def listar_datasets():

    opcoes = {}

    repositorios = [
        "datasets",
        "datasets-tratado",
        "datasets-analisado"
    ]

    for repo in repositorios:

        for nome, df in st.session_state.get(repo, {}).items():
            opcoes[f"{repo} -> {nome}"] = {
                "nome": nome,
                "repo": repo,
                "df": df
            }

    return opcoes


def escolher_fonte_e_dataset(chave):

    datasets_disponiveis = listar_datasets()

    if not datasets_disponiveis:

        st.warning(
            "Nenhum dataset disponível."
        )
        return None, None

    escolha = st.selectbox(
        "Escolha um dataset",
        list(datasets_disponiveis.keys()),
        key=chave
    )

    info = datasets_disponiveis[escolha]

    return info["nome"], info["df"]


def executar():
    reset_session()
    configurar_layout()
    inicializar_estados()
    carregar_paginas()


executar()
