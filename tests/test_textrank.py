import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.textrank import textrank, top_k_sentences, best_sentence_index


# ── textrank ──────────────────────────────────────────────────

def test_textrank_lista_vazia():
    assert textrank([]) == []


def test_textrank_scores_positivos():
    matrix = [
        [0.0, 0.5, 0.3],
        [0.5, 0.0, 0.8],
        [0.3, 0.8, 0.0],
    ]
    scores = textrank(matrix)
    assert len(scores) == 3
    assert all(s > 0 for s in scores)


def test_textrank_no_mais_conectado_tem_score_maior():
    matrix = [
        [0.0, 1.0, 1.0],
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
    ]
    scores = textrank(matrix)
    assert scores[0] > scores[1]
    assert scores[0] > scores[2]


def test_textrank_grafo_completo_scores_iguais():
    n = 4
    matrix = [[1.0 if i != j else 0.0 for j in range(n)] for i in range(n)]
    scores = textrank(matrix)
    assert max(scores) - min(scores) < 1e-3


# ── top_k_sentences ───────────────────────────────────────────

def test_top_k_lista_vazia():
    assert top_k_sentences([], k=3) == []


def test_top_k_retorna_k_tuplas_ordenadas():
    scores = [0.1, 0.9, 0.5, 0.3]
    result = top_k_sentences(scores, k=3)
    assert len(result) == 3
    assert result[0] == (0.9, 1)
    assert result[1] == (0.5, 2)
    assert result[2] == (0.3, 3)


def test_top_k_com_k_maior_que_n_retorna_todos():
    scores = [0.3, 0.7, 0.5]
    result = top_k_sentences(scores, k=10)
    assert len(result) == 3


# ── best_sentence_index ───────────────────────────────────────

def test_best_index_lista_vazia():
    assert best_sentence_index([]) == -1


def test_best_index_retorna_indice_correto():
    scores = [0.1, 0.5, 0.9, 0.3]
    assert best_sentence_index(scores) == 2


def test_best_index_retorna_inteiro():
    assert isinstance(best_sentence_index([0.3, 0.8, 0.5]), int)