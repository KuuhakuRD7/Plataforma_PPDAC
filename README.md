# Plataforma PPDAC

## Estrutura

- ```app.py```
    > Interface Inicial e Chamada das Abas para outras Exibições

- ```uploads/```
    > datasets carregados ou criados irão parar aqui

- ```outputs/```
    > datasets exportados irão parar aqui se não houver escolha do local de download

- ```core/```

    - ```in_data/```

        - ```obtencao.py```
            > funções de carregamento de datasets (Simples, Conjunto e Composto)

        - ```obtencao_ui.py```
            > exibição do menu de criação e de carregamento de datasets

    - ```out_data/```

        - ```exportacao.py```
            > funções de exportação do dataset (csv,excel,latex,json,parquet,zip)

        - ```exportacao_ui.py```
            > exibição do menu de exportação dos datasets

    - ```proc_data/```

        - ```exploracao.py```
            > funções de exploração (tipos, nulidade, estatísticas, linhas, colunas)

        - ```exploracao_ui.py```
            > exibição do menu de exploração

        - ```tratamento.py```
            > funções de tratamento (padronizar, substituir, renomear, limitar, converter)

        - ```tratamento_ui.py```
            > exibição do menu de tratamentos

        - ```analise.py```
            > funções de análise (filtragem, agregação e junção)

        - ```analise_ui.py```
            > exibição do menu de análise

        - ```visulizacao.py```
            > funções de visualização (barras, linhas, area, dispersão,...,mosaico)

        - ```visulizacao_ui.py```
            > exibição do menu de visualização


- ```wiki_data/```

    - ```wikis_ui.py```
        > exibição das páginas de explicação dos módulos

## Módulos da Plataforma

#### Inicio

Tela inicial da aplicação e navegação entre módulos.

#### Obtenção

Responsável pelo carregamento de datasets individuais, conjuntos de arquivos e datasets compostos.

* Importação de arquivos CSV
* Importação de arquivos Excel
* Importação de conjuntos de arquivos
* Carregamento de datasets compostos
* Definição de encoding
* Definição de separadores

#### Exploração

Permite inspecionar estrutura, tipos, nulidade e estatísticas gerais dos dados.

* Visualização de linhas e colunas
* Verificação de tipos
* Estatísticas descritivas
* Verificação de nulidade
* Frequência de valores
* Informações estruturais

#### Tratamento

Responsável pela limpeza, padronização, conversão e transformação dos dados.

* Padronização de colunas
* Conversão numérica
* Conversão de datas
* Renomeação de colunas
* Substituição de valores
* Tratamento de nulos
* Limitação de valores

#### Análise

Permite realizar filtragem, agregação e junção de datasets.

* Filtragem dinâmica
* Agregação de dados
* Operações estatísticas
* Junção de datasets
* Ordenação de resultados
* Top N

#### Visualização

Responsável pela geração de gráficos estatísticos e analíticos.

* Barras
* Linhas
* Área
* Dispersão
* Bolhas
* Pizza
* Boxplot
* Radar
* Waterfall
* Funil
* Sankey
* Mosaico

#### Exportação

Permite exportar datasets tratados e resultados analíticos.

* CSV
* Excel
* JSON
* Parquet
* LaTeX
* ZIP

---

## Fluxo da Plataforma

```text
Obtenção -> Exploração -> Tratamento -> Análise -> Visualização -> Exportação
```

---

## Objetivos do Projeto

* Facilitar manipulação de datasets tabulares
* Centralizar operações analíticas
* Reduzir código repetitivo
* Permitir exploração visual dos dados
* Auxiliar estudos de Ciência de Dados
* Apoiar projetos acadêmicos e experimentais

---

## Condição para uso


| **Interface** | **Operações e Tratamentos** | **Reconhecer Arquivos** | **Reconhecer Arquivos** | **Plotagem de Dados** |
|:-------------:|:---------------------------:|:-----------------------:|:-----------------------:|:---------------------:|
|   streamlit   |            pandas           |         openpyxl        |         pathlib         |       matplotlib      |
|               |            numpy            |          odfpy          |          shutil         |         plotly        |
|               |              re             |        xlsxwriter       |         zipfile         |        seaborn        |
|               |                             |                         |           io            |                       |


### Instalar bibliotecas
> ```pip install -r requirements.txt```

---

## Uso

### Executar

> ```source ~/<ambiente_venv>/bin/activate```

> ```streamlit run app.py --server.maxUploadSize=<Tamanho_em_MegaBytes>```

### Exemplo:

> ```source ~/meu_venv/bin/activate```

> ```streamlit run app.py --server.maxUploadSize=200```

### Sair
> ```Ctrl-C```

---

## Módulos Futuros

- Geração de Relatórios (Informações da Exploração)
- Análise de Estatísticas (Insights)
- Geração de SQL (Criação de Tabelas)
