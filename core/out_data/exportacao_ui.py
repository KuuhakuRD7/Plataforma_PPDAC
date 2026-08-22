import io
from datetime import datetime

import streamlit as st
import pandas as pd

from core.model.dataset import Dataset, DatasetHistorico
from core.model.dataset import Utilidades as utl

# from core.in_data.obtencao import UPLOAD_DIR, OUTPUT_DIR
from core.out_data.exportacao import Exportador


class ExportadorUI:

    def __init__(self):
        self.export = Exportador()

    # ----------------------------------------------------------------
    def registrar_operacao(self, dataset: Dataset, formato: str):
        hist = DatasetHistorico(
            modulo="ExportadorUI",
            operacao=f"Exportação de Dados ({formato.upper()})",
            parametros={
                "formato": formato,
                "data_exportacao": str(datetime.now())
            },
        )
        dataset.historico.append(hist)

    # ----------------------------------------------------------------

    def exibir_exportacao(self, nome, dataset):
        df = dataset.df
        st.subheader(f"Exportação de Dados: {dataset.nome}")
        # pasta_out = OUTPUT_DIR / nome
        # pasta_out.mkdir(exist_ok=True)

        st.subheader("Prévia dos Dados")
        st.dataframe(df.head(5))

        st.divider()
        st.subheader("Exportação de Tabelas")
        col1, col2, col3 = st.columns(3)

        with col1:
            try:
                if st.download_button(
                    "Baixar CSV",
                    data=self.export.exportar_csv(df),
                    file_name=f"{nome}.csv",
                    mime="text/csv",
                    key=f"{nome}_dl_csv",
                ):
                    self.registrar_operacao(dataset, "csv")
            except Exception as e:
                st.error(f"Erro ao gerar CSV: {e}")

            try:
                if st.download_button(
                    "Baixar Excel (.xlsx)",
                    data=self.export.exportar_excel(df),
                    file_name=f"{nome}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"{nome}_dl_excel",
                ):
                    self.registrar_operacao(dataset, "excel")
            except Exception as e:
                st.error(f"Erro ao gerar Excel: {e}")

        with col2:
            try:
                if st.download_button(
                    "Baixar JSON",
                    data=self.export.exportar_json(df),
                    file_name=f"{nome}.json",
                    mime="application/json",
                    key=f"{nome}_dl_json",
                ):
                    self.registrar_operacao(dataset, "json")
            except Exception as e:
                st.error(f"Erro ao gerar JSON: {e}")

            try:
                if st.download_button(
                    "Baixar LaTeX (.tex)",
                    data=self.export.exportar_latex(df),
                    file_name=f"{nome}.tex",
                    mime="text/plain",
                    key=f"{nome}_dl_latex",
                ):
                    self.registrar_operacao(dataset, "latex")
            except Exception as e:
                st.error(f"Erro ao gerar LaTeX: {e}")

        with col3:
            try:
                if st.download_button(
                    "Baixar Parquet",
                    data=self.export.exportar_parquet(df),
                    file_name=f"{nome}.parquet",
                    mime="application/octet-stream",
                    key=f"{nome}_dl_parquet",
                ):
                    self.registrar_operacao(dataset, "parquet")
            except Exception as e:
                st.error(f"Erro ao gerar Parquet: {e}")

            try:
                if st.download_button(
                    "Baixar Pacote ZIP",
                    data=self.export.exportar_zip(df, nome_base=nome),
                    file_name=f"{nome}.zip",
                    mime="application/zip",
                    key=f"{nome}_dl_zip",
                ):
                    self.registrar_operacao(dataset, "zip")
            except Exception as e:
                st.error(f"Erro ao gerar ZIP: {e}")

        if hasattr(dataset, "figuras") and dataset.figuras:
            st.divider()
            st.subheader("Exportação de Gráficos Salvos")

            for i, fig_obj in enumerate(dataset.figuras):
                col_fig1, col_fig2 = st.columns([3, 1])

                with col_fig1:
                    st.write(f"**{fig_obj.nome}**")

                with col_fig2:
                    # Exportação da figura Plotly em formato HTML interativo
                    try:
                        html_bytes = fig_obj.figura.to_html().encode("utf-8")
                        st.download_button(
                            label="Baixar HTML",
                            data=html_bytes,
                            file_name=f"{fig_obj.nome}.html",
                            mime="text/html",
                            key=f"{nome}_fig_dl_{i}",
                        )
                    except Exception as e:
                        st.error(f"Erro ao exportar gráfico: {e}")

        st.divider()
        st.subheader("Exportação de Instâncias")
        st.text("Recuso para salvar um json com todas as configurações dos datasets trabalha dos durante a sessão.")

        if st.button(f"Salvar Configurações para: {dataset.nome}"):
            utl.salvar_instancias(dataset)
            st.success(f"Instância '{dataset.nome}' salva")
