from datetime import datetime
from pathlib import Path
import streamlit as st
import pandas as pd
import json

from core.model.dataset import Dataset, DatasetHistorico
from core.in_data.obtencao import Carregador


class CarregadorUI:
    """
        Classe responsavel pela interação da interface
        com o carregamento de datasets, por meio de:
        - Carregamento de arquivos
    """

    def __init__(self):
        self.ldr = Carregador()

    # ----------------------------------------------------------------

    def exibir_carregamento(self):
        sessao_ant = st.file_uploader(
            "Carregar Sessão Anterior", type=["json"])
        if sessao_ant is not None:
            dados_json = json.load(sessao_ant)
            dataset_rec = Dataset.from_dict(dados_json)
            st.session_state["datasets"][dataset_rec.nome] = dataset_rec
            st.success(f"Instância '{dataset_rec.nome}' carregada")

        st.divider()
        arquivos = st.file_uploader(
            "Selecione arquivos",
            type=["csv", "xlsx", "ods", "zip"],
            accept_multiple_files=True
        )

        # caminhos = []

        if arquivos:
            for arquivo in arquivos:
                # pasta_destino = UPLOAD_DIR / Path(arquivo.name).stem
                # pasta_destino.mkdir(parents=True, exist_ok=True)
                # caminho_arquivo = pasta_destino / arquivo.name
                # with open(caminho_arquivo, "wb") as f:
                #     f.write(arquivo.getbuffer())
                # caminhos.append(caminho_arquivo)

                # if caminhos:
                arquivo_escolhido = st.selectbox(
                    "Arquivo",
                    arquivos,  # caminhos
                    format_func=lambda x: x.name
                )
                self._carregar_arquivo(arquivo_escolhido)

    # ----------------------------------------------------------------
    def _salvar_dataset(
        self,
        nome: str,
        df: pd.DataFrame,
        caminho: Path,
        sep: str,
        encoding: str
    ) -> Dataset:

        dataset = Dataset(nome=nome, df=df, origem=str(caminho))

        dataset.metadata.caminho = str(caminho)
        dataset.metadata.encoding = encoding
        dataset.metadata.Separador = sep
        dataset.metadata.criado_em = datetime.now()
        dataset.metadata.atualizado_em = datetime.now()
        dataset.metadata.linhas = df.shape[0]
        dataset.metadata.colunas = df.shape[1]

        historico_carregamento = DatasetHistorico(
            modulo="CarregadorUI",
            operacao="Carregamento de Arquivo",
            parametros={
                "arquivo": caminho.name,
                "encoding": encoding,
                "separador": sep,
            },
        )
        dataset.historico.append(historico_carregamento)

        return dataset

    # ----------------------------------------------------------------
    def _carregar_arquivo(self, arquivo):
        datasets_brutos = {}

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
                caminho = self.ldr.descompactar(arquivo)
                datasets_brutos = self.ldr.carregar_composto(
                    caminho, sep=sep, encoding=encoding)
            else:
                temp = self.ldr.carregar_dataset(
                    arquivo, sep=sep, encoding=encoding)
                datasets_brutos[arquivo.name] = temp
        elif tipo == "Conjunto":
            if arquivo.name.endswith(".zip"):
                caminho = self.ldr.descompactar(arquivo)
                datasets_brutos = self.ldr.carregar_composto(
                    caminho, sep=sep, encoding=encoding)
            else:
                temp = self.ldr.carregar_conjunto(
                    arquivo, sep=sep, encoding=encoding)
                datasets_brutos[arquivo.name] = temp
        elif tipo == "Composto":
            if arquivo.name.endswith(".zip"):
                caminho = self.ldr.descompactar(arquivo)
                datasets_brutos = self.ldr.carregar_composto(
                    caminho, sep=sep, encoding=encoding)
            else:
                temp = self.ldr.carregar_composto(
                    arquivo, sep=sep, encoding=encoding)
                datasets_brutos[arquivo.name] = temp

        if st.button("Carregar Dados", key=f"loaddata_{arquivo.name}"):
            datasets_carregados = {}

            for nome_ds, df in datasets_brutos.items():
                if isinstance(df, pd.DataFrame):
                    dataset_obj = self._salvar_dataset(
                        nome=nome_ds,
                        df=df,
                        caminho=arquivo,
                        sep=sep,
                        encoding=encoding,
                    )
                    datasets_carregados[nome_ds] = dataset_obj

            st.session_state["datasets"].update(datasets_carregados)
            st.success(f"Carregamento de {arquivo.name} concluido")
