"""
Módulo TextRank — adaptação do PageRank para ranqueamento de frases.

Fórmula:
    WS(Vi) = (1 - d) + d × Σj [ wji / Σk wjk × WS(Vj) ]

    d       = fator de amortecimento (0.85)
    wji     = peso da aresta entre Vj e Vi
    Σk wjk  = soma dos pesos de todas as arestas de Vj

O algoritmo itera até convergência (delta < epsilon) ou max_iter iterações.
Heap (heapq) é usado para extração eficiente das top-K frases — O(k log n).
"""

import heapq


DAMPING = 0.85
MAX_ITER = 100
EPSILON = 1e-4


def textrank(matrix: list[list[float]]) -> list[float]:
    """
    Executa o TextRank sobre a matriz de adjacência.

    Returns:
        scores: lista de scores (paralela às frases)
    """
    n = len(matrix)
    if n == 0:
        return []

    scores = [1.0 / n] * n

    # pré-calcula soma dos pesos de cada nó (denominador)
    out_weights = [sum(matrix[i]) for i in range(n)]

    for _ in range(MAX_ITER):
        new_scores = [0.0] * n

        for i in range(n):
            incoming = 0.0
            for j in range(n):
                if matrix[j][i] > 0 and out_weights[j] > 0:
                    incoming += (matrix[j][i] / out_weights[j]) * scores[j]
            new_scores[i] = (1 - DAMPING) + DAMPING * incoming

        # verifica convergência
        delta = sum(abs(new_scores[i] - scores[i]) for i in range(n))
        scores = new_scores

        if delta < EPSILON:
            break

    return scores


def top_k_sentences(scores: list[float], k: int = 3) -> list[tuple[float, int]]:
    """
    Retorna os índices das k frases com maior score.
    Usa heap para extração eficiente — O(k log n).

    Returns:
        lista de (score, índice) ordenada por score decrescente
    """
    heap = [(-score, idx) for idx, score in enumerate(scores)]
    heapq.heapify(heap)

    result = []
    for _ in range(min(k, len(heap))):
        neg_score, idx = heapq.heappop(heap)
        result.append((-neg_score, idx))

    return result


def best_sentence_index(scores: list[float]) -> int:
    """Retorna o índice da frase com maior score."""
    top = top_k_sentences(scores, k=1)
    return top[0][1] if top else 0
