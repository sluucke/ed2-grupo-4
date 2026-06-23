from src.graph import build_graph, graph_stats
from src.preprocessor import preprocess_text
from src.textrank import textrank, top_k_sentences, best_sentence_index
from src.heuristic import apply_heuristic


def generate_title(text: str, threshold: float = 0.1) -> dict:
    sentences, processed = preprocess_text(text)
    matrix = build_graph(processed, threshold)
    scores = textrank(matrix)
    top = top_k_sentences(scores, k=3)
    best_idx = best_sentence_index(scores)
    title = apply_heuristic(sentences[best_idx], sentences, processed, top)

    return {
        "title": title,
        "best_sentence_index": best_idx,
        "scores": scores,
        "sentences": sentences,
        "graph_stats": graph_stats(matrix),
    }
