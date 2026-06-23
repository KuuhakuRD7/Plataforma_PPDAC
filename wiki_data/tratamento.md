
# Tratamento de Dados

A etapa de tratamento é responsável por limpar, corrigir e padronizar os dados para garantir qualidade e consistência analítica.

Dados brutos frequentemente possuem:

- Valores inválidos
- Campos vazios
- Erros de digitação
- Tipos incorretos
- Inconsistências
- Duplicidades

O tratamento prepara os dados para análise e visualização.

---

# Principais operações de tratamento

## Limpeza de Colunas

Padroniza nomes de colunas:

- Remove espaços
- Remove acentos
- Converte para maiúsculo
- Substitui espaços por "_"

Exemplo:

"Município Nome" → "MUNICIPIO_NOME"

Melhor para:

- Padronização
- Compatibilidade entre datasets
- Evitar erros futuros

## Conversão Numérica

Transforma textos em números válidos.

Exemplos:

"1.234,50" → 1234.50

"10" → 10

Melhor para:

- Cálculos
- Estatísticas
- Gráficos

## Conversão de Datas

Converte textos para formato de data.

Exemplos:

"2024-01-01"

"01/01/2024"

Melhor para:

- Séries temporais
- Agrupamentos por período
- Análises históricas

## Tratamento de Valores Nulos

Permite:

- Remover linhas vazias
- Preencher dados ausentes

## Substituir valores inválidos

Melhor para:

- Melhorar qualidade do dataset
- Evitar erros em gráficos e modelos

## Substituição de Valores

Padroniza categorias ou corrige inconsistências.

Exemplos:

"Masc", "M" → "Masculino"

"Belém ", "Belem" → "BELÉM"

## Aplicação de Limites

Remove ou invalida valores fora de intervalos aceitáveis.

Exemplos:

- Idade negativa
- Temperaturas impossíveis
- Valores financeiros inválidos

---

# Por que tratar os dados?

Dados incorretos geram:

-  gráficos errados
-  estatísticas incorretas
-  análises enganosas
-  modelos ruins

# Objetivo do Tratamento

Transformar dados brutos em dados confiáveis.

#  Boas práticas

- Padronize nomes de colunas
- Corrija tipos de dados
- Trate valores nulos
- Detecte inconsistências
- Remova valores inválidos
- Documente transformações

