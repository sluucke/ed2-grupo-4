import sys

from src.pipeline import generate_title

EXEMPLO = (
    "O Brasil é um país de grande diversidade cultural e natural. "
    "Com uma população de mais de 210 milhões de pessoas, o país é conhecido "
    "por suas praias paradisíacas, florestas tropicais exuberantes e uma rica "
    "herança cultural. A capital do Brasil é Brasília, uma cidade planejada que "
    "abriga os principais órgãos governamentais. O país é famoso por sua música, "
    "dança e festivais vibrantes, como o Carnaval. Além disso, o Brasil é um "
    "importante produtor agrícola e possui uma economia diversificada. Com uma "
    "mistura única de influências indígenas, africanas e europeias, o Brasil é "
    "um destino fascinante para turistas de todo o mundo."
)


def main():
    if len(sys.argv) > 1:
        caminho = sys.argv[1]
        with open(caminho, encoding="utf-8") as f:
            texto = f.read()
        origem = caminho
    else:
        texto = EXEMPLO
        origem = "exemplo embutido"

    resultado = generate_title(texto)
    stats = resultado["graph_stats"]

    print(f"Fonte  : {origem}")
    print(f"Título : {resultado['title']}")
    print(
        f"Grafo  : {stats['nodes']} frases, {stats['edges']} arestas, "
        f"grau médio {stats['avg_degree']:.2f}"
    )


if __name__ == "__main__":
    main()
