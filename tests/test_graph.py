from src.graph import _similarity, build_graph, graph_stats


# ── _similarity ──────────────────────────────────────────────

def test_similaridade_frases_identicas_maior_que_zero():
    sim = _similarity(["brasil", "economia"], ["brasil", "economia"])
    assert sim > 0.0


def test_similaridade_e_simetrica():
    a = ["brasil", "economia", "selic"]
    b = ["economia", "selic", "juros"]
    assert _similarity(a, b) == _similarity(b, a)


# ── build_graph ──────────────────────────────────────────────

def test_grafo_e_simetrico_com_diagonal_zero():
    processed = [
        ["brasil", "economia"],
        ["economia", "selic"],
        ["futebol", "campeonato"],
    ]
    matrix = build_graph(processed, threshold=0.1)
    n = len(processed)
    for i in range(n):
        assert matrix[i][i] == 0.0
        for j in range(n):
            assert matrix[i][j] == matrix[j][i]


def test_grafo_mantem_aresta_acima_do_threshold():
    processed = [
        ["brasil", "economia", "selic"],
        ["brasil", "economia", "juros"],
    ]
    matrix = build_graph(processed, threshold=0.1)
    assert matrix[0][1] > 0.0
    assert matrix[0][1] == matrix[1][0]


# ── graph_stats ──────────────────────────────────────────────

def test_estatisticas_conta_nodes_edges_e_grau_medio():
    matrix = [
        [0.0, 0.5, 0.0],
        [0.5, 0.0, 0.3],
        [0.0, 0.3, 0.0],
    ]
    stats = graph_stats(matrix)
    assert stats["nodes"] == 3
    assert stats["edges"] == 2
    assert stats["avg_degree"] == 4 / 3
