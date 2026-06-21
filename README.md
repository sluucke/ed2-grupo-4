# ED2 · Grupo 4 · UnB — Geração Automática de Títulos de Notícias

Sistema de sumarização extrativa baseado em grafos para geração automática de títulos de artigos jornalísticos.

## Como funciona

```
Texto → Frases → Stopwords + Stemming → Grafo de Similaridade → TextRank → Heurística → Título
```

1. **Pré-processamento** — segmenta o texto em frases, remove stopwords (PT-BR via spaCy), aplica stemmer implementado manualmente
2. **Grafo** — frases = vértices; peso da aresta = número de palavras em comum após pré-processamento
3. **TextRank** — variante do PageRank implementada do zero que ranqueia as frases por importância estrutural
4. **Heurística** — ajusta o comprimento do título (≤5 / 5–20 / >20 palavras)

## Instalação

```bash
pip install -r requirements.txt
python main.py
```

## Estrutura

```
src/
  preprocessor.py   — tokenização, stopwords (spaCy), stemmer manual
  graph.py          — matriz de adjacência, similaridade por palavras em comum
  textrank.py       — algoritmo TextRank do zero + heap para top-K frases
  heuristic.py      — heurística de comprimento do título
  pipeline.py       — orquestrador principal

scripts/
  download_dataset.py — gera os artigos de desenvolvimento (JSON + .txt)
  evaluate.py         — calcula ROUGE-1 implementado do zero

tests/              — testes unitários (pytest)
data/raw/pt/        — 20 artigos PT-BR gerados por LLM (5 editorias)
```

## Dataset

20 artigos em PT-BR gerados por LLM, distribuídos em 5 editorias:
economia, política, esportes, tecnologia e saúde.

Para gerar os arquivos localmente:

```bash
python scripts/download_dataset.py --ptonly
```

## Avaliação

```bash
python scripts/evaluate.py
```

## Integrantes

| Nome | Módulo |
|------|--------|
| Pessoa 1 | `src/preprocessor.py` |
| Pessoa 2 | `src/graph.py` |
| Pessoa 3 | `src/textrank.py` |
| Pessoa 4 | `src/heuristic.py` + `src/pipeline.py` + `main.py` |
| Pessoa 5 | `scripts/evaluate.py` + análise de resultados |
