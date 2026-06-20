"""
Módulo de pré-processamento textual.

Responsável por:
- Segmentar texto em frases
- Tokenizar frases em palavras
- Remover stopwords em português
- Aplicar stemming (RSLP)
"""

import re
import ssl
import nltk
from nltk.stem import RSLPStemmer

# macOS pode ter SSL sem certificados de CA; ignora para baixar os dados do NLTK
_ctx = ssl._create_unverified_context
ssl._create_default_https_context = _ctx

nltk.download("rslp", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

ssl._create_default_https_context = ssl.create_default_context

STOPWORDS_PT = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas",
    "ao", "aos", "à", "às", "pelo", "pela", "pelos", "pelas",
    "por", "para", "com", "sem", "sob", "sobre", "entre", "até",
    "que", "se", "mas", "ou", "e", "nem", "porém", "contudo",
    "foi", "são", "ser", "ter", "tem", "era", "está", "esse",
    "essa", "este", "esta", "isso", "isto", "ele", "ela", "eles", "elas",
    "seu", "sua", "seus", "suas", "meu", "minha", "já", "mais", "como",
    "quando", "onde", "quem", "qual", "quais", "também", "não", "num",
    "numa", "neste", "nesta", "nesse", "nessa", "deste", "desta",
    "desse", "dessa", "pelo", "pela", "após", "ante", "perante",
}

_stemmer = RSLPStemmer()


def split_sentences(text: str) -> list[str]:
    """Divide o texto em frases usando pontuação como delimitador."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 10]


def tokenize(sentence: str) -> list[str]:
    """Extrai palavras da frase (apenas letras, lowercase)."""
    return re.findall(r"[a-záàâãéêíóôõúüç]+", sentence.lower())


def remove_stopwords(tokens: list[str]) -> list[str]:
    return [t for t in tokens if t not in STOPWORDS_PT]


def stem_tokens(tokens: list[str]) -> list[str]:
    return [_stemmer.stem(t) for t in tokens]


def preprocess_sentence(sentence: str) -> list[str]:
    """Retorna lista de stems significativos de uma frase."""
    tokens = tokenize(sentence)
    tokens = remove_stopwords(tokens)
    return stem_tokens(tokens)


def preprocess_text(text: str) -> tuple[list[str], list[list[str]]]:
    """
    Recebe texto bruto, retorna:
        sentences  — lista de frases originais
        processed  — lista de listas de stems (paralela a sentences)
    """
    sentences = split_sentences(text)
    processed = [preprocess_sentence(s) for s in sentences]
    return sentences, processed
