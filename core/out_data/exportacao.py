from pathlib import Path

import io
import shutil
import zipfile


def exportar_excel(df, destino=None):
    return df.to_excel(destino)


def exportar_json(df, destino=None):
    return df.to_json(destino)


def exportar_latex(df, destino=None):

    tabela = df.to_latex(index=False)

    documento = f"""
\\documentclass{{article}}
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


# def exportar_sql(df, destino=None): return df.to_sql()


def exportar_csv(df, destino=None):
    return df.to_csv(destino, index=False)


def exportar_parquet(df, destino=None):
    return df.to_parquet(destino, index=False)


def exportar_zip(df, origem, destino=None):

    # Caso queira salvar diretamente em disco
    if destino is not None:

        return shutil.make_archive(
            base_name=str(Path(destino).with_suffix("")),
            format="zip",
            root_dir=origem
        )

    # Caso queira retornar bytes em memória
    zip_buffer = io.BytesIO()

    origem = Path(origem)
    csv_file = exportar_csv(df, origem / (origem.name + ".csv"))
    excel_file = exportar_excel(df, origem / (origem.name + ".xlsx"))
    json_file = exportar_json(df, origem / (origem.name + ".json"))
    latex_file = exportar_latex(df, origem / (origem.name + ".tex"))
    parquet_file = exportar_parquet(df, origem/(origem.name + ".parquet"))

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:

        if origem.is_file():
            zip_file.write(origem, arcname=origem.name)

        else:
            for arquivo in origem.rglob("*"):

                if arquivo.is_file():
                    zip_file.write(
                        arquivo,
                        arcname=arquivo.relative_to(origem)
                    )

    zip_buffer.seek(0)

    return zip_buffer.getvalue()
