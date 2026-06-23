import pandas as pd


def filtrar_dados(df, **filtros):

    dados = df.copy()

    for coluna, valor in filtros.items():

        if coluna not in dados.columns:
            continue

        if valor is None:
            continue

        # Ignora lista vazia
        if isinstance(valor, (list, tuple, set)) and len(valor) == 0:
            continue

        if isinstance(valor, (list, tuple, set)):
            dados = dados[dados[coluna].astype(str).isin(valor)]
            # dados = dados[dados[coluna].isin(valor)]

        else:
            dados = dados[dados[coluna].astype(str) == str(valor)]
            # dados = dados[dados[coluna] == valor]

    return dados


def agregar_dados(
    df,
    eixo_x,
    coluna_alvo=None,
    selections=None,
    operacao="sum",
    top_n=None,
    ordenar=True
):

    if eixo_x == coluna_alvo:
        raise ValueError(
            "A coluna alvo não pode ser igual ao eixo de agrupamento."
        )

    keys = [eixo_x]

    if selections:
        keys += selections

    # COUNT sem coluna alvo
    if operacao == "count" and coluna_alvo is None:

        resultado = (
            df
            .groupby(keys)
            .size()
            .reset_index(name="contagem")
        )

        return resultado

    grupo = (df.groupby(keys)[coluna_alvo])

    if operacao == "sum":
        resultado = grupo.sum().reset_index()

    elif operacao == "mean":
        resultado = grupo.mean().reset_index()

    elif operacao == "count":
        resultado = grupo.count().reset_index()

    elif operacao == "max":
        resultado = grupo.max().reset_index()

    elif operacao == "min":
        resultado = grupo.min().reset_index()

    # Ordenação
    if ordenar and coluna_alvo:
        resultado = resultado.sort_values(
            by=coluna_alvo,
            ascending=False
        )

    # Top N
    if top_n:
        resultado = resultado.head(top_n)

    return resultado
