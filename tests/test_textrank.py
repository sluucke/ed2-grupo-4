import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.textrank import textrank, top_k_sentences, best_sentence_index


def _symmetric_matrix(n, val=0.5):
    m = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                m[i][j] = val
    return m


def test_textrank_returns_n_scores():
    matrix = _symmetric_matrix(4)
    scores = textrank(matrix)
    assert len(scores) == 4


def test_textrank_scores_positive():
    matrix = _symmetric_matrix(3)
    scores = textrank(matrix)
    assert all(s > 0 for s in scores)


def test_textrank_empty():
    assert textrank([]) == []


def test_top_k_sentences_length():
    scores = [0.1, 0.5, 0.3, 0.9, 0.2]
    top = top_k_sentences(scores, k=3)
    assert len(top) == 3


def test_top_k_sentences_ordered():
    scores = [0.1, 0.5, 0.3, 0.9, 0.2]
    top = top_k_sentences(scores, k=3)
    values = [s for s, _ in top]
    assert values == sorted(values, reverse=True)


def test_best_sentence_index():
    scores = [0.1, 0.9, 0.3]
    assert best_sentence_index(scores) == 1
