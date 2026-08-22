import streamlit as st
import pandas as pd


class Explorador:

    def __init__(self):
        self.info = None
        self.describe = None
        self.nullls = None
        self.types = None
        self.unicos = None

    # ----------------------------------------------------------------
    @staticmethod
    def mostrar_tipos(df):
        return pd.DataFrame({
            "coluna": df.columns,
            "tipo": df.dtypes.astype(str)
        })

    # ----------------------------------------------------------------
    @staticmethod
    def analisar_nulos(df):
        return (
            df
            .isnull()
            .sum()
            .sort_values(ascending=False)
        )

    # ----------------------------------------------------------------
    @staticmethod
    def resumo_estatistico(df, coluna):
        return {
            "media": df[coluna].mean(),
            "moda": df[coluna].mode(),
            "mediana": df[coluna].median(),
            "desvio": df[coluna].std(),
            "min": df[coluna].min(),
            "max": df[coluna].max()
        }

    # ----------------------------------------------------------------
    @staticmethod
    def analisar_colunas(df, coluna):
        valores = df[coluna].value_counts(
            ascending=True,
            dropna=False).reset_index()
        unicos = df[coluna].unique()
        return valores, unicos

    # ----------------------------------------------------------------
    @staticmethod
    def resumo_dataset(df):
        print("Linhas:", df.shape[0])
        print("Colunas:", df.shape[1])
        print("\n")
        display(df.head())
        print("\n")
        display(df.info())
        print("\n")
        display(df.describe())
        print("\n----TIPOS:")
        display(mostrar_tipos(df))
        print("\n----NULOS:")
        display(analisar_nulos(df))
