# ED2 · Grupo 4 · UnB — Geração Automática de Títulos de Notícias

Sistema de sumarização extrativa baseado em grafos para geração automática de títulos de artigos jornalísticos.

## Como funciona

```
Texto → Frases → Stopwords + Stemming → Grafo de Similaridade → TextRank → Heurística → Título
```

1. **Pré-processamento** — segmenta o texto em frases, remove stopwords (PT-BR), aplica stemming RSLP
2. **Grafo** — frases = vértices; peso da aresta = palavras em comum normalizadas por log(tamanho)
3. **TextRank** — variante do PageRank que ranqueia as frases por importância estrutural
4. **Heurística** — ajusta o comprimento do título (≤5 / 5–20 / >20 palavras)

## Instalação

```bash
pip install nltk
python main.py            # roda o exemplo embutido
python main.py artigo.txt # processa um arquivo
```

## Estrutura

```
src/
  preprocessor.py   — tokenização, stopwords, stemming
  graph.py          — matriz de adjacência, similaridade
  textrank.py       — algoritmo PageRank/TextRank + heap
  heuristic.py      — heurística de comprimento do título
  pipeline.py       — orquestrador principal

scripts/
  download_dataset.py — gera artigos de desenvolvimento (JSON + .txt)
  evaluate.py         — calcula ROUGE-1 sobre os artigos

tests/                — 22 testes unitários (pytest)
data/raw/             — artigos de entrada
```

## Avaliação

```bash
python scripts/download_dataset.py   # gera os artigos de teste
python scripts/evaluate.py           # ROUGE-1 F1 médio
```

ROUGE-1 F1 médio obtido nos artigos LLM: **0.439**

## Dataset

- **LLM-generated (PT-BR):** 5 artigos gerados em `data/raw/`
- **CSTNews:** corpus acadêmico NILC/USP com notícias PT-BR — baixe em http://nilc.icmc.usp.br/CSTNews/login e coloque em `data/raw/cstnews/`

## Integrantes

| Nome | Módulo |
|------|--------|
| Pessoa 1 | `src/preprocessor.py` |
| Pessoa 2 | `src/graph.py` |
| Pessoa 3 | `src/textrank.py` |
| Pessoa 4 | `src/heuristic.py` + `src/pipeline.py` |
| Pessoa 5 | `scripts/evaluate.py` + análise de resultados |
