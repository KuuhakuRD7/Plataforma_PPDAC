import pandas as pd

import plotly.express as px
import plotly.graph_objects as go


class Visualizador:

    @staticmethod
    def _aplicar_layout_padrao(fig: go.Figure, titulo: str = "Grafico") -> go.Figure:
        fig.update_layout(
            title=titulo,
            height=600,
            width=600,
            template='plotly_white',
            margin=dict(l=40, r=40, t=60, b=40)
        )

        return fig

    # ----------------------------------------------------------------
    @staticmethod
    def grafico_barra(df: pd.DataFrame, x: str, y: str, color: str = None) -> go.Figure:
        fig = px.bar(df, x=x, y=y, color=color)
        return fig

    # ----------------------------------------------------------------
    @staticmethod
    def grafico_linha(df: pd.DataFrame, x: str, y: str, color: str = None) -> go.Figure:
        fig = px.line(df, x=x, y=y, color=color)
        return fig

    # ----------------------------------------------------------------
    @staticmethod
    def grafico_area(df: pd.DataFrame, x: str, y: str, color: str = None) -> go.Figure:
        fig = px.area(df, x=x, y=y, color=color)
        return fig

    # ----------------------------------------------------------------

    @staticmethod
    def grafico_pizza(df: pd.DataFrame, x: str, y: str, color: str = None) -> go.Figure:
        fig = px.pie(df, x=x, y=y, color=color)
        return fig

    # ----------------------------------------------------------------

    @staticmethod
    def grafico_dispersao(df: pd.DataFrame, x: str, y: str, color: str = None) -> go.Figure:
        fig = px.scatter(df, x=x, y=y, color=color, trendline="ols")
        return fig

    # ----------------------------------------------------------------

    @staticmethod
    def grafico_bolhas(df: pd.DataFrame, x: str, y: str, color: str = None) -> go.Figure:
        fig = px.scatter(df, x=x, y=y, color=color)
        return fig

    # ----------------------------------------------------------------
    @staticmethod
    def grafico_caixas(df: pd.DataFrame, x: str, y: str, color: str = None) -> go.Figure:
        fig = px.box(df, x=x, y=y, color=color)
        return fig

    # ----------------------------------------------------------------

    @staticmethod
    def grafico_funil(df: pd.DataFrame, x: str, y: str, color: str = None) -> go.Figure:
        fig = px.funnel(df, x=x, y=y, color=color)
        return fig

    # ----------------------------------------------------------------

    @staticmethod
    def grafico_mosaico(df: pd.DataFrame, x: str, y: str, color: str = None) -> go.Figure:
        path = [col for col in [x, y] if col]
        fig = px.treemap(df, path=path, values=color)
        return fig

    # ----------------------------------------------------------------

    @staticmethod
    def grafico_cascata(df: pd.DataFrame, x: str, y: str, color: str = None) -> go.Figure:
        fig = go.Figure(go.Waterfall(
            x=df[x],
            y=df[y],
            measure=['relative'] * len(df)
        ))

        return fig

    # ----------------------------------------------------------------
    @staticmethod
    def grafico_sankey(df: pd.DataFrame, x: str, y: str, color: str = None) -> go.Figure:
        labels = list(set(df[x].astype(str).unique()).union(
            set(df[y].astype(str).unique())))
        mapa = {label: idx for idx, label in enumerate(labels)}
        fig = go.Figure(go.Sankey(
            node=dict(label=labels),
            link=dict(
                source=df[x].astype(str).map(mapa),
                target=df[y].astype(str).map(mapa),
                value=df[color]
            )
        ))

        return fig

    # ----------------------------------------------------------------
    @staticmethod
    def grafico_radar(df: pd.DataFrame, x: str, y: str, color: str = None) -> go.Figure:

        fig = go.Figure(go.Scatterpolar(
            r=df[x],
            theta=df[y],
            fill='toself',
            name=str(color)
        ))

        fig.update_layout(polar=dict(radialaxis=dict(visible=True)))

        return fig
