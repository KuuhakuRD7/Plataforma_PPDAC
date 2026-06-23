import streamlit as st
from pathlib import Path


@st.cache_data
def carregar_markdown(caminho):

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def exibir_wikis():

    base = Path("./wiki_data")

    wikis = {
        "Inicio":
        carregar_markdown(base / "inicio.md"),

        "Obtenção":
        carregar_markdown(base / "obtencao.md"),

        "Exploração":
        carregar_markdown(base / "exploracao.md"),

        "Tratamento":
        carregar_markdown(base / "tratamento.md"),

        "Análise":
        carregar_markdown(base / "analise.md"),

        "Visualização":
        carregar_markdown(base / "visualizacao.md"),

        "Exportação":
        carregar_markdown(base / "exportacao.md")
    }

    st.header("Wiki do Sistema")

    abas = st.tabs(list(wikis.keys()))

    for aba, (titulo, conteudo) in zip(
        abas,
        wikis.items()
    ):

        with aba:

            st.markdown(conteudo)
