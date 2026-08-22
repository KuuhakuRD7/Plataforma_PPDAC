from datetime import datetime
import pandas as pd
import streamlit as st


class PlanejadorUI:
    def __init__(self):
        self.data_plano = datetime.now()
        self.plano = {
            "titulo": "",
            "descricao": "",
            "indicadores": pd.DataFrame(),
            "metas": pd.DataFrame(),
            "recursos": pd.DataFrame(),
            "atividades": pd.DataFrame(),
            "dados": pd.DataFrame(),
            "riscos": pd.DataFrame()
        }

    def _df_para_markdown(self, df: pd.DataFrame, titulo_vazio: str = "Nenhum dado registrado.") -> str:
        if df.empty:
            return f"*{titulo_vazio}*\n"

        # O argumento index=False remove a coluna de índices numéricos do Pandas
        return df.to_markdown(index=False) + "\n"

    def salvar_plano_md(self) -> str:
        """Gera o texto estruturado em formato Markdown a partir do dicionário self.plano."""

        titulo = self.plano["titulo"] if self.plano["titulo"] else "Plano de Ação e Projeto"
        data_str = self.data_plano.strftime("%d/%m/%Y às %H:%M")

        md_content = f"""# {titulo}
**Data de Geração:** {data_str}
**Plataforma:** Planejador de Projetos UI

---

## 1. Identificação do Problema

### Descrição do Cenário Atual e Impacto
{self.plano['descricao'] if self.plano['descricao']
            else '*Sem descrição fornecida.*'}

### Indicadores e Metas
{self._df_para_markdown(self.plano['indicadores'])}

---

## 2. Análise de Causas e Recursos

{self._df_para_markdown(self.plano['recursos'])}

---

## 3. Plano de Ação (5W2H)

{self._df_para_markdown(self.plano['atividades_5w2h'])}

---

## 4. Matriz de Riscos e Contingência

{self._df_para_markdown(self.plano['riscos'])}

---

## 5. Fontes de Dados e Repositórios

{self._df_para_markdown(self.plano['fontes'])}
"""
        return md_content

    def salvar_plano(self) -> str:
        """Gera o código LaTeX completo compilável a partir do dicionário self.plano."""

        # Converte DataFrames do Pandas para tabelas formatadas em LaTeX
        tex_indicadores = self.plano["indicadores"].to_latex(
            index=False, escape=True) if not self.plano["indicadores"].empty else "Nenhum indicador registrado."
        tex_recursos = self.plano["recursos"].to_latex(
            index=False, escape=True) if not self.plano["recursos"].empty else "Nenhum recurso registrado."
        tex_5w2h = self.plano["atividades_5w2h"].to_latex(
            index=False, escape=True) if not self.plano["atividades_5w2h"].empty else "Nenhuma atividade registrada."
        tex_riscos = self.plano["riscos"].to_latex(
            index=False, escape=True) if not self.plano["riscos"].empty else "Nenhum risco registrado."
        tex_fontes = self.plano["fontes"].to_latex(
            index=False, escape=True) if not self.plano["fontes"].empty else "Nenhuma fonte registrada."

        template_latex = f"""\\documentclass[12pt, a4paper]{{article}}
\\usepackage[utf8]{{utf8}}
\\usepackage[brazil]{{babel}}
\\usepackage{{geometry}}
\\usepackage{{booktabs}}
\\usepackage{{hyperref}}

\\geometry{{margin=2.5cm}}

\\title{{{self.plano['titulo'] if self.plano['titulo'] else 'Plano de Ação e Projeto'}}}
\\author{{Gerado via Planejador de Projetos}}
\\date{{{self.data_plano.strftime('%d/%m/%Y')}}}

\\begin{{document}}

\\maketitle

\\section{{1. Identificação do Problema}}
{self.plano['descricao']}

\\subsection{{Indicadores e Metas}}
{tex_indicadores}

\\section{{2. Análise de Causas e Recursos}}
{tex_recursos}

\\section{{3. Plano de Ação (5W2H)}}
\\small
{tex_5w2h}
\\normalsize

\\section{{4. Matriz de Riscos}}
{tex_riscos}

\\section{{5. Fontes de Dados e Repositórios}}
{tex_fontes}

\\end{{document}}
"""
        return template_latex

    def exibir_planejar(self):

        st.subheader("Identificação do Problema.")
        titulo = st.text_input("Digite o Titulo do Plano a ser Tratado: ")
        descricao = st.text_area(
            "Descreva o problema, qual o impacto dele e o qual sua atual situação: ")

        # adaptar para dicionario/dataframe "indicadores"
        st.text("Indicadores do Problema e Metas")
        st.caption("Adicione ou remova linhas diretamente na tabela abaixo:")
        indicadores = pd.DataFrame([{
            "Indicador": "Exemplo",
            "Valor Atual": 8.5,
            "Unidade": "%",
            "Meta Esperada": 4.0,
            "Prazo": "30 dias"
        }])
        df_indicadores = st.data_editor(
            indicadores,
            num_rows="dynamic",
            width='stretch',
            key="edit_indic"
        )
        st.divider()

        st.subheader("Análise das Causas.")

        recursos = pd.DataFrame([
            {
                "Categoria": "Técnica",
                "Nome": "Diagrama de Ishikawa",
                "Aplicação/Objetivo": "Mapear causas raiz"
            },
            {
                "Categoria": "Ferramenta",
                "Nome": "Python / Pandas",
                "Aplicação/Objetivo": "Tratamento da base de dados"
            }
        ])

        df_recursos = st.data_editor(
            recursos,
            num_rows="dynamic",
            width='stretch',
            column_config={
                "Categoria": st.column_config.SelectboxColumn(
                    "Categoria",
                    options=[
                        "Técnica",
                        "Ferramenta",
                        "Infraestrutura",
                        "Pessoal"
                    ])},
            key="editor_recursos"
        )

        st.divider()

        st.subheader("Plano de Ação (5W2H)")
        st.caption(
            "Preencha as ações do plano. Crie novas linhas para novas atividades.")

        atividades = pd.DataFrame([
            {
                "O que (What)": "Coletar feedback dos clientes",
                "Por que (Why)": "Entender insatisfação",
                "Quem (Who)": "Equipe de CS",
                "Onde (Where)": "Sistema CRM",
                "Quando (When)": "Semana 1",
                "Como (How)": "Formulário automatizado",
                "Quanto Custa (How Much)": "R$ 0,00"
            }
        ])

        df_5w2h = st.data_editor(
            atividades,
            num_rows="dynamic",
            width='stretch',
            key="editor_5w2h"
        )

        st.divider()

        st.subheader("Matriz de Riscos & Contingência")
        df_riscos_init = pd.DataFrame([
            {"Risco Identificado": "Atraso na entrega dos dados", "Impacto": "Alto",
                "Plano de Mitigação / Ação": "Utilizar base histórica amostral"}
        ])

        df_riscos = st.data_editor(
            df_riscos_init,
            num_rows="dynamic",
            width='stretch',
            column_config={
                "Impacto": st.column_config.SelectboxColumn("Impacto", options=["Baixo", "Médio", "Alto"])
            },
            key="editor_riscos"
        )

        st.divider()

        st.subheader("Fontes de Dados & Repositórios")
        df_fontes_init = pd.DataFrame([
            {"Nome da Fonte": "Kaggle - Customer Churn",
                "Tipo": "Dataset Público", "Link/Endereço": "https://kaggle.com/..."}
        ])

        df_fontes = st.data_editor(
            df_fontes_init,
            num_rows="dynamic",
            width='stretch',
            key="editor_fontes"
        )

        # Montagem do dicionário estruturado
        self.plano["titulo"] = titulo
        self.plano["descricao"] = descricao
        self.plano["indicadores"] = df_indicadores
        self.plano["recursos"] = df_recursos
        self.plano["atividades_5w2h"] = df_5w2h
        self.plano["riscos"] = df_riscos
        self.plano["fontes"] = df_fontes

        st.divider()

        st.subheader("Exportar Planejamento")
        col1, col2 = st.columns(2)

        with col1:
            codigo_tex = self.salvar_plano()
            st.download_button(
                label="Baixar Relatório em LaTex (.tex)",
                data=codigo_tex,
                file_name=f"plano_{
                    datetime.now().strftime('%Y%m%d_%H%M')}.tex",
                mime="text/x-tex",
                key=f"exportar_plano_latex"
            )

            codigo_md = self.salvar_plano_md()
            st.download_button(
                label="Baixar Relatório em Markdown (.md)",
                data=codigo_md,
                file_name=f"plano_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                key=f"exportar_plano_markdown"
            )

        with col2:
            with st.expander("Visualizar Relatório em LaTex"):
                st.code(codigo_tex, language="latex")

            with st.expander("Visualizar Relatório em Markdown"):
                st.markdown(codigo_md)
