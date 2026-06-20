"""
Entry point — gera título para um arquivo de texto ou para um artigo de exemplo.

Uso:
    python main.py                        # roda o exemplo embutido
    python main.py data/raw/artigo.txt    # processa um arquivo
    python main.py data/raw/artigo.txt --verbose
"""

import sys
from src.pipeline import generate_title


EXEMPLO = """
O Brasil registrou recorde de exportações em maio. O agronegócio liderou os
resultados, com destaque para a soja e o milho. A balança comercial fechou com
superávit de R$ 12 bilhões. Analistas apontam o câmbio favorável como fator
principal. O setor industrial também apresentou crescimento moderado, puxado
pela demanda interna e pelo avanço das exportações manufaturadas para a Europa.
""".strip()


def main():
    verbose = "--verbose" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if args:
        path = args[0]
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {path}")
            sys.exit(1)
    else:
        text = EXEMPLO
        print("── Usando artigo de exemplo ──\n")

    result = generate_title(text, verbose=verbose)

    print(f"Título gerado : {result['title']}")
    print(f"Frase origem  : {result['sentences'][result['best_idx']]}")
    print(f"Grafo         : {result['stats']}")


if __name__ == "__main__":
    main()
