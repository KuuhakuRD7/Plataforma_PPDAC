import pandas as pd
import numpy as np
import re


class Tratador:

    # ----------------------------------------------------------------
    @staticmethod
    def preencher_nulos(df, coluna):
        df[coluna] = (
            df[coluna]
            .fillna(
                df[coluna].median()
            )
        )
        return df

    # ----------------------------------------------------------------
    @staticmethod
    def remover_nulos(df):
        return df.dropna()

    # ----------------------------------------------------------------
    @staticmethod
    def limpar_colunas(df):
        df.columns = (
            df.columns
            .astype(str)
            .str.upper()
            .str.strip()
            .str.replace(" ", "_")
            .str.normalize("NFKD")
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
        )
        return df
    # ----------------------------------------------------------------

    @staticmethod
    def renomear_colunas(df, mapa):
        return df.rename(columns=mapa)

    # ----------------------------------------------------------------
    @staticmethod
    def substituir_valores(df, substituicoes):
        for coluna, valores in substituicoes.items():
            if coluna in df.columns:
                df.loc[
                    df[coluna].isin(valores[0]),
                    coluna
                ] = valores[1]
        return df

    # ----------------------------------------------------------------
    @staticmethod
    def substituir_invalidos(df, regras):

        for coluna, valores in regras.items():

            if coluna in df.columns:

                df.loc[
                    df[coluna].isin(valores),
                    coluna
                ] = np.nan

        return df

    # ----------------------------------------------------------------
    @staticmethod
    def aplicar_limites(df, regras):

        for col, (minimo, maximo) in regras.items():

            if col in df.columns:

                df.loc[
                    (df[col] < minimo)
                    |
                    (df[col] > maximo),
                    col
                ] = np.nan

        return df

    # ----------------------------------------------------------------
    @staticmethod
    def converter_numericos(df, colunas):

        for col in colunas:

            if col in df.columns:

                df[col] = (
                    df[col]
                    .astype(str)
                    .str.strip()
                    .str.replace(".", "", regex=False)
                    .str.replace(",", ".", regex=False)
                )
                df[col] = pd.to_numeric(
                    df[col],
                    errors="coerce"
                )

        return df

    # ----------------------------------------------------------------
    @staticmethod
    def converter_datas(df, colunas):

        for col in colunas:

            if col in df.columns:

                df[col] = pd.to_datetime(
                    df[col],
                    errors="coerce",
                    format="mixed"
                )

        return df

    # ----------------------------------------------------------------
    @staticmethod
    def preparar_dataset(
        df,
        limpar_cols=None,
        colunas_remover=None,
        mapa_colunas=None,
        invalidos=None,
        substituicoes=None,
        colunas_numericas=None,
        colunas_datas=None,
        limites=None,
        # exportar=False
    ):
        # alteracao encapsular o limpar_colunas
        if limpar_cols:
            df = Tratador.limpar_colunas(df)
        # alteracao verificaao de colunas
        if colunas_remover:
            df = df.drop(colunas_remover, axis=1)  # errors="ignore"
        if mapa_colunas:
            df = Tratador.renomear_colunas(df, mapa_colunas)
        if invalidos:
            df = Tratador.substituir_invalidos(df, invalidos)
        if substituicoes:
            df = Tratador.substituir_valores(df, substituicoes)
        if colunas_numericas:
            df = Tratador.converter_numericos(df, colunas_numericas)
        if colunas_datas:
            df = Tratador.converter_datas(df, colunas_datas)
        if limites:
            df = Tratador.aplicar_limites(df, limites)
        # if exportar:
        #     exportar_dataset(df)
        return df
