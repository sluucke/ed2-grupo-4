import spacy
from spacy.lang.pt.stop_words import STOP_WORDS

_nlp = spacy.blank("pt")
_nlp.add_pipe("sentencizer")

_PLURAL = [
    ("ns", 1, "m"),
    ("ões", 3, "ão"),
    ("ães", 3, "ão"),
    ("ais", 3, "al"),
    ("éis", 3, "el"),
    ("eis", 3, "el"),
    ("óis", 3, "ol"),
    ("is", 2, "il"),
    ("es", 3, ""),
    ("s", 3, ""),
]

_FEMININE = [
    ("ona", 3, "ão"),
    ("ã", 2, "ão"),
    ("a", 3, "o"),
]

_AUGDIM = [
    ("zíssimo", 2, ""),
    ("íssimo", 3, ""),
    ("zinhos", 2, ""),
    ("zinhas", 2, ""),
    ("zinho", 2, ""),
    ("zinha", 2, ""),
    ("inhos", 3, ""),
    ("inhas", 3, ""),
    ("inho", 3, ""),
    ("inha", 3, ""),
    ("zão", 2, ""),
]

_ADVERB = [
    ("mente", 4, ""),
]

_NOUN = [
    ("abilidade", 3, ""),
    ("icidade", 3, ""),
    ("ividade", 3, ""),
    ("izações", 3, ""),
    ("ização", 3, ""),
    ("imentos", 3, ""),
    ("imento", 3, ""),
    ("âncias", 3, ""),
    ("ências", 3, ""),
    ("mentos", 3, ""),
    ("idades", 3, ""),
    ("ismos", 3, ""),
    ("istas", 3, ""),
    ("dades", 3, ""),
    ("turas", 3, ""),
    ("ância", 3, ""),
    ("ência", 3, ""),
    ("mento", 3, ""),
    ("idade", 3, ""),
    ("ções", 3, ""),
    ("ores", 3, ""),
    ("ismo", 3, ""),
    ("ista", 3, ""),
    ("ados", 3, ""),
    ("adas", 3, ""),
    ("osos", 3, ""),
    ("osas", 3, ""),
    ("ivos", 3, ""),
    ("ivas", 3, ""),
    ("icos", 3, ""),
    ("icas", 3, ""),
    ("dade", 3, ""),
    ("tura", 3, ""),
    ("uras", 3, ""),
    ("ção", 3, ""),
    ("ura", 3, ""),
    ("oso", 3, ""),
    ("osa", 3, ""),
    ("ivo", 3, ""),
    ("iva", 3, ""),
    ("ico", 3, ""),
    ("ica", 3, ""),
    ("ado", 3, ""),
    ("ada", 3, ""),
    ("or", 3, ""),
]

_VERB = [
    ("aríamos", 2, ""),
    ("eríamos", 2, ""),
    ("iríamos", 2, ""),
    ("ássemos", 2, ""),
    ("êssemos", 2, ""),
    ("íssemos", 2, ""),
    ("aremos", 2, ""),
    ("eremos", 2, ""),
    ("iremos", 2, ""),
    ("ávamos", 2, ""),
    ("áramos", 2, ""),
    ("éramos", 2, ""),
    ("íramos", 2, ""),
    ("assem", 2, ""),
    ("essem", 2, ""),
    ("issem", 2, ""),
    ("ariam", 2, ""),
    ("eriam", 2, ""),
    ("iriam", 2, ""),
    ("arão", 2, ""),
    ("erão", 2, ""),
    ("irão", 2, ""),
    ("aram", 2, ""),
    ("eram", 2, ""),
    ("iram", 2, ""),
    ("avam", 2, ""),
    ("ando", 2, ""),
    ("endo", 2, ""),
    ("indo", 2, ""),
    ("asse", 2, ""),
    ("esse", 2, ""),
    ("isse", 2, ""),
    ("aste", 2, ""),
    ("este", 2, ""),
    ("iste", 2, ""),
    ("ares", 2, ""),
    ("eres", 2, ""),
    ("ires", 2, ""),
    ("avas", 2, ""),
    ("ados", 2, ""),
    ("idas", 2, ""),
    ("idos", 2, ""),
    ("adas", 2, ""),
    ("aria", 2, ""),
    ("eria", 2, ""),
    ("iria", 2, ""),
    ("ava", 2, ""),
    ("iam", 2, ""),
    ("ido", 2, ""),
    ("ida", 2, ""),
    ("ar", 2, ""),
    ("er", 2, ""),
    ("ir", 2, ""),
    ("ou", 2, ""),
    ("eu", 2, ""),
    ("iu", 2, ""),
    ("am", 2, ""),
    ("em", 2, ""),
]

_VOWEL = [
    ("os", 3, ""),
    ("as", 3, ""),
    ("a", 3, ""),
    ("e", 3, ""),
    ("o", 3, ""),
]


def _apply_step(word: str, rules: list) -> str:
    best_len = 0
    result = word
    for suffix, min_stem, replacement in rules:
        if word.endswith(suffix):
            stem_len = len(word) - len(suffix)
            if stem_len >= min_stem and len(suffix) > best_len:
                best_len = len(suffix)
                result = word[:stem_len] + replacement
    return result


def split_sentences(text: str) -> list[str]:
    doc = _nlp(text.strip())
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]


def tokenize(sentence: str) -> list[str]:
    doc = _nlp.tokenizer(sentence.lower())
    return [token.text for token in doc if token.is_alpha]


def remove_stopwords(tokens: list[str]) -> list[str]:
    return [t for t in tokens if t not in STOP_WORDS]


def stem(word: str) -> str:
    word = _apply_step(word, _PLURAL)
    word = _apply_step(word, _FEMININE)
    word = _apply_step(word, _AUGDIM)
    word = _apply_step(word, _ADVERB)
    word = _apply_step(word, _NOUN)
    word = _apply_step(word, _VERB)
    word = _apply_step(word, _VOWEL)
    return word


def preprocess_text(text) -> str:
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = [stem(t) for t in tokens]
    return " ".join(tokens)
