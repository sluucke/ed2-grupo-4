# TODO: entry point — chamar pipeline.generate_title() com artigo de exemplo ou arquivo .txt


from src.pipeline import generate_title

if __name__ == "__main__":
    # TODO: ler artigo de exemplo de um arquivo .txt
    article = """
    O Brasil é um país de grande diversidade cultural e natural. Com uma população de mais de 210 milhões de pessoas, o país é conhecido por suas praias paradisíacas, florestas tropicais exuberantes e uma rica herança cultural. A capital do Brasil é Brasília, uma cidade planejada que abriga os principais órgãos governamentais. O país é famoso por sua música, dança e festivais vibrantes, como o Carnaval. Além disso, o Brasil é um importante produtor agrícola e possui uma economia diversificada. Com uma mistura única de influências indígenas, africanas e europeias, o Brasil é um destino fascinante para turistas de todo o mundo.
    """
    result = generate_title(article)
    print(result)
