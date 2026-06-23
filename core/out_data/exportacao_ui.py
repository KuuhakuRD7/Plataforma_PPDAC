import streamlit as st
import pandas as pd
from core.in_data.obtencao import DIRETORIOS, UPLOAD_DIR, OUTPUT_DIR
from core.out_data.exportacao import *


def exibir_exportacao(nome, df):
    pasta_in = UPLOAD_DIR / nome

    pasta_out = OUTPUT_DIR / nome
    pasta_in.mkdir(exist_ok=True)

    pasta_out.mkdir(exist_ok=True)

    st.dataframe(df.head(5))

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        csv = exportar_csv(df)
        st.download_button(
            "Baixar CSV",
            data=csv,
            file_name=f"{nome}.csv",
            mime="text/csv"
        )

        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        excel_buffer.seek(0)
        st.download_button(
            "Baixar Excel",
            data=excel_buffer.getvalue(),
            file_name=f"{nome}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col2:

        json_data = exportar_json(df)
        st.download_button(
            "Baixar JSON",
            data=json_data,
            file_name=f"{nome}.json",
            mime="application/json"
        )

        latex_data = exportar_latex(df)
        st.download_button(
            "Baixar LaTeX",
            data=latex_data,
            file_name=f"{nome}.tex",
            mime="text/plain"
        )

    with col3:

        parquet_data = exportar_parquet(df)
        st.download_button(
            "Baixar Parquet",
            data=parquet_data,
            file_name=f"{nome}.parquet",
            mime="application/octet-stream"
        )

        zip_data = exportar_zip(df, OUTPUT_DIR / nome)
        st.download_button(
            "Baixar ZIP",
            data=zip_data,
            file_name=f"{nome}.zip",
            mime="application/zip"
        )
