import pandas as pd
from pathlib import Path
import zipfile
import shutil


class Carregador():
    def descompactar(self, arquivo, caminho):
        nome_arquivo = arquivo.name if hasattr(
            arquivo, 'name') else Path(arquivo).name
        stem_arquivo = Path(nome_arquivo).stem

        pasta = caminho / arquivo.stem
        pasta.mkdir(exist_ok=True)

        with zipfile.ZipFile(arquivo) as z:
            z.extractall(pasta)

        return pasta

    def carregar_dataset(self, path, sep=None, encoding=None):
        if isinstance(path, (str, Path)):
            path = Path(path)
            ext = path.suffix.lower()
        else:
            # Caso receba diretamente o UploadedFile do Streamlit
            ext = Path(path.name).suffix.lower()
        if ext == ".csv":
            try:
                df = pd.read_csv(
                    path,
                    sep=sep,
                    encoding=encoding,
                    low_memory=False)
            except UnicodeDecodeError:
                df = pd.read_csv(
                    path, sep=sep, encoding=encoding, engine="python")
            except ValueError:
                df = pd.read_csv(
                    path, sep=sep, encoding=encoding, engine="python")

            return df
        if ext in [".xlsx", ".xls"]:
            return pd.read_excel(path)
        if ext == ".ods":
            return pd.read_excel(path, engine="odf")
        raise ValueError(f"Formato não suportado: {ext}")

    def carregar_conjunto(
            self,
            caminho,
            sep=None,
            encoding='utf-8'
    ):
        caminho = Path(caminho)
        extensoes = ['.csv', '.xls', '.xlsx', '.ods']

        # Cria uma lista única com todos os arquivos encontrados
        ARQUIVOS = [
            arquivo for ext in extensoes for arquivo in caminho.glob(f'*{ext}')]

        if not ARQUIVOS:
            raise FileNotFoundError(f"Nenhum dataset encontrado em {caminho}")

        lista_dfs = []

        for arquivo in ARQUIVOS:
            # print(f"Carregando: {arquivo.name}")

            df_temp = carregar_dataset(arquivo, sep=sep, encoding=encoding)
            lista_dfs.append(df_temp)

        df_final = pd.concat(lista_dfs, ignore_index=True)

        # print(f"\nTotal de arquivos carregados: {len(lista_dfs)}")
        # print(f"Total de linhas consolidadas: {len(df_final):,}")

        return df_final

    def carregar_composto(
        self,
        caminho,
        sep=None,
        encoding=None
    ):
        caminho = Path(caminho)
        datasets = {}

        extensoes = ['.csv', '.xls', '.xlsx', '.ods']

        # Cria uma lista única com todos os arquivos encontrados
        ARQUIVOS = [
            arquivo for ext in extensoes for arquivo in caminho.glob(f'*{ext}')]

        for arquivo in ARQUIVOS:

            nome = arquivo.stem

            try:
                df_temp = carregar_dataset(arquivo)

                datasets[nome] = df_temp

                print(f"[OK] {nome}")

            except Exception as e:
                print(f"[ERRO] {nome}: {e}")
        # display(datasets.keys())
        return datasets
