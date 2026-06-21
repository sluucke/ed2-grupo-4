import heapq

DAMPING  = 0.85
MAX_ITER = 100
EPSILON  = 1e-4 

def textrank(matrix: list[list[float]]) -> list[float]:
   
    n = len(matrix)
    if n == 0:
        return []

    scores = [1.0 / n] * n

    out_weights = [sum(row) for row in matrix]

    for _ in range(MAX_ITER):
        new_scores = [0.0] * n

        for i in range(n):
            soma = 0.0
            for j in range(n):
                if matrix[j][i] > 0 and out_weights[j] > 0:
                    soma += (matrix[j][i] / out_weights[j]) * scores[j]
            new_scores[i] = (1 - DAMPING) + DAMPING * soma

        delta = sum(abs(new_scores[i] - scores[i]) for i in range(n))
        scores = new_scores

        if delta < EPSILON:
            break

    return scores


def top_k_sentences(scores: list[float], k: int = 3) -> list[tuple[float, int]]:

    if not scores:
        return []

    heap = [(-s, i) for i, s in enumerate(scores)]
    heapq.heapify(heap)

    result = []
    for _ in range(min(k, len(heap))):
        neg_s, i = heapq.heappop(heap)
        result.append((-neg_s, i))

    return result


def best_sentence_index(scores: list[float]) -> int:
    top = top_k_sentences(scores, k=1)
    return top[0][1] if top else -1