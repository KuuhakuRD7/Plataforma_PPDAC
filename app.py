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

        if "num_df_criados" not in st.session_state:
            st.session_state.num_df_criados = 0

    # ----------------------------------------------------------------

    def resetar_estados_manual(self):
        for cfg, vpadrao in self.grupos_data.items():
            st.session_state[cfg] = vpadrao

        st.session_state["resultado_atual"] = None
        st.session_state.estrutura = {}
        st.session_state.df_editor = None


class MainApp:

    def __init__(self):
        # Estruturar a Plataforma antes de tudo
        self.configurar_layout()

        # Atributos
        self.data_sessao = datetime.now()
        self.STM = GerenciadorEstados()

        # Metodos
        self.inicializar_modulos()

    # ----------------------------------------------------------------
    def configurar_layout(self):
        st.set_page_config(
            page_title="Laboratório de Dados | PPDAC",
            # page_icon="img/icon.png",
            layout="wide",
            initial_sidebar_state="expanded",
            # menu_items={"Page": "UrlTo",}
        )
        self._aplicar_estilo_css()

    def _aplicar_estilo_css(self):
        # Configuração por html e css
        st.markdown(
        """
        <!-- Importação de ícones W3 / Font Awesome -->
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

        <style>
            :root {
                /* Cores do Laboratório */
                --lab-blue: #2573DA;
                --lab-dark: #0C1523;
                --lab-light: #F5F9FD;

                --primary-hover: #125BB2;
                --success: #10B981;
                --warning: #F19E0B;
            }

            /* Tema claro do Streamlit */
            [data-theme="light"] {
                --bg-main: #F8FAFC;
                --surface-card: #FFFFFF;
                --border-color: #E2E8F0;
                --text-primary: #0F172A;
                --text-secondary: #475569;
            }

            /* Tema escuro do Streamlit */
            [data-theme="dark"] {
                --bg-main: #090D16;
                --surface-card: #0C1523;
                --border-color: #1E293B;
                --text-primary: #F8FAFC;
                --text-secondary: #94A3B8;
            }

            /* Aplicação Principal */
            .stApp {
                background-color: var(--bg-main);
                color: var(--text-primary);
            }

            /* Cabeçalho */
            [data-testid="stHeader"] {
                background-color: transparent !important;
            }

            /* Barra Lateral (Sidebar) */
            [data-testid="stSidebar"] {
                background-color: var(--surface-card) !important;
                border-right: 1px solid var(--border-color);
            }

            /* Forçar contraste nos textos da barra lateral */
            [data-testid="stSidebar"] *,
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] span {
                color: var(--text-primary) !important;
            }

            /* Containers / Cards */
            div[data-testid="stVerticalBlockBorderWrapper"] {
                background-color: var(--surface-card);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1rem;
            }

            /* Títulos */
            h1, h2, h3, h4, h5, h6 {
                color: var(--text-primary) !important;
                font-weight: 700 !important;
                letter-spacing: -0.02em;
            }

            /* Textos e Parágrafos */
            p, label, .stMarkdown {
                color: var(--text-secondary);
                line-height: 1.6;
            }

            /* Botões Primários */
            div.stButton > button[kind="primary"],
            div.stFormSubmitButton > button[kind="primary"] {
                background-color: var(--lab-blue) !important;
                border: 1px solid var(--lab-blue) !important;
                color: #FFFFFF !important;
                border-radius: 8px;
                font-weight: 600;
                transition: all 0.2s ease;
            }

            div.stButton > button[kind="primary"]:hover,
            div.stFormSubmitButton > button[kind="primary"]:hover {
                background-color: var(--primary-hover) !important;
                border-color: var(--primary-hover) !important;
                box-shadow: 0 4px 12px rgba(37, 115, 218, 0.25);
            }

            /* Botões Secundários */
            div.stButton > button:not([kind="primary"]),
            div.stFormSubmitButton > button:not([kind="primary"]) {
                background-color: var(--surface-card) !important;
                border: 1px solid var(--border-color) !important;
                color: var(--text-primary) !important;
                border-radius: 8px;
                font-weight: 500;
            }

            div.stButton > button:not([kind="primary"]):hover {
                border-color: var(--lab-blue) !important;
                color: var(--lab-blue) !important;
            }

            /* Butões Radio */
            [data-testid="stSidebar"] div[role="radiogroup"] label {
                position: relative;
                display: flex;
                align-items: center;
                gap: 0.65rem;

                padding: 0.65rem 0.85rem;
                margin: 0.25rem 0;

                border: 1px solid transparent;
                border-radius: 8px;

                cursor: pointer;
                transition:
                    background-color 0.2s ease,
                    border-color 0.2s ease,
                    color 0.2s ease;
            }

            [data-testid="stSidebar"]
            div[role="radiogroup"] label:has(input:checked) {
                background-color: color-mix(
                    in srgb,
                    var(--lab-blue) 10%,
                    var(--surface-card)
                ) !important;

                border: 1px solid var(--lab-blue) !important;
                box-shadow: 0 0 0 1px
                    color-mix(in srgb, var(--lab-blue) 12%, transparent);

                padding-left: 2.1rem;
            }

            /* Áreas de Upload */
            [data-testid="stFileUploader"] section {
                background-color: var(--surface-card) !important;
                border: 2px dashed var(--border-color) !important;
                border-radius: 10px;
            }

            /* Inputs, Seletores e Textareas */
            div[data-baseweb="input"] > div,
            div[data-baseweb="select"] > div,
            div[data-baseweb="textarea"] > div {
                background-color: var(--surface-card) !important;
                border-color: var(--border-color) !important;
                border-radius: 8px;
                color: var(--text-primary) !important;
            }

            /* Tabelas e Dataframes */
            div[data-testid="stDataFrame"],
            div[data-testid="stDataEditor"] {
                border: 1px solid var(--border-color);
                border-radius: 10px;
                background-color: var(--surface-card);
            }

            /* Utilitário para Ícones W3 / FontAwesome */
            .icon-lab {
                color: var(--lab-blue) !important;
                margin-right: 8px;
            }

            /* Menu e Rodapé nativos ocultos */
            #MainMenu, footer {
                /* visibility: hidden; */
            }
        </style>
        """, unsafe_allow_html=True
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
            "Início": {
                "grupo": "",
                "titulo": "",
                "descricao": (),
                "funcao": self.Tutor.exibir_inicio,
                "dataset": False,
            },
            "Wikis": {
                "grupo": "",
                "titulo": "",
                "descricao": (),
                "funcao": self.Tutor.exibir_wikis,
                "dataset": False,
            },
            "Planejamento": {
                "grupo": "",
                "titulo": "",
                "descricao": (),
                "funcao": self.Planejador.exibir_planejar,
                "dataset": False,
            },
            "Criação": {
                "grupo": "",
                "titulo": "",
                "descricao": (),
                "funcao": self.Criador.exibir_criacao,
                "dataset": False,
            },
            "Carregamento": {
                "grupo": "",
                "titulo": "",
                "descricao": (),
                "funcao": self.Carregador.exibir_carregamento,
                "dataset": False,
            },
            "Exploração": {
                "grupo": "",
                "titulo": "",
                "descricao": (),
                "funcao": self.Explorador.exibir_exploracao,
                "dataset": True,
            },
            "Tratamento": {
                "grupo": "",
                "titulo": "",
                "descricao": (),
                "funcao": self.Tratador.exibir_tratamento,
                "dataset": True,
            },
            "Análise": {
                "grupo": "",
                "titulo": "",
                "descricao": (),
                "funcao": self.Analisador.exibir_analise,
                "dataset": True,
            },
            "Visualização": {
                "grupo": "",
                "titulo": "",
                "descricao": (),
                "funcao": self.Visualizador.exibir_visualizacao,
                "dataset": True,
            },
            "Exportação": {
                "grupo": "",
                "titulo": "",
                "descricao": (),
                "funcao": self.Exportador.exibir_exportacao,
                "dataset": True,
            },
            "Conclusão": {
                "grupo": "",
                "titulo": "",
                "descricao": (),
                "funcao": self.Relatador.exibir_relato,
                "dataset": True,
            },
        }

        grupos = {
            "Sobre ciência de dados": [
                "Início", "Wikis"
            ],
            "Inserção de dados" : [
                "Criação", "Carregamento"
            ],
            "Trabalhar com dados": [
                "Exploração", "Tratamento", "Análise", "Visualização"
            ],
            "Investigação": [
                "Planejamento", "Conclusão", "Exportação"
            ],
        }

        st.sidebar.markdown(
            '<h3><i class="fa fa-flask icon-lab"></i> Laboratório de Dados</h3>',
            unsafe_allow_html=True
        )
        st.sidebar.caption("Aprender • Investigar • Descobrir")
        st.sidebar.divider()

        grupo = st.sidebar.radio(
            "Área de trabalho",
            list(grupos.keys()),
            key="grupo_navegacao",
        )

        pagina = st.sidebar.radio(
            "Escolhe uma atividade",
            grupos[grupo],
            key=f"pagina_{grupo}",
        )

        st.sidebar.divider()
        st.sidebar.caption("Método de investigação")
        st.sidebar.markdown(
            '<div style="font-size: 0.85rem; line-height: 1.8;">'
            '<i class="fa fa-search icon-lab"></i> Problema <br>'
            '<i class="fa fa-map-o icon-lab"></i> Plano <br>'
            '<i class="fa fa-database icon-lab"></i> Dados <br>'
            '<i class="fa fa-line-chart icon-lab"></i> Análise <br>'
            '<i class="fa fa-lightbulb-o icon-lab"></i> Conclusão'
            '</div>',
            unsafe_allow_html=True
        )

        config = paginas[pagina]

        st.title(config["titulo"])
        st.markdown(config["descricao"])
        st.divider()

        if config["dataset"]:
            nome_df, dataset = self.escolher_fonte_e_dataset(
                f"{pagina}_data_select"
            )

            if dataset is not None:
                # df = (
                #     dataset.df
                #     if hasattr(dataset, "df")
                #     else dataset
                # )
                config["funcao"](nome_df, dataset)
            else:
                st.info(
                    "Primeiro, cria ou importa um conjunto de dados "
                    "na área «Trabalhar com dados»."
                )
        else:
            config["funcao"]()

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
