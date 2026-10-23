import streamlit as st
from pathlib import Path


class TutorUI:

    def __init__(self, caminho=Path("./wiki_data")):
        self.wikis = {}
        self.caminho = caminho

    # ----------------------------------------------------------------
    def exibir_inicio(self):
        st.markdown("## Bem-vindo ao laboratório de ciência de dados!")
        st.write(
            "Aqui você poderá investigar perguntas, experimentar "
            "com dados, descobrir padrões e brincar com dados. "
            " Não é preciso saber tudo para começar."
        )

        # Resumo do trabalho realizado
        datasets = st.session_state.get("datasets", {})
        total_datasets = len(datasets)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Conjuntos de dados atuais",
                total_datasets,
            )

        with col2:
            st.metric(
                "Etapa atual",
                "Exploração",
            )

        with col3:
            st.metric(
                "Objetivo",
                "Descobrir padrões",
            )

        st.divider()
        st.subheader("Por onde vamos começar?")

        st.divider()
        st.subheader("O percurso da investigação")

        etapas = [
            ("01", "Problema", "O que queremos descobrir?"),
            ("02", "Planeamento", "Como vamos investigar?"),
            ("03", "Dados", "Que informação precisamos?"),
            ("04", "Análise", "O que nos dizem os dados?"),
            ("05", "Conclusão", "A que respostas chegámos?"),
        ]

        for numero, titulo, descricao in etapas:
            with st.container(border=True):
                c1, c2 = st.columns([1, 5])

                with c1:
                    st.markdown(f"### {numero}")

                with c2:
                    st.markdown(f"**{titulo}**")
                    st.caption(descricao)

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
