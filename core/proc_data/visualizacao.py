import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns

from core.proc_data.exploracao import agregar_dados

sns.set_style('whitegrid')
TEMPLATE = 'plotly_white'


def grafico_barra(
    df,
    eixo_x=None,
    eixo_y=None,
    coluna_categoria=None,
    top_n=10,
    stacked=False
):

    if coluna_categoria:

        fig = px.bar(

            df,

            x=eixo_x,
            y=eixo_y,
            color=coluna_categoria,

            barmode='stack' if stacked else 'group',

            template=TEMPLATE
        )

    else:

        fig = px.bar(

            df,

            x=eixo_x,
            y=eixo_y,

            template=TEMPLATE
        )

    fig.update_layout(
        title='Bar Chart',
        height=600
    )

    # fig.show()
    return fig


def grafico_linha(
    df,
    eixo_x,
    eixo_y,
    coluna_categoria=None
):

    fig = px.line(
        df,
        x=eixo_x,
        y=eixo_y,
        color=coluna_categoria,
        markers=True,
        template=TEMPLATE
    )

    fig.update_layout(
        title="Line Chart",
        height=600
    )

    return fig


def grafico_area(
    df,
    eixo_x,
    eixo_y,
    coluna_categoria=None
):

    fig = px.area(
        df,
        x=eixo_x,
        y=eixo_y,
        color=coluna_categoria,
        template=TEMPLATE
    )

    fig.update_layout(
        title="Area Chart",
        height=600
    )

    return fig


def grafico_pizza(
    df,
    categoria,
    valor,
    top_n=10
):

    resultado = (
        df.groupby(categoria)[valor]
        .sum()
        .reset_index()
        .sort_values(
            valor,
            ascending=False
        )
        .head(top_n)
    )

    fig = px.pie(
        resultado,
        names=categoria,
        values=valor,
        template=TEMPLATE
    )

    fig.update_layout(
        title='Pie Chart',
        height=600
    )
    return fig


def grafico_dispersao(
    df,
    coluna_x,
    coluna_y,
    coluna_categoria=None
):

    fig = px.scatter(

        df,

        x=coluna_x,
        y=coluna_y,

        color=coluna_categoria,

        trendline='ols',

        template=TEMPLATE
    )

    fig.update_layout(
        title='Scatter Plot',
        height=600
    )

    return fig


def grafico_bolhas(
    df,
    coluna_x,
    coluna_y,
    coluna_tamanho,
    coluna_categoria=None
):

    fig = px.scatter(

        df,

        x=coluna_x,
        y=coluna_y,

        size=coluna_tamanho,

        color=coluna_categoria,

        size_max=60,

        template=TEMPLATE
    )

    fig.update_layout(
        title='Bubble Chart',
        height=600
    )

    return fig

    fig = px.scatter(

        df,

        x=coluna_x,
        y=coluna_y,

        size=coluna_tamanho,

        color=coluna_categoria,

        hover_name='MUNICIPIO',

        size_max=60,

        template=TEMPLATE
    )

    fig.update_layout(
        title='Bubble Chart',
        height=600
    )

    return fig


def grafico_caixas(
    df,
    eixo_x,
    eixo_y
):

    fig = px.box(

        df,

        x=eixo_x,
        y=eixo_y,

        template=TEMPLATE
    )

    fig.update_layout(
        title='Box Plot',
        height=600
    )

    return fig


def grafico_cascata(
    df,
    eixo_x,
    eixo_y,
    top_n=10
):

    resultado = (
        df
        .groupby(eixo_x)[eixo_y]
        .sum()
        .reset_index()
        .sort_values(
            eixo_y,
            ascending=False
        )
        .head(top_n)
    )

    fig = go.Figure(

        go.Waterfall(

            x=resultado[eixo_x],

            y=resultado[eixo_y],

            measure=['relative'] * len(resultado)
        )
    )

    fig.update_layout(
        title='Waterfall Chart',
        template=TEMPLATE,
        height=600
    )

    return fig


def grafico_funil(
    df,
    eixo_x,
    eixo_y,
    top_n=10
):

    resultado = (
        df
        .groupby(eixo_x)[eixo_y]
        .sum()
        .reset_index()
        .sort_values(
            eixo_y,
            ascending=False
        )
        .head(top_n)
    )

    fig = px.funnel(

        resultado,

        x=eixo_y,
        y=eixo_x,

        template=TEMPLATE
    )

    fig.update_layout(
        title='Funnel Chart',
        height=600
    )

    return fig

    dados = filtrar_dados(
        df,
        ano=ano
    )

    resultado = agregar_dados(
        dados,
        eixo_x=eixo_x,
        top_n=top_n
    )

    resultado = resultado.sort_values(
        by='VALOR',
        ascending=True
    )

    fig = px.funnel(

        resultado,

        x='VALOR',
        y=eixo_x,

        template=TEMPLATE
    )

    fig.update_layout(
        title='Funnel Chart',
        height=600
    )

    return fig


def grafico_sankey(
    df,
    origem,
    destino
):

    tabela = (
        df
        .groupby([origem, destino])
        .size()
        .reset_index(name='valor')
    )

    labels = list(
        set(
            tabela[origem].tolist() +
            tabela[destino].tolist()
        )
    )

    mapa = {
        label: i
        for i, label in enumerate(labels)
    }

    fig = go.Figure(

        go.Sankey(

            node=dict(
                label=labels
            ),

            link=dict(

                source=tabela[origem].map(mapa),

                target=tabela[destino].map(mapa),

                value=tabela['valor']
            )
        )
    )

    fig.update_layout(
        title='Sankey Diagram',
        template=TEMPLATE,
        height=700
    )

    return fig


def grafico_mosaico(
    df,
    coluna1,
    coluna2,
    valor,
    top_n=5
):

    top = (

        df

        .groupby(coluna1)[valor]
        .sum()

        .sort_values(ascending=False)

        .head(top_n)

        .index
    )

    dados = df[
        df[coluna1].isin(top)
    ]

    tabela = (

        dados

        .groupby([coluna1, coluna2])[valor]
        .sum()

        .reset_index()
    )

    fig = px.treemap(

        tabela,

        path=[coluna1, coluna2],

        values=valor,

        color=valor,

        template=TEMPLATE
    )

    fig.update_layout(
        title='Mosaic / Treemap',
        height=700
    )

    return fig


def grafico_radar(
    df,
    categoria,
    valor,
    grupo
):

    resultado = (

        df

        .groupby(categoria)[valor]
        .sum()

        .reset_index()
    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatterpolar(

            r=resultado[valor],

            theta=resultado[categoria],

            fill='toself',

            name=str(grupo)
        )
    )

    fig.update_layout(

        polar=dict(
            radialaxis=dict(
                visible=True
            )
        ),

        template=TEMPLATE,

        title='Radar Chart',
        height=700
    )

    return fig
