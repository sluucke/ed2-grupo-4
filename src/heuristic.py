"""
Módulo de heurística de comprimento para geração de título.

Regras:
    ≤ 5 palavras  → executa mini-TextRank sobre top-3 frases → nova candidata
    5–20 palavras → usa a frase diretamente como título
    > 20 palavras → trunca no 1º separador natural (vírgula ou ponto e vírgula)
"""

import re
from src.textrank import textrank, top_k_sentences, best_sentence_index
from src.graph import build_graph


def _word_count(sentence: str) -> int:
    return len(sentence.split())


def _truncate_at_separator(sentence: str) -> str:
    """Trunca no primeiro separador natural após a 5ª palavra."""
    match = re.search(r"[,;]", sentence)
    if match:
        return sentence[: match.start()].strip()
    # sem separador: usa as primeiras 20 palavras
    words = sentence.split()
    return " ".join(words[:20])


def _capitalize(sentence: str) -> str:
    """Garante que a primeira letra seja maiúscula e remove ponto final."""
    s = sentence.strip().rstrip(".")
    return s[0].upper() + s[1:] if s else s


def apply_heuristic(
    best_sentence: str,
    sentences: list[str],
    processed: list[list[str]],
    top_scores: list[tuple[float, int]],
) -> str:
    """
    Aplica a heurística de comprimento sobre a frase candidata.

    Args:
        best_sentence : frase com maior score do TextRank
        sentences     : todas as frases originais
        processed     : frases pré-processadas (stems)
        top_scores    : resultado de top_k_sentences (score, idx)

    Returns:
        título gerado
    """
    wc = _word_count(best_sentence)

    if wc > 20:
        title = _truncate_at_separator(best_sentence)

    elif wc <= 5:
        # mini-TextRank sobre as top-3 frases
        top_indices = [idx for _, idx in top_scores[:3]]
        sub_sentences = [sentences[i] for i in top_indices]
        sub_processed = [processed[i] for i in top_indices]

        if len(sub_sentences) > 1:
            sub_matrix = build_graph(sub_processed, threshold=0.0)
            sub_scores = textrank(sub_matrix)
            best_sub_idx = best_sentence_index(sub_scores)
            title = sub_sentences[best_sub_idx]
        else:
            title = best_sentence

        # se ainda curta, usa as primeiras 10 palavras da frase original
        if _word_count(title) <= 5:
            words = best_sentence.split()
            title = " ".join(words[:10]) if len(words) > 5 else best_sentence

    else:
        title = best_sentence

    return _capitalize(title)
