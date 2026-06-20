"""
Módulo de construção do grafo de similaridade.

Vértices  → frases do texto
Arestas   → similaridade por palavras em comum (após stopwords + stemming)
Peso      → |A ∩ B| / (log|A| + log|B|)   (normalizado pelo tamanho das frases)
Tipo      → não-direcionado e ponderado

Representação interna: matriz de adjacência (lista de listas).
"""

import math


def _similarity(stems_a: list[str], stems_b: list[str]) -> float:
    """
    Calcula a similaridade entre duas frases pelo número de stems comuns,
    normalizado pela soma dos logaritmos dos tamanhos.
    Retorna 0 se alguma das frases estiver vazia ou se a interseção for vazia.
    """
    if not stems_a or not stems_b:
        return 0.0

    set_a = set(stems_a)
    set_b = set(stems_b)
    common = len(set_a & set_b)

    if common == 0:
        return 0.0

    denom = math.log(len(stems_a) + 1) + math.log(len(stems_b) + 1)
    return common / denom if denom > 0 else 0.0


def build_graph(processed_sentences: list[list[str]], threshold: float = 0.1) -> list[list[float]]:
    """
    Constrói a matriz de adjacência do grafo de similaridade.

    Args:
        processed_sentences: lista de listas de stems (saída do preprocessor)
        threshold: arestas com peso abaixo desse valor são descartadas

    Returns:
        matrix: lista de listas (n×n) com os pesos das arestas
    """
    n = len(processed_sentences)
    matrix: list[list[float]] = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            sim = _similarity(processed_sentences[i], processed_sentences[j])
            if sim >= threshold:
                matrix[i][j] = sim
                matrix[j][i] = sim

    return matrix


def graph_stats(matrix: list[list[float]]) -> dict:
    """Retorna estatísticas básicas do grafo (nós, arestas, grau médio)."""
    n = len(matrix)
    edges = sum(1 for i in range(n) for j in range(i + 1, n) if matrix[i][j] > 0)
    degrees = [sum(1 for w in row if w > 0) for row in matrix]
    avg_degree = sum(degrees) / n if n > 0 else 0
    return {"nodes": n, "edges": edges, "avg_degree": round(avg_degree, 2)}
