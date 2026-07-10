import streamlit as st
import shutil

from pathlib import Path

from wiki_data.wikis_ui import exibir_wikis

from core.in_data.obtencao import DIRETORIOS, UPLOAD_DIR, OUTPUT_DIR

from core.in_data.obtencao_ui import exibir_obtencao
from core.in_data.obtencao_ui import exibir_criacao
from core.out_data.exportacao_ui import exibir_exportacao

from core.proc_data.exploracao_ui import exibir_exploracao
from core.proc_data.tratamento_ui import exibir_tratamento
from core.proc_data.visualizacao_ui import exibir_visualizacao
from core.proc_data.analise_ui import exibir_analise


st.set_page_config(page_title="Plataforma PPDAC", layout="wide")

aba_Inicio, \
    aba_Criacao, \
    aba_Carregamento, \
    aba_Exploracao, \
    aba_Tratamento, \
    aba_Analise, \
    aba_Visualizacao, \
    aba_Exportacao = st.tabs([
        "Início",
        "Criacao",
        "Carregamento",
        "Exploração",
        "Tratamento",
        "Análise",
        "Visualização",
        "Exportação"
    ])


def reset_diretorios(session_id: str):
    # Percorre todos os arquivos e pastas dentro do diretório
    for item in UPLOAD_DIR.iterdir():
        if item.is_file():
            item.unlink()  # Apaga o arquivo
        elif item.is_dir():
            # Apaga subdiretório e seu conteúdo recursivamente
            shutil.rmtree(item)

    for item in OUTPUT_DIR.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)
    st.session_state["datasets"] = None
    st.session_state["datasets-tratado"] = None
    st.session_state["datasets-analisado"] = None
    st.session_state["resultado_atual"] = None
    st.session_state.estrutura = None
    st.session_state.df_editor = None
    print(f"Encerrando: {session_id}")


@st.cache_resource(on_release=reset_diretorios, scope="session")
def reset_session():
    return "ID_DA_SESS0"


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


reset_session()

with aba_Inicio:
    if "datasets" not in st.session_state:
        st.session_state["datasets"] = {}
    if "datasets-tratado" not in st.session_state:
        st.session_state["datasets-tratado"] = {}
    if "datasets-analisado" not in st.session_state:
        st.session_state["datasets-analisado"] = {}
    st.title("Plataforma de Educação em Ciência de Dados")
    st.write("Upload, tratamento, análise e exportação de datasets.")

    exibir_wikis()

with aba_Criacao:
    st.title("Criação")
    exibir_criacao()

with aba_Carregamento:
    st.title("Carregamento")
    arquivos = st.file_uploader(
        "Selecione arquivos",
        type=["csv", "xlsx", "ods", "zip"],
        accept_multiple_files=True
    )

    caminhos = []

    if arquivos:
        for arquivo in arquivos:
            pasta_destino = UPLOAD_DIR / Path(arquivo.name).stem
            pasta_destino.mkdir(parents=True, exist_ok=True)
            caminho_arquivo = pasta_destino / arquivo.name
            with open(caminho_arquivo, "wb") as f:
                f.write(arquivo.getbuffer())
            caminhos.append(caminho_arquivo)

        if caminhos:
            arquivo_escolhido = st.selectbox(
                "Arquivo",
                caminhos,
                format_func=lambda x: x.name)
            exibir_obtencao(arquivo_escolhido)


with aba_Exploracao:
    st.title("Exploração")
    nome, df = escolher_fonte_e_dataset(
        "explorar_select"
    )

    if df is not None:

        st.subheader(nome)

        exibir_exploracao(
            nome,
            df
        )

with aba_Tratamento:
    st.title("Tratamento")
    nome, df = escolher_fonte_e_dataset(
        "tratar_select"
    )

    if df is not None:

        st.subheader(nome)

        exibir_tratamento(
            nome,
            df
        )

with aba_Analise:
    st.title("Análise")
    nome, df = escolher_fonte_e_dataset(
        "analisar_select"
    )

    if df is not None:

        st.subheader(nome)

        exibir_analise(
            nome,
            df
        )

with aba_Visualizacao:
    st.title("Visualização")
    nome, df = escolher_fonte_e_dataset(
        "visualizar_select"
    )

    if df is not None:

        st.subheader(nome)

        exibir_visualizacao(
            nome,
            df
        )

with aba_Exportacao:
    st.title("Exportação")
    nome, df = escolher_fonte_e_dataset(
        "exportar_select"
    )

    if df is not None:

        st.subheader(nome)

        exibir_exportacao(
            nome,
            df
        )
