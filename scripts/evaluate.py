"""
Avalia o sistema sobre os artigos LLM e exibe métricas.

Métrica principal: ROUGE-1 (Recall, Precision, F1) entre título gerado e título de referência.
ROUGE-1 compara unigramas (palavras individuais).

Uso:
    python scripts/evaluate.py
"""

import json
import os
import sys
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.pipeline import generate_title
from src.preprocessor import tokenize, remove_stopwords


DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "llm_articles.json")


def rouge1(hypothesis: str, reference: str) -> dict:
    """Calcula ROUGE-1 (F1, Precision, Recall) entre duas strings."""
    hyp_tokens = set(remove_stopwords(tokenize(hypothesis)))
    ref_tokens = set(remove_stopwords(tokenize(reference)))

    if not ref_tokens:
        return {"f1": 0.0, "precision": 0.0, "recall": 0.0}

    common = len(hyp_tokens & ref_tokens)
    precision = common / len(hyp_tokens) if hyp_tokens else 0.0
    recall = common / len(ref_tokens)
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {"f1": round(f1, 3), "precision": round(precision, 3), "recall": round(recall, 3)}


def run_evaluation():
    with open(DATA_PATH, encoding="utf-8") as f:
        articles = json.load(f)

    print(f"{'ID':<12} {'Título Gerado':<55} {'Ref':<45} {'F1':>5}")
    print("─" * 120)

    total_f1 = 0.0
    for art in articles:
        result = generate_title(art["body"])
        generated = result["title"]
        reference = art["reference_title"]
        score = rouge1(generated, reference)
        total_f1 += score["f1"]

        print(f"{art['id']:<12} {generated[:53]:<55} {reference[:43]:<45} {score['f1']:>5.3f}")

    avg_f1 = total_f1 / len(articles)
    print("─" * 120)
    print(f"\nROUGE-1 F1 médio: {avg_f1:.3f}  ({len(articles)} artigos)")


if __name__ == "__main__":
    run_evaluation()
