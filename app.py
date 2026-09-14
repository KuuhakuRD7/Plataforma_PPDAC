import streamlit as st
import shutil
from datetime import datetime
from pathlib import Path


from core.model.dataset import Dataset

from wiki_data.tutor_ui import TutorUI
from wiki_data.planejar_ui import PlanejadorUI
from wiki_data.relatar_ui import RelatadorUI

from core.in_data.obtencao_ui import CarregadorUI
from core.in_data.criacao_ui import CriadorUI
from core.out_data.exportacao_ui import ExportadorUI

from core.proc_data.exploracao_ui import ExploradorUI
from core.proc_data.tratamento_ui import TratadorUI
from core.proc_data.visualizacao_ui import VisualizadorUI
from core.proc_data.analise_ui import AnalisadorUI


class GerenciadorEstados():

    def __init__(self):
        self.grupos_data = {
            "datasets": {},
            "datasets-tratado": {},
            "datasets-analisado": {},
        }
        # self.diretorios = [
        #     UPLOAD_DIR,
        #     OUTPUT_DIR,
        #     INSTANSIAS
        # ]

        self._limpeza_inicial()
        self._inicializar_estados()

    # ----------------------------------------------------------------
    @st.cache_resource
    def _limpar_diretorios():
        # Percorre todos os arquivos e pastas dentro do diretório
        for diretorio in [UPLOAD_DIR, OUTPUT_DIR, INSTANSIAS]:
            if diretorio.exists():
                for item in diretorio.iterdir():
                    try:
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)
                    except Exception as e:
                        print(f"Erro ao remover {item}: {e}")
        print("DIRETORIOS_LIMPOS")

    # ----------------------------------------------------------------
    @staticmethod
    @st.cache_resource
    def _limpeza_inicial():
        # GerenciadorEstados._limpar_diretorios()
        return "RECURSO_LIMPEZA_ATIVO"

    # ----------------------------------------------------------------
    def _inicializar_estados(self):
        for cfg, vpadrao in self.grupos_data.items():
            if cfg not in st.session_state:
                st.session_state[cfg] = vpadrao

        if "estrutura" not in st.session_state:
            st.session_state.estrutura = {}

        if "df_editor" not in st.session_state:
            st.session_state.df_editor = None

    # ----------------------------------------------------------------

    def resetar_estados_manual(self):
        for cfg, vpadrao in self.grupos_data.items():
            st.session_state[cfg] = vpadrao

        st.session_state["resultado_atual"] = None
        st.session_state.estrutura = {}
        st.session_state.df_editor = None


class MainApp:

    def __init__(self):
        # Atributos
        self.data_sessao = datetime.now()
        self.STM = GerenciadorEstados()

        # Metodos
        self.configurar_layout()
        self.inicializar_modulos()

    # ----------------------------------------------------------------
    def configurar_layout(self):
        st.set_page_config(
            page_title="Plataforma PPDAC",
            # page_icon="img/icon.png",
            layout="wide",
            # initial_sidebar_state="auto",
            # menu_items={"Page": "UrlTo",}
        )

    # ----------------------------------------------------------------
    def inicializar_modulos(self):
        # Classes Educacionais
        self.Tutor = TutorUI()
        self.Planejador = PlanejadorUI()
        self.Relatador = RelatadorUI()

        # Classes Input e Output
        self.Carregador = CarregadorUI()
        self.Criador = CriadorUI()
        self.Exportador = ExportadorUI()

        # Classes Operações de Processamento
        self.Explorador = ExploradorUI()
        self.Tratador = TratadorUI()
        self.Analisador = AnalisadorUI()
        self.Visualizador = VisualizadorUI()

    # ----------------------------------------------------------------
    def carregar_paginas(self):
        paginas = {
            "Início": (
                "Visão Geral da Plataforma",
                "Bem-vindo ao ambiente de análise de dados. Esta ferramenta guia você de forma estruturada por todas as etapas da resolução de problemas orientados a dados.",
                self.Tutor.exibir_inicio
            ),  # ---------------------------
            "Wikis": (
                "Base de Conhecimento e PPDAC",
                "Explore os conceitos fundamentais da ciência de dados e entenda em detalhes o método PPDAC (Problema, Planejamento, Dados, Análise e Conclusão).",
                self.Tutor.exibir_wikis
            ),  # ---------------------------
            "Planejamento": (
                "Planejamento do Estudo",
                "Defina o problema de pesquisa, formula hipóteses, especifique a população-alvo e selecione os indicadores necessários para o estudo.",
                self.Planejador.exibir_planejar
            ),  # ---------------------------
            "Criação": (
                "Criação de Dataset",
                "Área responsável por criar datasets para experimentação, seja manualmente ou por meio de simulações e geração aleatória de dados.",
                self.Criador.exibir_criacao
            ),  # ---------------------------
            "Carregamento": (
                "Carregamento de Dados",
                "Importe arquivos de fontes externas (CSV, Excel, JSON, Banco de Dados) para iniciar a manipulação e preparação dos seus dados.",
                self.Carregador.exibir_carregamento
            ),  # ---------------------------
            "Exploração": (
                "Exploração Inicial de Dados",
                "Inspecione a estrutura básica do conjunto de dados: tipos de colunas, contagem de registros, valores ausentes e estatísticas sumárias preliminares.",
                self.Explorador.exibir_exploracao
            ),  # ---------------------------
            "Tratamento": (
                "Tratamento e Limpeza de Dados",
                "Corrija inconformidades nos dados realizando imputação de nulos, remoção de duplicatas, conversão de tipos e filtragem de outliers.",
                self.Tratador.exibir_tratamento
            ),  # ---------------------------
            "Análise": (
                "Análise Estatística e Modelagem",
                "Aplique técnicas estatísticas descritivas e inferenciais para responder às hipóteses e identificar padrões Relevantes nos dados.",
                self.Analisador.exibir_analise
            ),  # ---------------------------
            "Visualização": (
                "Visualização de Dados",
                "Gere gráficos iterativos e dashboards interativos para comunicar tendências, distribuições e relações entre as variáveis.",
                self.Visualizador.exibir_visualizacao
            ),  # ---------------------------
            "Exportação": (
                "Exportação de Resultados",
                "Exporte os dados tratados e os artefatos gerados em diferentes formatos (CSV, Excel, imagens ou JSON) para compartilhamento.",
                self.Exportador.exibir_exportacao
            ),  # ---------------------------
            "Conclusão": (
                "Conclusão e Relatório Final",
                "Sintetize os achados da análise, valide as hipóteses planejadas inicialmente e gere o relatório explicativo para tomada de decisão.",
                self.Relatador.exibir_relato
            ),  # ---------------------------
        }

        abas = st.tabs(list(paginas.keys()))

        for aba, nome_aba in zip(abas, paginas.keys()):
            titulo, texto, func_exibir = paginas[nome_aba]
            self.carregar_aba(nome_aba, aba, titulo, texto, func_exibir)

    # ----------------------------------------------------------------
    def carregar_aba(self, nome_aba: str, aba, titulo: str, texto: str, func_exibir):
        abas_base = ["Início", "Wikis", "Planejamento", "Carregamento", "Criação"]

        with aba:
            st.title(titulo)
            st.write(texto)
            if nome_aba not in abas_base:
                nome_df, df = self.escolher_fonte_e_dataset(
                    f"{nome_aba}_data_select")
                if df is not None:
                    func_exibir(nome_df, df)
            else:
                func_exibir()

    # ----------------------------------------------------------------
    def listar_datasets(self):

        opcoes = {}
        repositorios = list(self.STM.grupos_data.keys())

        for repo in repositorios:
            for nome, dataset in st.session_state.get(repo, {}).items():
                opcoes[f"{repo} -> {nome}"] = {
                    "nome": nome,
                    "repo": repo,
                    "dataset": dataset
                }
        return opcoes

    # ----------------------------------------------------------------
    def escolher_fonte_e_dataset(self, chave):

        datasets_disponiveis = self.listar_datasets()

        if not datasets_disponiveis:

            st.warning(
                "Nenhum dataset carregado."
            )
            return None, None

        escolha = st.selectbox(
            "Escolha um dataset",
            list(datasets_disponiveis.keys()),
            key=chave
        )

        info = datasets_disponiveis[escolha]

        return info["nome"], info["dataset"]

    # ----------------------------------------------------------------
    def executar(self):
        self.carregar_paginas()


# ----------------------------------------------------------------
if __name__ == '__main__':
    app = MainApp()
    app.executar()

# streamlit run app.py --server.maxUploadSize=200
