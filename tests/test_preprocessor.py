import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.preprocessor import split_sentences, tokenize, remove_stopwords, stem_tokens, preprocess_text


def test_split_sentences():
    text = "O Brasil exportou soja. A balança comercial fechou positiva. Analistas comemoram."
    sentences = split_sentences(text)
    assert len(sentences) == 3


def test_tokenize_removes_punctuation():
    tokens = tokenize("Olá, mundo! Teste 123.")
    assert "," not in tokens
    assert "123" not in tokens
    assert "olá" in tokens


def test_remove_stopwords():
    tokens = ["o", "brasil", "exportou", "a", "soja"]
    result = remove_stopwords(tokens)
    assert "o" not in result
    assert "a" not in result
    assert "brasil" in result


def test_stem_tokens():
    tokens = ["exportações", "exportou", "liderança"]
    stems = stem_tokens(tokens)
    # RSLP deve reduzir exportações e exportou ao mesmo radical
    assert stems[0] == stems[1]


def test_preprocess_text_returns_parallel_lists():
    text = "O agronegócio liderou os resultados. A soja foi destaque nas exportações."
    sentences, processed = preprocess_text(text)
    assert len(sentences) == len(processed)
    assert all(isinstance(p, list) for p in processed)
