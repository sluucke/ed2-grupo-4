# TODO: carregar data/raw/pt/articles.json e calcular ROUGE-1 para cada artigo


def rouge1(hypothesis: str, reference: str) -> dict:
    # tokenizar e remover stopwords os dois títulos (reutilizar preprocessor)
    # depois:
    #   common    = len(set(hyp) & set(ref))
    #   precision = common / len(set(hyp))  se não vazio
    #   recall    = common / len(set(ref))
    #   f1        = 2 * p * r / (p + r)     se não zero
    # return {"precision": p, "recall": r, "f1": f1}
    pass