import streamlit as st
from pathlib import Path


class TutorUI:

    def __init__(self, caminho=Path("./wiki_data")):
        self.wikis = {}
        self.caminho = caminho

    # ----------------------------------------------------------------
    def exibir_inicio(self):
        # st.write("inicio")
        pass

    # ----------------------------------------------------------------
    @st.cache_data
    def carregar_markdown(_self, caminho):

        with open(caminho, "r", encoding="utf-8") as arquivo:
            return arquivo.read()

    # ----------------------------------------------------------------
    def carregar_wikis(self):

        self.wikis = {
            "Inicio":
            self.carregar_markdown(self.caminho / "inicio.md"),

            "Obtenção":
            self.carregar_markdown(self.caminho / "obtencao.md"),

            "Exploração":
            self.carregar_markdown(self.caminho / "exploracao.md"),

            "Tratamento":
            self.carregar_markdown(self.caminho / "tratamento.md"),

            "Análise":
            self.carregar_markdown(self.caminho / "analise.md"),

            "Visualização":
            self.carregar_markdown(self.caminho / "visualizacao.md"),

            "Exportação":
            self.carregar_markdown(self.caminho / "exportacao.md")
        }

    # ----------------------------------------------------------------
    def exibir_wikis(self):
        self.carregar_wikis()

        abas = st.tabs(list(self.wikis.keys()))

        for aba, (titulo, conteudo) in zip(
            abas,
            self.wikis.items()
        ):

            with aba:
                st.markdown(conteudo)
