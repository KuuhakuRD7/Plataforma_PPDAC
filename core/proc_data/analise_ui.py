import streamlit as st
from core.proc_data.analise import *


def exibir_juncao(nome, df):

    st.info(
        "O segundo DataFrame deve estar carregado no Session State."
    )

    if "datasets" not in st.session_state or len(st.session_state["datasets"]) < 2:

        st.warning(
            "Nenhum DataFrame disponível para junção."
        )

    else:

        opc = st.selectbox(
            "A juntar", st.session_state["datasets"].keys())
        df2 = st.session_state["datasets"][opc]
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

            resultado = juncao(
                df,
                df2,
                left_keys,
                right_keys,
                how
            )

            st.session_state["resultado_atual"][nome] = resultado

            st.session_state[merge_key] = resultado

    if merge_key in st.session_state:

        resultado = st.session_state[merge_key]

        st.success(
            f"{len(resultado)} registros encontrados."
        )

        st.dataframe(
            resultado,
            width="stretch"
        )

        if st.button(
            "Aplicar Análise",
            key=f"btnaj_{nome}"
        ):

            analisado = f"{nome}_juncao"

            st.session_state["datasets-analisado"][
                analisado
            ] = resultado.copy()

            st.success(
                f"Dataset '{analisado}' criado."
            )

            st.dataframe(
                resultado.head()
            )


def exibir_filtragem(nome, df):

    cols = list(df.columns)

    filtros = {}

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

    resultado = filtrar_dados(
        df,
        **filtros
    )

    st.session_state["resultado_atual"][nome] = resultado

    st.write("Dados filtrados")
    st.dataframe(resultado, width='stretch')

    if st.button("Gravar Filtros", key=f"btnaf_{nome}"):
        analisado = f"{nome}_filtrado"
        st.session_state["datasets-analisado"][analisado] = resultado
        st.success(f"Dataset '{analisado}' criado.")
        st.dataframe(resultado.head())


def exibir_agregacao(nome, df):

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

    else:

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

    resultado = agregar_dados(
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

    if st.button("Gravar Agregacao", key=f"btnaa_{nome}"):
        analisado = f"{nome}_agregado"
        st.session_state["datasets-analisado"][analisado] = resultado
        st.success(f"Dataset '{analisado}' criado.")
        st.dataframe(resultado.head())


def exibir_analise(nome, df):
    df_temp = df.copy()

    if "resultado_atual" not in st.session_state:
        st.session_state["resultado_atual"] = {}

    st.header("Análise dos Dados")
    if df_temp is not None:

        with st.expander("Filtros"):
            exibir_filtragem(nome, df_temp)
        with st.expander("Agregações"):
            exibir_agregacao(nome, df_temp)
        with st.expander("Junção"):
            exibir_juncao(nome, df_temp)
