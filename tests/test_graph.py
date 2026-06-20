import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.graph import build_graph, graph_stats, _similarity


def test_similarity_identical():
    a = ["export", "soj", "brasil"]
    assert _similarity(a, a) > 0


def test_similarity_disjoint():
    a = ["export", "soj"]
    b = ["câmbio", "dólar"]
    assert _similarity(a, b) == 0.0


def test_similarity_symmetry():
    a = ["export", "soj", "brasil"]
    b = ["brasil", "câmbio"]
    assert _similarity(a, b) == _similarity(b, a)


def test_build_graph_shape():
    processed = [["export", "soj"], ["soj", "brasil"], ["câmbio", "dólar"]]
    matrix = build_graph(processed, threshold=0.0)
    n = len(processed)
    assert len(matrix) == n
    assert all(len(row) == n for row in matrix)


def test_build_graph_symmetric():
    processed = [["a", "b", "c"], ["b", "c", "d"], ["e", "f"]]
    matrix = build_graph(processed, threshold=0.0)
    n = len(processed)
    for i in range(n):
        for j in range(n):
            assert matrix[i][j] == matrix[j][i]


def test_graph_stats():
    processed = [["a", "b"], ["b", "c"], ["x", "y"]]
    matrix = build_graph(processed, threshold=0.0)
    stats = graph_stats(matrix)
    assert stats["nodes"] == 3
    assert stats["edges"] >= 1
