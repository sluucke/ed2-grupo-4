import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline import generate_title
from src.preprocessor import split_sentences, tokenize, remove_stopwords

DATASET = os.path.join(
    os.path.dirname(__file__), "..", "data", "raw", "pt", "articles.json"
)
THRESHOLDS = [0.05, 0.1, 0.2]
DEFAULT_THRESHOLD = 0.1


def _bag(text: str) -> set:
    return set(remove_stopwords(tokenize(text)))


def rouge1(hypothesis: str, reference: str) -> dict:
    hyp = _bag(hypothesis)
    ref = _bag(reference)

    if not hyp or not ref:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    common = len(hyp & ref)
    precision = common / len(hyp)
    recall = common / len(ref)
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def baseline_title(body: str) -> str:
    sentences = split_sentences(body)
    return sentences[0] if sentences else ""


def load_articles() -> list[dict]:
    with open(DATASET, encoding="utf-8") as f:
        return json.load(f)


def evaluate(articles: list[dict], threshold: float) -> list[dict]:
    rows = []
    for art in articles:
        result = generate_title(art["body"], threshold=threshold)
        ref = art["reference_title"]
        rows.append({
            "id": art["id"],
            "editoria": art["editoria"],
            "reference": ref,
            "generated": result["title"],
            "rouge": rouge1(result["title"], ref),
            "baseline_rouge": rouge1(baseline_title(art["body"]), ref),
        })
    return rows


def print_per_article(rows: list[dict]) -> None:
    print("\n=== Títulos gerados (threshold = %.2f) ===" % DEFAULT_THRESHOLD)
    for r in rows:
        print(f"\n[{r['id']}] ({r['editoria']})  F1={r['rouge']['f1']:.3f}")
        print(f"  ref : {r['reference']}")
        print(f"  ger : {r['generated']}")


def print_per_editoria(rows: list[dict]) -> None:
    print("\n=== Desempenho por editoria (F1 médio) ===")
    editorias = {}
    for r in rows:
        editorias.setdefault(r["editoria"], []).append(r["rouge"]["f1"])
    print(f"{'editoria':<12} {'n':>3} {'F1 medio':>10}")
    print("-" * 27)
    for ed in sorted(editorias, key=lambda e: -_mean(editorias[e])):
        f1s = editorias[ed]
        print(f"{ed:<12} {len(f1s):>3} {_mean(f1s):>10.3f}")


def print_threshold_study(articles: list[dict]) -> None:
    print("\n=== Efeito do threshold do grafo (F1 médio global) ===")
    print(f"{'threshold':<12} {'F1 medio':>10} {'arestas medias':>16}")
    print("-" * 40)
    for th in THRESHOLDS:
        rows = evaluate(articles, th)
        f1 = _mean([r["rouge"]["f1"] for r in rows])
        edges = _mean([
            generate_title(a["body"], threshold=th)["graph_stats"]["edges"]
            for a in articles
        ])
        print(f"{th:<12} {f1:>10.3f} {edges:>16.1f}")


def print_baseline_comparison(rows: list[dict]) -> None:
    print("\n=== TextRank vs baseline (primeira frase) ===")
    tr = _mean([r["rouge"]["f1"] for r in rows])
    bl = _mean([r["baseline_rouge"]["f1"] for r in rows])
    print(f"  TextRank          F1 medio = {tr:.3f}")
    print(f"  Baseline 1a frase F1 medio = {bl:.3f}")
    delta = tr - bl
    sinal = "+" if delta >= 0 else ""
    print(f"  Ganho do TextRank          = {sinal}{delta:.3f}")


def main():
    articles = load_articles()
    rows = evaluate(articles, DEFAULT_THRESHOLD)

    print_per_article(rows)
    print_per_editoria(rows)
    print_baseline_comparison(rows)
    print_threshold_study(articles)

    f1_global = _mean([r["rouge"]["f1"] for r in rows])
    p_global = _mean([r["rouge"]["precision"] for r in rows])
    rec_global = _mean([r["rouge"]["recall"] for r in rows])
    print("\n=== Resumo global (threshold = %.2f) ===" % DEFAULT_THRESHOLD)
    print(f"  Precision media = {p_global:.3f}")
    print(f"  Recall    medio = {rec_global:.3f}")
    print(f"  F1        medio = {f1_global:.3f}")


if __name__ == "__main__":
    main()
