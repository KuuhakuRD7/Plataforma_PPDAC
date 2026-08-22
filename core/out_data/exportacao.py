import io
import shutil
import zipfile
from pathlib import Path
import pandas as pd


class Exportador:

    def exportar_csv(self, df: pd.DataFrame, destino=None):
        if destino is not None:
            return df.to_csv(destino, index=False)
        return df.to_csv(index=False).encode("utf-8")

    def exportar_excel(self, df: pd.DataFrame, destino=None):
        if destino is not None:
            return df.to_excel(destino, index=False)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        buffer.seek(0)
        return buffer.getvalue()

    def exportar_json(self, df: pd.DataFrame, destino=None):
        if destino is not None:
            return df.to_json(destino, orient="records", indent=2)
        return df.to_json(orient="records", indent=2).encode("utf-8")

    def exportar_latex(self, df: pd.DataFrame, destino=None):
        tabela = df.to_latex(index=False)
        documento = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{booktabs}}

\\begin{{document}}

{tabela}

\\end{{document}}
"""
        if destino is not None:
            with open(destino, "w", encoding="utf-8") as f:
                f.write(documento)
            return destino

        return documento.encode("utf-8")

    def exportar_parquet(self, df: pd.DataFrame, destino=None):
        if destino is not None:
            return df.to_parquet(destino, index=False)

        buffer = io.BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)
        return buffer.getvalue()

    def exportar_zip(self, df: pd.DataFrame, nome_base: str = "dados", origem=None, destino=None):
        """
        - Se 'destino' for passado, compacta uma pasta 'origem' no disco.
        - Se 'destino' for None, gera um arquivo ZIP em memória contendo todos os formatos do DataFrame.
        """
        if destino is not None and origem is not None:
            return shutil.make_archive(
                base_name=str(Path(destino).with_suffix("")),
                format="zip",
                root_dir=origem
            )

        # Geração do ZIP 100% em memória
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(f"{nome_base}.csv", self.exportar_csv(df))
            zip_file.writestr(f"{nome_base}.xlsx", self.exportar_excel(df))
            zip_file.writestr(f"{nome_base}.json", self.exportar_json(df))
            zip_file.writestr(f"{nome_base}.tex", self.exportar_latex(df))
            zip_file.writestr(f"{nome_base}.parquet",
                              self.exportar_parquet(df))

        zip_buffer.seek(0)
        return zip_buffer.getvalue()
