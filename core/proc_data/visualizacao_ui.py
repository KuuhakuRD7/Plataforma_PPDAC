from datetime import datetime

import streamlit as st
import plotly.graph_objects as go

from core.model.dataset import Dataset, DatasetHistorico, DatasetFiguras
from core.proc_data.visualizacao import Visualizador as vis
from wiki_data.tutor_ui import TutorUI


class VisualizadorUI:

    def __init__(self):
        self.mp_graficos = {
            "barra": vis.grafico_barra,
            "linha": vis.grafico_linha,
            "area": vis.grafico_area,
            "pizza": vis.grafico_pizza,
            "funil": vis.grafico_funil,
            "caixa": vis.grafico_caixas,
            "dispersao": vis.grafico_dispersao,
            "bolha": vis.grafico_bolhas,
            "mosaic": vis.grafico_mosaico,
            "radar": vis.grafico_radar,
            "cascata": vis.grafico_cascata,
            "sankey": vis.grafico_sankey
        }

    # ----------------------------------------------------------------

    def exibir_visualizacao(self, nome, dataset):
        df = dataset.df
        df_temp = df.copy()
        st.header("Visualizacao dos Dados")
        with st.expander("Dicas Sobre Gráficos"):
            ttw = TutorUI()
            dicas = ttw.carregar_markdown("./wiki_data/dicas_graficos.md")
            st.markdown(dicas)

        # graficos_comparar = ["barra", "radar", "pizza"]
        # graficos_mudancas = ["linha", "area", "cascata"]
        # graficos_organizar = ["mosaic", "funil"]
        # graficos_relacoes = ["dispersao", "bolha", "caixa", "sankey"]

        grafico = st.selectbox(
            "Selecione a visualizacao",
            options=list(self.mp_graficos.keys()),
            key=f"{nome}_grafico",
            index=None
        )

        eixo_x = None
        eixo_y = None
        color = None
        size = None

        stacked = False

        numericas = (
            df_temp
            .select_dtypes(include="number")
            .columns
        )

        # ---------------------------------

        eixo_x = st.selectbox(
            "Selecione eixo x",
            df_temp.columns,
            key=f"eixo_x_{nome}"
        )

        eixo_y = st.selectbox(
            "Selecione eixo y",
            df_temp.columns,
            key=f"eixo_y_{nome}"
        )

        color = st.selectbox(
            "Selecionar Cor",
            df_temp.columns,
            index=None,
            key=f"{nome}_cor"
        )

        if grafico is None:
            return
        # size = st.selectbox(
        #     "Selecionar Tamanho",
        #     df_temp.columns,
        #     index=None,
        #     key=f"{nome}_size"
        # )

        # top_n = st.number_input(
        #     "Top N",
        #     min_value=1,
        #     max_value=len(df_temp),
        #     value=min(10, len(df_temp)),
        #     step=1,
        #     key=f"{nome}_top_n"
        # )
        # if grafico in ["barra"]:
        #     stacked = st.toggle("Stacked")

        # ---------------------------------

        try:

            fn_grafico = self.mp_graficos[grafico]
            fig = fn_grafico(df_temp, eixo_x, eixo_y, color)
            fig = vis._aplicar_layout_padrao(fig)

            st.plotly_chart(fig, width='content')

            st.subheader("Salvar Visualização")
            titulo_figura = st.text_input(
                "Título/Identificador do Gráfico",
                value=f"Gráfico de {grafico.title()} - {dataset.nome}",
                key=f"{nome}_fig_title",
            )

            if st.button("Salvar Figura no Dataset", key=f"{nome}_btn_salvar_fig"):
                params_usados = {
                    "eixo_x": eixo_x,
                    "eixo_y": eixo_y,
                    "color": color,
                    # "size": size,
                    # "top_n": top_n,
                }

                nova_figura = DatasetFiguras(
                    nome=titulo_figura,
                    tipo=grafico,
                    figura=fig,
                    parametros=params_usados
                )

                if not hasattr(dataset, "figuras") or dataset.figuras is None:
                    dataset.figuras = []
                dataset.figuras.append(nova_figura)

                registro_hist = DatasetHistorico(
                    modulo="VisualizadorUI",
                    operacao=f"Criação de Gráfico ({grafico})",
                    parametros=params_usados,
                )
                dataset.historico.append(registro_hist)

                st.success(
                    f"Figura '{titulo_figura}' salva no dataset com sucesso!")
        except Exception as e:
            st.error(f"Erro ao gerar o grafico: {str(e)}")
