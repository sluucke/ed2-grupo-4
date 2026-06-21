# TODO: implementar construção do grafo de similaridade



def _similarity(text1, text2) -> float:
    # implementar calculo de similaridade entre dois textos, baseado na quantidade de palavras em comum
    pass

def build_graph(processed, threshold=0.1) -> list[list[float]]:
    # construir grafo de similaridade entre os textos processados, utilizando a função de similaridade e o limiar definido
    pass


def graph_stats(matrix) -> dict:
    # calcular estatísticas do grafo, como número de vértices, arestas, grau médio, etc
    '''
        exemplo de retorno:
        {
            "nodes": 20,
            "edges": 50,
            "average_degree": 5.0
        }
    '''
    pass