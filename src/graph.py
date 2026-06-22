import math


def _similarity(stems_a: list[str], stems_b: list[str]) -> float:
    # similaridade = stems em comum / soma dos logaritmos dos tamanhos das frases
    if not stems_a or not stems_b:
        return 0.0
    common = len(set(stems_a) & set(stems_b))
    if common == 0:
        return 0.0
    return common / (math.log(len(stems_a) + 1) + math.log(len(stems_b) + 1))


def build_graph(processed: list[list[str]], threshold: float = 0.1) -> list[list[float]]:
    # matriz de adjacência n x n, grafo não-direcionado, arestas abaixo do threshold descartadas
    n = len(processed)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            sim = _similarity(processed[i], processed[j])
            if sim >= threshold:
                matrix[i][j] = sim
                matrix[j][i] = sim
    return matrix


def graph_stats(matrix: list[list[float]]) -> dict:
    '''
        exemplo de retorno:
        {
            "nodes": 20,
            "edges": 50,
            "avg_degree": 5.0
        }
    '''
    n = len(matrix)
    edges = sum(1 for i in range(n) for j in range(i + 1, n) if matrix[i][j] > 0)
    avg_degree = (2 * edges / n) if n > 0 else 0.0
    return {
        "nodes": n,
        "edges": edges,
        "avg_degree": avg_degree,
    }