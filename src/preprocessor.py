import nltk
import spacy
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

nltk.download("stopwords", quiet=True)
nltk.download("rslp", quiet=True)

_nlp = spacy.blank("pt")
_nlp.add_pipe("sentencizer")

_STOP_WORDS = set(stopwords.words("portuguese"))
_stemmer = RSLPStemmer()


def split_sentences(text: str) -> list[str]:
    doc = _nlp(text.strip())
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]


def tokenize(sentence: str) -> list[str]:
    doc = _nlp.tokenizer(sentence.lower())
    return [token.text for token in doc if token.is_alpha]


def remove_stopwords(tokens: list[str]) -> list[str]:
    return [t for t in tokens if t not in _STOP_WORDS]


def stem(word: str) -> str:
    return _stemmer.stem(word)


def preprocess_sentence(sentence: str) -> list[str]:
    tokens = tokenize(sentence)
    tokens = remove_stopwords(tokens)
    return [stem(t) for t in tokens]


def preprocess_text(text: str) -> tuple[list[str], list[list[str]]]:
    sentences = split_sentences(text)
    processed = [preprocess_sentence(s) for s in sentences]
    return sentences, processed
