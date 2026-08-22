import copy
from datetime import datetime
import streamlit as st
from core.proc_data.analise import Analisador as anl
from core.model.dataset import Dataset, DatasetHistorico


class AnalisadorUI:

    def __init__(self):
        self.historico_analise = {}

    # ----------------------------------------------------------------

    def _registrar_operacao(
        self,
        dataset_origem: Dataset,
        sufixo_nome: str,
        novo_df,
        operacao: str,
        parametros: dict,
    ) -> Dataset:
        nome_analisado = f"{dataset_origem.nome}_{sufixo_nome}"

        novo_dataset = copy.deepcopy(dataset_origem)
        novo_dataset.nome = nome_analisado
        novo_dataset.df = novo_df

        novo_dataset.metadata.atualizado_em = datetime.now()
        novo_dataset.metadata.linhas = novo_df.shape[0]
        novo_dataset.metadata.colunas = novo_df.shape[1]

        registro_historico = DatasetHistorico(
            modulo="AnalisadorUI",
            operacao=operacao,
            parametros=parametros,
        )
        novo_dataset.historico.append(registro_historico)

        dataset_origem.variacoes.append(nome_analisado)

        st.session_state["datasets-analisado"][nome_analisado] = novo_dataset
        return novo_dataset

    # ----------------------------------------------------------------
    def exibir_juncao(self, dataset: Dataset):
        nome = dataset.nome
        df = dataset.df

        st.info(
            "O segundo DataFrame deve estar carregado no Session State."
        )

        repositorio_datasets = st.session_state.get("datasets", {})

        if len(repositorio_datasets) < 2:
            st.warning("Nenhum outro DataFrame disponível para junção.")
            return

        opcoes = [k for k in repositorio_datasets.keys() if k != nome]
        if not opcoes:
            st.warning(
                "Selecione um dataset diferente do atual para a junção.")
            return

        opc = st.selectbox(
            "Selecione o Dataset para Junção",
            opcoes,
            key=f"{nome}_select_ds2",
        )
        obj_dataset2 = repositorio_datasets[opc]
        df2 = obj_dataset2.df if isinstance(
            obj_dataset2, Dataset) else obj_dataset2
        left_keys = st.multiselect(
            "Colunas do DataFrame Atual",
            options=df.columns.tolist(),
            key=f"{nome}_left_keys"
        )

        right_keys = st.multiselect(
            "Colunas do DataFrame de Junção",
            options=df2.columns.tolist(),
            key=f"{nome}_right_keys"
        )

        how = st.selectbox(
            "Tipo de Join",
            [
                "inner",
                "left",
                "right",
                "outer"
            ],
            key=f"{nome}_join_type"
        )

        merge_key = f"merge_{nome}"

        if st.button(
            "Executar Junção",
            key=f"{nome}_btn_juncao"
        ):

            if not left_keys or not right_keys:

                st.warning(
                    "Selecione as colunas de junção."
                )

            elif len(left_keys) != len(right_keys):

                st.warning(
                    "A quantidade de colunas deve ser igual nos dois DataFrames."
                )

            else:

                resultado = anl.juncao(
                    df,
                    df2,
                    left_keys,
                    right_keys,
                    how
                )

                st.session_state["resultado_atual"][nome] = resultado
                st.session_state[merge_key] = {
                    "resultado": resultado,
                    "params": {
                        "dataset_direita": opc,
                        "chaves_esquerda": left_keys,
                        "chaves_direita": right_keys,
                        "tipo_juncao": how,
                    },
                }

        if merge_key in st.session_state:
            dados_merge = st.session_state[merge_key]
            resultado = dados_merge["resultado"]
            params = dados_merge["params"]

            st.success(f"{len(resultado)} registros encontrados na junção.")
            st.dataframe(resultado, width="stretch")

            if st.button("Gravar Junção", key=f"btnaj_{nome}"):
                novo_obj = self._registrar_operacao(
                    dataset_origem=dataset,
                    sufixo_nome="juncao",
                    novo_df=resultado,
                    operacao="Junção",
                    parametros=params,
                )
                st.success(f"Dataset '{novo_obj.nome}' criado com sucesso.")
                st.dataframe(novo_obj.df.head())

    # ----------------------------------------------------------------
    def exibir_filtragem(self, dataset: Dataset):
        nome = dataset.nome
        df = dataset.df

        coluna_filtro = st.selectbox(
            "Selecione a coluna",
            options=df.columns.tolist(),
            key=f"{nome}_filtro_coluna"
        )

        valores_disponiveis = (
            df[coluna_filtro]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        valores_selecionados = st.multiselect(
            "Selecione os valores",
            options=valores_disponiveis,
            key=f"{nome}_filtro_valores"
        )

        filtros = {
            coluna_filtro: valores_selecionados
        }

        resultado = anl.filtrar_dados(
            df,
            **filtros
        )

        st.session_state["resultado_atual"][nome] = resultado

        st.write("Dados filtrados")
        st.dataframe(resultado, width='stretch')

        if st.button("Gravar Filtros", key=f"btnaf_{nome}"):
            novo_obj = self._salvar_dataset_analisado(
                dataset_origem=dataset,
                sufixo_nome="filtrado",
                novo_df=resultado,
                operacao="Filtragem",
                parametros=filtros,
            )
            st.success(f"Dataset '{novo_obj.nome}' criado com sucesso.")
            st.dataframe(novo_obj.df.head())

    # ----------------------------------------------------------------
    def exibir_agregacao(self, dataset: Dataset):
        nome = dataset.nome
        df = dataset.df

        eixo_x = st.selectbox(
            "Agrupar por",
            options=df.columns.tolist(),
            key=f"{nome}_ag_eixo"
        )

        colunas_numericas = (
            df
            .select_dtypes(include="number")
            .columns
            .tolist()
        )

        if not colunas_numericas:

            st.warning(
                "Não existem colunas numéricas para agregação."
            )
            return

        coluna_alvo = st.selectbox(
            "Coluna alvo",
            options=[
                c for c in colunas_numericas
                if c != eixo_x
            ],
            key=f"{nome}_ag_coluna"
        )

        colunas_secundarias = st.multiselect(
            "Agrupamentos adicionais (opcional)",
            options=[
                c for c in df.columns
                if c != eixo_x
            ],
            key=f"{nome}_ag_selections"
        )

        top_n = st.number_input(
            "Top N",
            min_value=1,
            max_value=len(df),
            value=min(10, len(df)),
            step=1,
            key=f"{nome}_ag_top"
        )

        ordenar = st.checkbox(
            "Ordenar resultado",
            value=True,
            key=f"{nome}_ag_ord"
        )

        resultado = anl.agregar_dados(
            df=df,
            eixo_x=eixo_x,
            coluna_alvo=coluna_alvo,
            selections=colunas_secundarias,
            top_n=top_n,
            ordenar=ordenar
        )

        st.session_state["resultado_atual"][nome] = resultado

        st.write("Dados agregados")
        st.dataframe(resultado, width='stretch')

        if st.button("Gravar Agregação", key=f"btnaa_{nome}"):
            params_agregacao = {
                "eixo_x": eixo_x,
                "coluna_alvo": coluna_alvo,
                "selections": colunas_secundarias,
                "top_n": top_n,
                "ordenar": ordenar,
            }

            novo_obj = self._salvar_dataset_analisado(
                dataset_origem=dataset,
                sufixo_nome="agregado",
                novo_df=resultado,
                operacao="Agregação",
                parametros=params_agregacao,
            )
            st.success(f"Dataset '{novo_obj.nome}' criado com sucesso.")
            st.dataframe(novo_obj.df.head())

    # ----------------------------------------------------------------
    def exibir_analise(self, nome, dataset):
        if "resultado_atual" not in st.session_state:
            st.session_state["resultado_atual"] = {}

        st.subheader(f"Dataset em Analise:{nome} ")
        if dataset is not None:

            with st.expander("Filtros"):
                self.exibir_filtragem(dataset)
            with st.expander("Agregações"):
                self.exibir_agregacao(dataset)
            with st.expander("Junção"):
                self.exibir_juncao(dataset)
