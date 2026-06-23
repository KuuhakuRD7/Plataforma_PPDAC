# Exploração de Dados

A etapa de exploração é responsável por compreender a estrutura, qualidade e comportamento dos dados antes de qualquer transformação ou análise avançada.

O objetivo principal é responder perguntas como:

- Quais colunas existem?
- Quais são os tipos dos dados?
- Existem valores nulos?
- Existem padrões ou inconsistências?
- Como os dados estão distribuídos?

---

#  Principais análises disponíveis

## Tipos de Dados

Permite identificar o tipo de cada coluna:

- Texto (`object/string`)
- Numérico (`int`, `float`)
- Datas (`datetime`)
- Booleanos (`bool`)

Isso ajuda a:
- Escolher visualizações corretas
- Detectar colunas mal formatadas
- Planejar conversões

---

## Valores Nulos

Mostra a quantidade de dados ausentes por coluna.

Útil para:
- Detectar problemas de qualidade
- Decidir estratégias de limpeza
- Avaliar completude do dataset

---

## Resumo Estatístico

Apresenta métricas importantes como:

- Média
- Mediana
- Moda
- Desvio padrão
- Valor mínimo
- Valor máximo

Melhor para:
- Entender distribuição dos dados
- Detectar outliers
- Comparar variáveis numéricas

---

## Frequência de Valores

Mostra a ocorrência de categorias ou valores únicos.

Melhor para:
- Dados categóricos
- Análise de classes
- Verificar balanceamento

Exemplos:
- Quantidade por município
- Frequência de categorias
- Distribuição de crimes

---

# Quando usar exploração?

Use a exploração sempre:

- Antes da limpeza
- Antes da modelagem
- Antes da visualização
- Antes da análise estatística
- Antes de Machine Learning

---

# Objetivo da Exploração

A exploração transforma dados desconhecidos em dados compreendidos.

Ela ajuda a:

- Encontrar erros
- Descobrir padrões
- Identificar inconsistências
- Entender relações
- Guiar decisões analíticas

---

#  Boas práticas

- Analise os tipos de dados
- Verifique valores nulos
- Procure valores extremos
- Entenda a distribuição
- Identifique colunas importantes
- Observe padrões e anomalias
