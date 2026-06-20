"""
Pipeline principal: texto → título gerado.
"""

from src.preprocessor import preprocess_text
from src.graph import build_graph, graph_stats
from src.textrank import textrank, top_k_sentences, best_sentence_index
from src.heuristic import apply_heuristic


def generate_title(text: str, threshold: float = 0.1, verbose: bool = False) -> dict:
    """
    Recebe o corpo de um artigo e retorna o título gerado.

    Returns:
        {
            "title"     : str,
            "best_idx"  : int,
            "scores"    : list[float],
            "stats"     : dict,
            "sentences" : list[str],
        }
    """
    # 1. Pré-processamento
    sentences, processed = preprocess_text(text)

    if len(sentences) == 0:
        return {"title": "", "best_idx": -1, "scores": [], "stats": {}, "sentences": []}

    if len(sentences) == 1:
        return {
            "title": sentences[0],
            "best_idx": 0,
            "scores": [1.0],
            "stats": {"nodes": 1, "edges": 0, "avg_degree": 0},
            "sentences": sentences,
        }

    # 2. Construção do grafo
    matrix = build_graph(processed, threshold=threshold)
    stats = graph_stats(matrix)

    # 3. TextRank
    scores = textrank(matrix)

    # 4. Seleção da melhor frase
    top = top_k_sentences(scores, k=3)
    best_idx = best_sentence_index(scores)
    best_sentence = sentences[best_idx]

    # 5. Heurística de comprimento
    title = apply_heuristic(best_sentence, sentences, processed, top)

    if verbose:
        print(f"\n[Pipeline] {stats}")
        print(f"[Pipeline] Scores: {[round(s, 4) for s in scores]}")
        print(f"[Pipeline] Melhor frase (idx={best_idx}): {best_sentence}")
        print(f"[Pipeline] Título gerado: {title}\n")

    return {
        "title": title,
        "best_idx": best_idx,
        "scores": scores,
        "stats": stats,
        "sentences": sentences,
    }
