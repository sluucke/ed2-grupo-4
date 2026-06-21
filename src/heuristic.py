import re
from src.textrank import textrank, best_sentence_index
from src.graph import build_graph


def _capitalize(sentence: str) -> str:
    s = sentence.strip().rstrip(".")
    if not s:
        return s
    return s[0].upper() + s[1:]


def apply_heuristic(best_sentence, sentences, processed, top_scores) -> str:
    size = len(best_sentence.split())

    if size > 20:
        match = re.search(r"[,;]", best_sentence)
        if match:
            title = best_sentence[:match.start()]
        else:
            title = " ".join(best_sentence.split()[:20])

    elif size <= 5:
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

    else:
        title = best_sentence

    return _capitalize(title)
