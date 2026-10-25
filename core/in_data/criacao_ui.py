from datetime import datetime
from faker import Faker
import random
import re
import json
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
        - Criação Manual
        - Criação Automatica por Parametros
        - Criação Automatica por Provedores
        - Exportação dos Parametros
        - Importação dos Parametros
    """

    def __init__(self):
        if "df_configuracoes" not in st.session_state:
            st.session_state["df_configuracoes"] = {}
        if "nome_dataset" not in st.session_state:
            st.session_state.nome_dataset = ""
        if "num_colunas" not in st.session_state:
            st.session_state.num_colunas = 3
        if "num_linhas" not in st.session_state:
            st.session_state.num_linhas = 10
        if "num_df_criados" not in st.session_state:
            st.session_state.num_df_criados = 0
        if "seed_faker" not in st.session_state:
            st.session_state.seed_faker = 32


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
    def _base_inicial(self):
        st.session_state.nome_dataset = st.text_input(
            "Nome do Dataset",
            # placeholder="meu_dataset",
            value=f"dataset_teste_{st.session_state.num_df_criados}",
        )

        st.session_state.num_colunas = st.number_input(
            "Quantidade de colunas",
            min_value=1,
            max_value=20,
            value=st.session_state.num_colunas,
            step=1
        )

        st.session_state.num_linhas = st.number_input(
            "Quantidade de linhas",
            min_value=1,
            max_value=1000,
            value=st.session_state.num_linhas,
            step=1
        )

    # ---------------------------------------------------------
    def _estruturar_dataset(self):
        with st.form("estrutura_dataset"):
            for i in range(st.session_state.num_colunas):

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
                    st.session_state.estrutura[nome_coluna] = tipo

            return st.form_submit_button(
                "Criar Tabela"
            )

    # ---------------------------------------------------------
    def _tipos_colunas(self):

        dados = {}

        for coluna, tipo in st.session_state.estrutura.items():

            if tipo == "string":
                dados[coluna] = [""] * st.session_state.num_linhas

            elif tipo == "int":
                dados[coluna] = [0] * st.session_state.num_linhas

            elif tipo == "float":
                dados[coluna] = [0.0] * st.session_state.num_linhas

            elif tipo == "bool":
                dados[coluna] = [False] * st.session_state.num_linhas

            elif tipo == "date":
                dados[coluna] = [pd.Timestamp.today().date()] * st.session_state.num_linhas

            elif tipo == "datetime":
                dados[coluna] = [pd.Timestamp.now()] * st.session_state.num_linhas

        st.session_state.df_editor = pd.DataFrame(dados)

    # ---------------------------------------------------------
    def _povoar_dataset(self):
        st.session_state.df_editor = st.data_editor(
            st.session_state.df_editor,
            num_rows="fixed",
            width='stretch',
            hide_index=True
        )

    # ---------------------------------------------------------
    def _configuracao_padrao(self, coluna, tipo):
        return {
            # Geral
            "coluna": coluna,
            "tipo": tipo,
            "tx_nulo": 0.2,
            "tx_sujeira": 0.3,

            "metodo_geracao": "Parâmetros",
            "provider": None,

            # Strings
            "qtd_chars": 30 if tipo == "string" else "",
            "padrao_string": "CODE-" if tipo == "string" else "",

            # Inteiros e Flutuantes
            "max": 100 if tipo in ("int", "float") else "",
            "min": 0 if tipo in ("int", "float") else "",
            "passo" : 1 if tipo in ("int", "float") else "",
            "casas_decimais": 2 if tipo == "float" else "",

            # Datas e Horarios
            "data_inicio": "2000-01-01",
            "data_fim": "2025-12-31",

            # Booleano
            "probabilidade_true" : 0.5 if tipo == "bool" else "",
        }

    # ---------------------------------------------------------
    def configurar_seed_faker(self, seed):
        self.faker.seed_instance(seed)
        st.session_state.seed_faker = seed

    # ---------------------------------------------------------
    def _aplicar_provedores(self, tipo):
        providers = {
            "string": {
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
                "texto": lambda: self.faker.text(max_nb_chars=300),
                "palavra": self.faker.word
            },
            "int" : {
                "idade": lambda: self.faker.random_int(min=0, max=120)
            },

            "float": {
                "salario": lambda:  self.faker.pyfloat(left_digits=5,right_digits=2,positive=True),
            },
            "bool": {
                "Booleano": self.faker.boolean,
            },
            "date": {
                "Data aleatória": self.faker.date_object,
            },
            "datetime": {
                "Data e hora": self.faker.date_time,
            },
        }

        return providers.get(tipo, {})

    # ---------------------------------------------------------
    def _configurar_parametros(self):
        st.subheader("Configurações do Faker")

        configuracoes = st.session_state["df_configuracoes"]

        for coluna, tipo in st.session_state.estrutura.items():
            if coluna not in configuracoes:
                configuracoes[coluna] = self._configuracao_padrao(
                    coluna, tipo
                )
            cfg = configuracoes[coluna]

            if cfg.get("tipo") != tipo:
                configuracoes[coluna] = self._configuracao_padrao(
                    coluna, tipo
                )
                cfg = configuracoes[coluna]

            with st.expander(f"{coluna} ({tipo})"):

                providers = self._aplicar_provedores(tipo)

                cfg["metodo_geracao"] = st.selectbox(
                    "Forma de geração",
                    options=["Parâmetros", "Provider"],
                    index=(
                        1 if cfg.get("metodo_geracao") == "Provider"
                        else 0
                    ),
                    key=f"metodo_geracao_{coluna}"
                )

                if cfg["metodo_geracao"] == "Provider":
                    opcoes = list(providers.keys())

                    if not opcoes:
                        st.warning(
                            f"Não existem providers disponíveis para o tipo {tipo}."
                        )
                    else:
                        provider_atual = cfg.get("provider")

                        if provider_atual not in opcoes:
                            provider_atual = opcoes[0]

                        cfg["provider"] = st.selectbox(
                            "Provider",
                            options=opcoes,
                            index=opcoes.index(provider_atual),
                            key=f"provider_{coluna}"
                        )

                c1, c2 = st.columns(2)
                with c1:
                    cfg["tx_nulo"] = st.slider(
                        "Probabilidade de Valores Nulos",
                        min_value=0.0,
                        max_value=1.0,
                        value=float(cfg.get("tx_nulo", 0.2)),
                        step=0.05,
                        key=f"faker_tx_nulo_{coluna}"
                    )
                with c2:
                    cfg["tx_sujeira"] = st.slider(
                        "Probabilidade de Valores Sujos",
                        min_value=0.0,
                        max_value=1.0,
                        value=float(cfg.get("tx_sujeira", 0.2)),
                        step=0.05,
                        key=f"faker_tx_sujeira_{coluna}"
                    )

                if tipo == "bool":
                    with c1:
                        cfg["probabilidade_true"] = st.slider(
                            "Probabilidade de True",
                            min_value=0.0,
                            max_value=1.0,
                            value=float(cfg.get("probabilidade_true", 0.5)),
                            step=0.05,
                            key=f"faker_prob_true_{coluna}"
                        )
                elif tipo in ("date", "datetime"):
                    with c1:
                        cfg["data_inicio"] = st.text_input(
                            "Data inicial (AAAA-MM-DD)",
                            value=str(cfg.get("data_inicio", "2000-01-01")),
                            key=f"faker_inicio_{coluna}"
                        )

                        cfg["data_fim"] = st.text_input(
                            "Data final (AAAA-MM-DD)",
                            value=str(cfg.get("data_fim", "2025-12-31")),
                            key=f"faker_fim_{coluna}"
                        )

                elif tipo in ("int", "float"):


                    with c1:
                        cfg["max"] = st.number_input(
                            "Máximo",
                            value=float(cfg.get("max", 100))
                                if tipo == "float"
                                else int(cfg.get("max", 100)),
                            step=1.0 if tipo == "float" else 1,
                            key=f"faker_max_{coluna}"
                        )

                        cfg["min"] = st.number_input(
                            "Mínimo",
                            value=float(cfg.get("min", 0))
                                if tipo == "float"
                                else int(cfg.get("min", 0)),
                            step=1.0 if tipo == "float" else 1,
                            key=f"faker_min_{coluna}"
                        )
                    with c2:
                        cfg["passo"] = st.number_input(
                            "Passo",
                            min_value=0.000001 if tipo == "float" else 1,
                            value=float(cfg.get("passo", 1))
                                if tipo == "float"
                                else max(1, int(cfg.get("passo", 1))),
                            key=f"faker_passo_{coluna}"
                        )

                        if tipo == "float":
                            cfg["casas_decimais"] = st.number_input(
                                "Casas decimais",
                                min_value=0,
                                max_value=10,
                                value=int(cfg.get("casas_decimais", 2)),
                                step=1,
                                key=f"faker_decimais_{coluna}"
                            )
        st.session_state["df_configuracoes"] = configuracoes

    # ---------------------------------------------------------
    def _aplicar_sujeira(self,tipo):
        pass

    # ---------------------------------------------------------
    def _gerar_dataset_faker(self):
        dados = {}
        estrutura = st.session_state.estrutura
        configuracoes = st.session_state["df_configuracoes"]
        num_linhas = int(st.session_state.num_linhas)

        for coluna, tipo in estrutura.items():

            cfg = configuracoes.get(
                coluna,
                self._configuracao_padrao(coluna, tipo)
            )

            qtd_nulos = round(num_linhas * cfg["tx_nulo"])
            qtd_sujos = round(num_linhas * cfg["tx_sujeira"])

            pos_nulos = set(random.sample(range(num_linhas), qtd_nulos))
            pos_sujos= set(random.sample(range(num_linhas), qtd_sujos))

            valores = []

            if cfg.get("metodo_geracao") == "Provider":
                providers = self._aplicar_provedores(tipo)
                provider_nome = cfg.get("provider")

                if provider_nome not in providers:
                    raise ValueError(
                        f"Provider inválido para a coluna '{coluna}'."
                    )

                gerar_valor = providers[provider_nome]

            else:
                gerar_valor = None

            for i in range(num_linhas):
                if i in pos_nulos:
                    valores.append(None)
                    continue
                if i in pos_sujos:
                    valores.append(self._aplicar_sujeira(tipo))
                    continue

                if gerar_valor is not None:
                    valores.append(gerar_valor())
                    continue

                if tipo == "int":
                    valores.append(
                        self.faker.pyint(
                            min_value=cfg["min"],
                            max_value=cfg["max"],
                            step=cfg["passo"],
                        )
                    )
                elif tipo == "float":
                    valores.append(
                        self.faker.pyfloat(
                            #left_digits=cfg["qtd_digitos"],
                            right_digits=cfg["casas_decimais"],
                            #positive=cfg["positivo"],
                            min_value=cfg["min"],
                            max_value=cfg["max"]
                        )
                    )
                elif tipo == "string":
                    valores.append(
                        self.faker.text(max_nb_chars=30)
                    )
                elif tipo == "bool":
                    valores.append(self.faker.pybool(cfg["probabilidade_true"]))
                elif tipo in ("date", "datetime"):
                    inicio = datetime.strptime(
                        cfg["data_inicio"], "%Y-%m-%d"
                    )
                    fim = datetime.strptime(
                        cfg["data_fim"], "%Y-%m-%d"
                    )

                    if fim < inicio:
                        raise ValueError(
                            f"Data final anterior à inicial: {coluna}."
                        )

                    if tipo == "date":
                        valores.append(
                            self.faker.date_between_dates(
                                date_start=inicio.date(),
                                date_end=fim.date()
                            )
                        )
                    else:
                        valores.append(
                            self.faker.date_time_between_dates(
                                datetime_start=inicio,
                                datetime_end=fim.replace(
                                    hour=23, minute=59, second=59
                                )
                            )
                        )

            dados[coluna] = valores
        st.session_state.df_editor = pd.DataFrame(dados)


    # ---------------------------------------------------------
    def _salvar_parametros(self):
        configuracoes = st.session_state["df_configuracoes"]

        conteudo = json.dumps(
            configuracoes,
            ensure_ascii=False,
            indent=4,
            default=str
        )


        st.download_button(
            "Salvar configurações JSON",
            data=conteudo,
            file_name=f"{st.session_state.nome_dataset}_configuracoes.json",
            mime="application/json"
        )

    # ---------------------------------------------------------
    def _carregar_parametros(self):
        arquivo_upload = st.file_uploader(
            "Carregar arquivo JSON de configurações",
            type=["json"],
            key="uploader_config_json"
        )

        if arquivo_upload is not None:
            if st.button("Aplicar Configurações", key="btn_aplicar_config"):
                try:
                    conteudo_bytes = arquivo_upload.read()
                    configuracoes_carregadas = json.loads(conteudo_bytes.decode("utf-8"))

                    if not isinstance(configuracoes_carregadas, dict):
                        st.error("O arquivo JSON não possui o formato esperado.")
                        return

                    # 1. Atualiza as estruturas principais no session_state
                    st.session_state["df_configuracoes"] = configuracoes_carregadas

                    nova_estrutura = {}
                    chaves_colunas = list(configuracoes_carregadas.keys())

                    for i, (coluna, cfg) in enumerate(configuracoes_carregadas.items()):
                        tipo_col = cfg.get("tipo", "string")
                        nova_estrutura[coluna] = tipo_col

                        # Pré-popula as chaves dos widgets antes de renderizá-los
                        st.session_state[f"nome_coluna_{i}"] = coluna
                        st.session_state[f"tipo_coluna_{i}"] = tipo_col

                        # Atualiza também as configurações específicas do Faker por coluna
                        st.session_state[f"metodo_geracao_{coluna}"] = cfg.get("metodo_geracao", "Parâmetros")
                        if cfg.get("provider"):
                            st.session_state[f"provider_{coluna}"] = cfg.get("provider")

                    st.session_state.estrutura = nova_estrutura
                    st.session_state.num_colunas = len(nova_estrutura)

                    # 2. Inicializa o DataFrame do editor com base na nova estrutura
                    self._tipos_colunas()

                    st.success("Configurações carregadas e aplicadas com sucesso!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Erro ao processar o arquivo JSON: {e}")

    # ----------------------------------------------------------------
    def exibir_criacao(self):

        with st.expander("Configurações Geração"):
            c1, c2 = st.columns(2)
            with c1:
                self._salvar_parametros()
                self._carregar_parametros()
            with c2:

                st.subheader("Configurar Seed")
                seed = st.number_input(
                    "Defina a seed usada pelo faker.",
                    value=st.session_state.seed_faker,
                    key=f"faker_seed_input"
                )

                self.configurar_seed_faker(seed)

        st.subheader("Configurar Base")
        self._base_inicial()
        st.divider()

        st.subheader("Configurar Colunas")
        criar_tabela = self._estruturar_dataset()

        if criar_tabela:
            self._tipos_colunas()

        st.divider()

        if st.session_state.df_editor is not None:

            self._configurar_parametros()
            operacao = "Manual"

            if st.button("Gerar Automaticamente"):
                operacao = "Automatica"
                try:
                    self._gerar_dataset_faker()
                    st.success("Dados gerados com sucesso.")
                except (ValueError, TypeError, KeyError) as erro:
                    st.error(f"Erro ao gerar os dados: {erro}")


            st.divider()


            self._povoar_dataset()

            if st.button("Gravar"):
                novo_dataset = Dataset(
                        nome=st.session_state.nome_dataset,
                        df=st.session_state.df_editor,
                        origem="CriadorUI"
                )

                novo_dataset.metadata.linhas = st.session_state.df_editor.shape[0]
                novo_dataset.metadata.colunas = st.session_state.df_editor.shape[1]
                novo_dataset.metadata.criado_em = datetime.now()

                historico_criacao = DatasetHistorico(
                        modulo="CriadorUI",
                        operacao=f"Criação {operacao} de tabela",
                        parametros={
                            "colunas": list(st.session_state.estrutura.keys()),
                            "configuracoes": st.session_state.df_configuracoes
                        }
                )
                novo_dataset.historico.append(historico_criacao)

                st.session_state["datasets"][st.session_state.nome_dataset] = novo_dataset

                st.success(f"{st.session_state.nome_dataset} gravado com sucesso.")

                st.divider()

                st.subheader("Informações")
                ExploradorUI.exploracao_base(st.session_state.df_editor)
