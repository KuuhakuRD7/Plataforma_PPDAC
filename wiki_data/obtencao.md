
# Obtenção de Dados

A etapa de obtenção é responsável por carregar datasets para o ambiente analítico.

Os dados podem vir de diferentes fontes e formatos, como:

- CSV
- ZIP
- Conjuntos de arquivos
- Bases compostas

---

# Tipos de carregamento

## Simples

Carrega um único dataset.

Melhor para:
- Arquivos CSV únicos
- Bases pequenas
- Dados isolados

---

## Conjunto

Carrega múltiplos arquivos relacionados pertencentes ao mesmo dataset.

Melhor para:
- Dados particionados
- Bases divididas por ano ou região

---

## Composto

Carrega múltiplos datasets independentes.

Melhor para:
- Projetos com várias tabelas
- Integração de diferentes fontes

---

#  Configurações de Importação

## Separador CSV

Define como os dados estão separados:

- `,`
- `;`
- `|`

---

## Codificação

Define o padrão de caracteres utilizado.

Exemplos:
- UTF-8
- Latin1
- CP1252

Importante para:
- Acentuação
- Caracteres especiais
- Compatibilidade

---

# Problemas comuns na importação

- Colunas quebradas
- Caracteres estranhos
- Separadores incorretos
- Datas mal interpretadas
- Tipos incorretos

---

# Objetivo da Obtenção

Garantir que os dados sejam carregados corretamente antes do processamento.

---

#  Boas práticas

- Verifique encoding
- Confirme separadores
- Analise tipos de dados
- Padronize datasets
- Organize arquivos por projeto

