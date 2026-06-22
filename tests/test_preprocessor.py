import pytest
from src.preprocessor import (
    preprocess_text,
    remove_stopwords,
    split_sentences,
    stem,
    tokenize,
)


class TestSplitSentences:
    def test_single_sentence(self):
        result = split_sentences("O gato está dormindo.")
        assert result == ["O gato está dormindo."]

    def test_multiple_sentences(self):
        result = split_sentences("O gato dorme. O cachorro late.")
        assert len(result) == 2
        assert result[0] == "O gato dorme."
        assert result[1] == "O cachorro late."

    def test_strips_surrounding_whitespace(self):
        result = split_sentences("  Frase com espaços.  ")
        assert result == ["Frase com espaços."]

    def test_empty_string(self):
        assert split_sentences("") == []


class TestTokenize:
    def test_lowercases(self):
        assert "brasil" in tokenize("Brasil")

    def test_removes_punctuation(self):
        tokens = tokenize("Olá, mundo!")
        assert "," not in tokens
        assert "!" not in tokens

    def test_removes_numbers(self):
        assert "2024" not in tokenize("O ano 2024 foi importante")

    def test_all_tokens_are_alpha(self):
        tokens = tokenize("texto, com 42 símbolos @ e pontos.")
        assert all(t.isalpha() for t in tokens)

    def test_empty_string(self):
        assert tokenize("") == []


class TestRemoveStopwords:
    def test_removes_common_stopwords(self):
        stopwords = ["de", "a", "o", "que", "e", "para", "com"]
        result = remove_stopwords(stopwords)
        assert result == []

    def test_keeps_content_words(self):
        tokens = ["casa", "cachorro", "computador"]
        assert remove_stopwords(tokens) == tokens

    def test_mixed_list(self):
        tokens = ["de", "casa", "para", "cachorro"]
        result = remove_stopwords(tokens)
        assert "de" not in result
        assert "para" not in result
        assert "casa" in result
        assert "cachorro" in result

    def test_empty_list(self):
        assert remove_stopwords([]) == []


class TestStem:
    def test_returns_string(self):
        assert isinstance(stem("computadores"), str)

    def test_non_empty_for_normal_word(self):
        assert stem("programação") != ""

    def test_is_deterministic(self):
        assert stem("correndo") == stem("correndo")

    def test_normalizes_plural_to_same_root_as_singular(self):
        # RSLP should map plural and singular to the same stem
        assert stem("gatos") == stem("gato")

    def test_normalizes_verb_forms_to_same_root(self):
        # gerund and infinitive should share the same stem
        assert stem("correndo") == stem("correr")


class TestPreprocessText:
    def test_returns_tuple_of_two_lists(self):
        sentences, processed = preprocess_text("O Brasil é um país grande.")
        assert isinstance(sentences, list)
        assert isinstance(processed, list)

    def test_sentences_and_processed_same_length(self):
        sentences, processed = preprocess_text("O gato dorme. O cachorro late.")
        assert len(sentences) == len(processed)

    def test_processed_contains_stems(self):
        sentences, processed = preprocess_text("Computadores modernos processam dados.")
        assert len(processed) == 1
        assert len(processed[0]) > 0
        assert all(isinstance(s, str) for s in processed[0])

    def test_empty_string(self):
        sentences, processed = preprocess_text("")
        assert sentences == []
        assert processed == []

    def test_stopwords_removed_from_processed(self):
        _, processed = preprocess_text("O Brasil exportou soja para a China.")
        all_stems = processed[0]
        assert "o" not in all_stems
        assert "para" not in all_stems
        assert "a" not in all_stems
