import streamlit as st
from datetime import datetime
import pandas as pd


class RelatadorUI:
    def __init__(self):
        self.data_relatorio = datetime.now()
        self.conclusao = {
            "titulo_projeto": "",
            "resumo_executivo": "",
            "resposta_problema": "",
            "validacao_hipoteses": pd.DataFrame(),
            "principais_insights": "",
            "limitacoes_vieses": "",
            "recomendacoes_decisao": pd.DataFrame(),
            "proximos_passos": ""
        }

    def _df_para_markdown(self, df: pd.DataFrame, texto_vazio: str = "*Nenhum registro informado.*") -> str:
        """Converte DataFrame em tabela Markdown."""
        if df is None or df.empty:
            return f"{texto_vazio}\n"
        return df.to_markdown(index=False) + "\n"

    def gerar_markdown(self) -> str:
        """Gera a versão em Markdown do Relatório de Conclusão PPDAC."""
        titulo = self.conclusao[
            "titulo_projeto"] or "Relatório de Conclusão da Análise (PPDAC)"
        data_str = self.data_relatorio.strftime("%d/%m/%Y às %H:%M")

        md_content = f"""# Relatório de Conclusão Analítica (PPDAC)
**Projeto:** {titulo}
**Data de Emissão:** {data_str}
**Framework:** PPDAC - Step 5: Conclusion

---

## 1. Resumo Executivo
{self.conclusao['resumo_executivo'] or '*Sem resumo executivo fornecido.*'}

---

## 2. Resposta ao Problema de Pesquisa
> {self.conclusao['resposta_problema'] or '*A resposta principal ainda não foi sintetizada.*'}

---

## 3. Validação das Hipóteses
{self._df_para_markdown(self.conclusao['validacao_hipoteses'])}

---

## 4. Principais Insights e Descobertas (Analysis ➔ Conclusion)
{self.conclusao['principais_insights'] or '*Nenhum insight cadastrado.*'}

---

## 5. Limitações dos Dados e Viéses
{self.conclusao['limitacoes_vieses'] or '*Nenhuma limitação relatada.*'}

---

## 6. Recomendações e Tomada de Decisão
{self._df_para_markdown(self.conclusao['recomendacoes_decisao'])}

---

## 7. Próximos Passos e Trabalhos Futuros
{self.conclusao['proximos_passos'] or '*Sem próximos passos mapeados.*'}
"""
        return md_content

    def gerar_latex(self) -> str:
        """Gera o código fonte em LaTeX do Relatório de Conclusão."""
        titulo = self.conclusao["titulo_projeto"] or "Relatorio de Conclusao Analitica"
        data_str = self.data_relatorio.strftime("%d/%m/%Y")

        latex_code = f"""\\documentclass[12pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[brazil]{{babel}}
\\usepackage{{geometry}}
\\usepackage{{booktabs}}
\\usepackage{{hyperref}}
\\usepackage{{xcolor}}

\\geometry{{margin=1in}}
\\definecolor{{primarycolor}}{{HTML}}{{1B5E20}}

\\title{{\\textbf{{\\color{{primarycolor}} Relatório de Conclusão Analítica (PPDAC)}}\\\\\\large {titulo}}}
\\author{{Plataforma PPDAC}}
\\date{{{data_str}}}

\\begin{{document}}

\\maketitle

\\section{{Resumo Executivo}}
{self.conclusao['resumo_executivo'] or 'Sem resumo fornecido.'}

\\section{{Resposta ao Problema de Pesquisa}}
{self.conclusao['resposta_problema']
            or 'A resposta principal não foi definida.'}

\\section{{Principais Insights}}
{self.conclusao['principais_insights'] or 'Nenhum insight detalhado.'}

\\section{{Limitações e Viéses}}
{self.conclusao['limitacoes_vieses'] or 'Nenhuma limitação detalhada.'}

\\section{{Próximos Passos}}
{self.conclusao['proximos_passos'] or 'Nenhum próximo passo.'}

\\end{{document}}
"""
        return latex_code

    def exibir_relato(self, nome=None, dataset_obj=None):

        if dataset_obj is not None and hasattr(dataset_obj, 'df') and dataset_obj.df is not None:
            with st.expander("Resumo do Dataset Atual", expanded=False):
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Total de Linhas", dataset_obj.df.shape[0])
                col_b.metric("Total de Colunas", dataset_obj.df.shape[1])
                col_c.metric("Colunas Numéricas", len(
                    dataset_obj.df.select_dtypes(include=['number']).columns))
                st.dataframe(dataset_obj.df.head(3), use_container_width=True)

        with st.form("form_conclusao_ppdac"):
            st.subheader("Identificação e Síntese")
            self.conclusao["titulo_projeto"] = st.text_input(
                "Título do Projeto / Análise:",
                value=self.conclusao["titulo_projeto"],
                placeholder="Ex: Análise de Incidência de Dengue nos Municípios do Pará (2020-2024)"
            )

            self.conclusao["resumo_executivo"] = st.text_area(
                "Resumo Executivo:",
                value=self.conclusao["resumo_executivo"],
                placeholder="Breve resumo da investigação, destacando as descobertas mais relevantes."
            )

            self.conclusao["resposta_problema"] = st.text_area(
                "Resposta Direta ao Problema Inicial:",
                value=self.conclusao["resposta_problema"],
                placeholder="Como os dados respondem à pergunta central formulada na etapa de Problem?"
            )

            st.subheader("Validação das Hipóteses")
            st.caption(
                "Insira o resultado do teste das hipóteses formuladas no planejamento.")

            # Editor interativo de tabela para hipóteses
            df_hipoteses_def = pd.DataFrame([
                {"Hipótese": "Existe correlação entre X e Y",
                    "Status": "Validada", "Evidência": "p-valor < 0.05 e r = 0.82"},
                {"Hipótese": "O indicador Z cresceu em 2023", "Status": "Refutada",
                    "Evidência": "Queda observada de 12% no período"}
            ]) if self.conclusao["validacao_hipoteses"].empty else self.conclusao["validacao_hipoteses"]

            edited_hipoteses = st.data_editor(
                df_hipoteses_def,
                num_rows="dynamic",
                width='stretch',
                key="editor_hipoteses"
            )
            self.conclusao["validacao_hipoteses"] = edited_hipoteses

            st.subheader("Insights e Limitações")
            self.conclusao["principais_insights"] = st.text_area(
                "Principais Insights e Padrões Descobertos:",
                value=self.conclusao["principais_insights"],
                placeholder="Descreva padrões surpreendentes, clusters ou anomalias encontradas durante a Análise."
            )

            self.conclusao["limitacoes_vieses"] = st.text_area(
                "Limitações dos Dados ou Possíveis Viéses:",
                value=self.conclusao["limitacoes_vieses"],
                placeholder="Ex: Dados faltantes em determinado município, amostra restrita a determinado período, etc."
            )

            st.subheader("Recomendações e Próximos Passos")
            df_recom_def = pd.DataFrame([
                {"Ação Recomendada": "Alocar recursos na região X",
                    "Público/Responsável": "Gestão Operacional", "Impacto": "Alto"},
            ]) if self.conclusao["recomendacoes_decisao"].empty else self.conclusao["recomendacoes_decisao"]

            edited_recom = st.data_editor(
                df_recom_def,
                num_rows="dynamic",
                width='stretch',
                key="editor_recom"
            )
            self.conclusao["recomendacoes_decisao"] = edited_recom

            self.conclusao["proximos_passos"] = st.text_area(
                "Próximos Passos ou Trabalhos Futuros:",
                value=self.conclusao["proximos_passos"],
                placeholder="Ações subsequentes recomendadas (Ex: Treinar um modelo preditivo, coletar mais dados)."
            )

            btn_salvar = st.form_submit_state = st.form_submit_button(
                "Salvar Dados da Conclusão")
            if btn_salvar:
                st.success(
                    "Dados do Relatório de Conclusão atualizados com sucesso!")

        st.divider()

        st.subheader("Exportar Planejamento")
        col1, col2 = st.columns(2)

        with col1:
            codigo_tex = self.gerar_latex()
            st.download_button(
                label="Baixar Relatório em LaTex (.tex)",
                data=codigo_tex,
                file_name=f"plano_{
                    datetime.now().strftime('%Y%m%d_%H%M')}.tex",
                mime="text/x-tex",
                key=f"exportar_conclusao_latex"
            )

            codigo_md = self.gerar_markdown()
            st.download_button(
                label="Baixar Relatório em Markdown (.md)",
                data=codigo_md,
                file_name=f"plano_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                key=f"exportar_conclusao_markdown"
            )

        with col2:
            with st.expander("Visualizar Relatório em LaTex"):
                st.code(codigo_tex, language="latex")

            with st.expander("Visualizar Relatório em Markdown"):
                st.markdown(codigo_md)
