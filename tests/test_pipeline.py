import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.pipeline import generate_title

ARTIGO = """
O Brasil registrou recorde de exportações em maio. O agronegócio liderou os
resultados, com destaque para a soja e o milho. A balança comercial fechou com
superávit de R$ 12 bilhões. Analistas apontam o câmbio favorável como fator
principal. O setor industrial também apresentou crescimento moderado.
""".strip()


def test_generate_title_returns_string():
    result = generate_title(ARTIGO)
    assert isinstance(result["title"], str)
    assert len(result["title"]) > 0


def test_generate_title_has_expected_keys():
    result = generate_title(ARTIGO)
    for key in ("title", "best_idx", "scores", "stats", "sentences"):
        assert key in result


def test_generate_title_word_count():
    result = generate_title(ARTIGO)
    words = result["title"].split()
    # título nunca deve ter mais de 20 palavras após a heurística
    assert len(words) <= 20


def test_generate_title_empty_text():
    result = generate_title("")
    assert result["title"] == ""


def test_generate_title_single_sentence():
    result = generate_title("Brasil exporta soja para a China e Europa com recorde histórico em 2026.")
    assert isinstance(result["title"], str)
