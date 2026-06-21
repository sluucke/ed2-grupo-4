# TODO: implementar algoritmo TextRank + heap

def textrank(matrix: list[list[float]]) -> list[float]:
    # recebe a matriz de adjacência do grafo de frases
    # retorna um score por frase (paralelo à lista de frases)
    pass

def top_k_sentences(scores: list[float], k=5) -> list[str]:
    # recebe a lista de frases e seus respectivos scores
    # retorna as top k frases mais relevantes, ordenadas pela posição original no texto
    pass

def best_sentence_index(scores: list[float]) -> int:
    # recebe a lista de scores das frases
    # retorna o índice da frase com o maior score
    pass

