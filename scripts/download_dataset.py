"""
Prepara o dataset do projeto.

Fontes:
  1. Artigos LLM em PT-BR (dados fictícios, conforme permitido pelo professor)
     → 20 artigos em 5 editorias: política, economia, esportes, tecnologia, saúde
     → Salvos em data/raw/pt/

  2. CNN/DailyMail (inglês, Hugging Face) — complemento para demonstrar
     que o algoritmo é agnóstico ao idioma
     → 10 artigos em data/raw/en/

Uso:
    python scripts/download_dataset.py          # baixa tudo
    python scripts/download_dataset.py --ptonly # só PT-BR
"""

import json
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PT_DIR = os.path.join(DATA_DIR, "pt")
EN_DIR = os.path.join(DATA_DIR, "en")

os.makedirs(PT_DIR, exist_ok=True)
os.makedirs(EN_DIR, exist_ok=True)

# ──────────────────────────────────────────────────────────────────────────────
# Dataset primário: artigos gerados por LLM (PT-BR)
# 20 artigos em 5 editorias × 4 artigos cada
# ──────────────────────────────────────────────────────────────────────────────
LLM_ARTICLES = [
    # ── ECONOMIA (4) ──────────────────────────────────────────────────────────
    {
        "id": "ec_001", "editoria": "economia",
        "body": (
            "A inflação no Brasil recuou para 4,2% em maio, abaixo das expectativas do mercado. "
            "O IPCA registrou queda nos preços de alimentos e energia elétrica. "
            "O Banco Central sinalizou possível corte na taxa Selic na próxima reunião do Copom. "
            "Economistas avaliam que o cenário é favorável para a retomada do crédito. "
            "A bolsa de valores reagiu positivamente, com o Ibovespa subindo 1,8% no pregão."
        ),
        "reference_title": "Inflação recua para 4,2% em maio e abre espaço para corte da Selic",
    },
    {
        "id": "ec_002", "editoria": "economia",
        "body": (
            "O Brasil registrou recorde de exportações em maio, impulsionado pelo agronegócio. "
            "A soja e o milho lideraram os resultados, com alta de 18% em relação ao mesmo período do ano anterior. "
            "A balança comercial fechou com superávit de R$ 12 bilhões no mês. "
            "Analistas apontam o câmbio favorável como fator principal do desempenho. "
            "O setor industrial também apresentou crescimento moderado de 3,2%."
        ),
        "reference_title": "Brasil bate recorde de exportações em maio com liderança do agronegócio",
    },
    {
        "id": "ec_003", "editoria": "economia",
        "body": (
            "O desemprego no Brasil caiu para 6,8% no primeiro trimestre de 2026, menor taxa em 10 anos. "
            "O setor de serviços foi o principal gerador de vagas, com 450 mil novos postos formais. "
            "A renda média do trabalhador cresceu 3,1% acima da inflação no período. "
            "Especialistas alertam que a queda do desemprego pode pressionar salários e inflação. "
            "O governo federal atribui o resultado às políticas de incentivo ao emprego formal."
        ),
        "reference_title": "Desemprego cai para 6,8% e atinge menor nível em 10 anos",
    },
    {
        "id": "ec_004", "editoria": "economia",
        "body": (
            "O governo federal anunciou novo programa de concessões de infraestrutura avaliado em R$ 90 bilhões. "
            "O pacote inclui rodovias, portos, aeroportos e ferrovias em 15 estados. "
            "O leilão das concessões está previsto para o segundo semestre de 2026. "
            "Investidores estrangeiros demonstraram interesse em participar dos lotes. "
            "O ministério prevê a geração de 200 mil empregos diretos ao longo dos contratos."
        ),
        "reference_title": "Governo lança pacote de R$ 90 bilhões em concessões de infraestrutura",
    },

    # ── POLÍTICA (4) ──────────────────────────────────────────────────────────
    {
        "id": "po_001", "editoria": "politica",
        "body": (
            "O Congresso Nacional aprovou nesta semana a reforma tributária complementar. "
            "A medida simplifica o ICMS e cria um imposto único sobre consumo de bens e serviços. "
            "A proposta foi aprovada com 312 votos a favor e 98 contrários na Câmara. "
            "Estados e municípios terão cinco anos para adaptar suas legislações. "
            "Empresários celebraram a aprovação como um avanço para a competitividade do país."
        ),
        "reference_title": "Congresso aprova reforma tributária que cria imposto único sobre consumo",
    },
    {
        "id": "po_002", "editoria": "politica",
        "body": (
            "O Supremo Tribunal Federal retomou nesta terça o julgamento sobre autonomia de bancos centrais. "
            "A discussão gira em torno dos limites do poder executivo sobre a política monetária. "
            "Ministros divergem sobre a interpretação do mandato do presidente do Banco Central. "
            "O julgamento foi suspenso após pedido de vista de um dos ministros. "
            "A decisão deve impactar a relação entre o governo e a autoridade monetária nos próximos anos."
        ),
        "reference_title": "STF retoma julgamento sobre autonomia do Banco Central",
    },
    {
        "id": "po_003", "editoria": "politica",
        "body": (
            "O presidente sancionou o novo marco legal das startups com vetos a dois artigos. "
            "A lei simplifica a abertura e o encerramento de empresas inovadoras no Brasil. "
            "O marco prevê sandbox regulatório para testar novos modelos de negócio. "
            "Associações do setor comemoraram a aprovação, mas criticaram os vetos. "
            "O texto também facilita a emissão de opções de ações para funcionários de startups."
        ),
        "reference_title": "Presidente sanciona marco legal das startups com vetos a dois artigos",
    },
    {
        "id": "po_004", "editoria": "politica",
        "body": (
            "O Brasil assinou acordo de livre-comércio com o bloco do Pacífico Sul nesta sexta-feira. "
            "O tratado deve eliminar tarifas sobre 95% dos produtos trocados entre os países em 10 anos. "
            "O setor agrícola brasileiro foi o principal impulsionador das negociações. "
            "Críticos alertam para o impacto sobre a indústria nacional com a abertura comercial. "
            "O acordo ainda precisa ser ratificado pelos parlamentos dos países membros."
        ),
        "reference_title": "Brasil fecha acordo de livre-comércio com Pacífico Sul após anos de negociação",
    },

    # ── ESPORTES (4) ──────────────────────────────────────────────────────────
    {
        "id": "es_001", "editoria": "esportes",
        "body": (
            "A seleção brasileira de futebol venceu a Argentina por 2 a 1 nas eliminatórias da Copa. "
            "Os gols foram marcados por Endrick e Vini Jr., enquanto a Argentina descontou no segundo tempo. "
            "Com a vitória, o Brasil assume a liderança das eliminatórias sul-americanas com 18 pontos. "
            "O técnico Dorival Júnior elogiou o desempenho coletivo da equipe. "
            "A próxima partida da seleção será contra o Uruguai, em Montevidéu, na próxima semana."
        ),
        "reference_title": "Brasil vence Argentina e assume liderança das eliminatórias com 18 pontos",
    },
    {
        "id": "es_002", "editoria": "esportes",
        "body": (
            "O tenista João Fonseca conquistou seu primeiro título no ATP 500 de Hamburgo neste domingo. "
            "O brasileiro derrotou o espanhol Carlos Alcaraz por 2 sets a 1 na final. "
            "Com o resultado, Fonseca sobe para a 12ª posição no ranking mundial. "
            "O jovem de 19 anos se tornou o tenista brasileiro mais bem colocado no ranking desde Guga. "
            "Multidões comemoraram nas ruas do Rio de Janeiro após o título histórico."
        ),
        "reference_title": "João Fonseca vence Alcaraz e conquista ATP 500 em Hamburgo",
    },
    {
        "id": "es_003", "editoria": "esportes",
        "body": (
            "O Flamengo venceu o Palmeiras por 3 a 0 e conquistou o Campeonato Brasileiro com duas rodadas de antecedência. "
            "Os gols foram marcados por Pedro, Arrascaeta e Gabi no segundo tempo. "
            "Foi o décimo segundo título brasileiro do clube carioca. "
            "O técnico Filipe Luís dedicou o troféu à torcida que encheu o Maracanã. "
            "O Palmeiras termina a temporada como vice-campeão pela terceira vez consecutiva."
        ),
        "reference_title": "Flamengo bate Palmeiras e conquista o Brasileirão com dois jogos de antecedência",
    },
    {
        "id": "es_004", "editoria": "esportes",
        "body": (
            "O Brasil sediará os Jogos Pan-Americanos de 2031, confirmou o Comitê Olímpico das Américas. "
            "A cidade do Rio de Janeiro foi escolhida após disputa com Buenos Aires e Bogotá. "
            "O evento deverá movimentar R$ 4 bilhões na economia carioca. "
            "O governo federal prometeu investimentos em infraestrutura esportiva para sediar as competições. "
            "Os jogos contarão com 41 esportes e mais de 6 mil atletas de 41 países."
        ),
        "reference_title": "Rio de Janeiro é escolhido sede dos Jogos Pan-Americanos de 2031",
    },

    # ── TECNOLOGIA (4) ────────────────────────────────────────────────────────
    {
        "id": "te_001", "editoria": "tecnologia",
        "body": (
            "A startup brasileira Quanta recebeu investimento de R$ 200 milhões em rodada série B. "
            "A empresa desenvolve software de inteligência artificial para diagnóstico médico. "
            "O aporte foi liderado por fundos americanos e europeus especializados em healthtech. "
            "A Quanta pretende expandir para mercados da América Latina e Portugal nos próximos 18 meses. "
            "O CEO afirmou que o capital será usado principalmente em pesquisa e desenvolvimento."
        ),
        "reference_title": "Startup Quanta capta R$ 200 milhões para expandir IA médica na América Latina",
    },
    {
        "id": "te_002", "editoria": "tecnologia",
        "body": (
            "O governo federal lançou o programa Brasil Digital, voltado à universalização da internet. "
            "O plano prevê fibra óptica para 5 mil municípios ainda sem acesso de alta velocidade até 2028. "
            "O investimento total estimado é de R$ 15 bilhões provenientes de parcerias público-privadas. "
            "Operadoras de telecomunicações terão metas de cobertura vinculadas à renovação de licenças. "
            "Especialistas estimam que o programa pode reduzir a exclusão digital em 40% até o fim da década."
        ),
        "reference_title": "Governo lança Brasil Digital para levar fibra óptica a 5 mil municípios até 2028",
    },
    {
        "id": "te_003", "editoria": "tecnologia",
        "body": (
            "O Brasil aprovou regulamentação para uso de inteligência artificial no setor público. "
            "A lei exige transparência algorítmica e auditorias periódicas em sistemas de IA governamentais. "
            "Decisões automatizadas que afetem direitos de cidadãos deverão ter revisão humana obrigatória. "
            "Especialistas elogiaram o texto, mas pediram ampliação das sanções para descumprimento. "
            "O Brasil se torna o terceiro país da América Latina a regulamentar IA de forma abrangente."
        ),
        "reference_title": "Brasil aprova lei de IA que exige transparência e revisão humana em decisões públicas",
    },
    {
        "id": "te_004", "editoria": "tecnologia",
        "body": (
            "A Embraer anunciou parceria com empresa de semicondutores para desenvolver chips aeronáuticos no Brasil. "
            "O acordo prevê investimento conjunto de R$ 1,2 bilhão em uma fábrica em São José dos Campos. "
            "Os chips serão usados em sistemas de controle de voo e comunicação de aviões regionais. "
            "O projeto deve gerar 1.500 empregos especializados na região do Vale do Paraíba. "
            "A parceria conta com apoio do BNDES e do Ministério da Ciência e Tecnologia."
        ),
        "reference_title": "Embraer anuncia fábrica de chips aeronáuticos em São José dos Campos com R$ 1,2 bi",
    },

    # ── SAÚDE (4) ─────────────────────────────────────────────────────────────
    {
        "id": "sa_001", "editoria": "saude",
        "body": (
            "O Ministério da Saúde anunciou a ampliação da campanha de vacinação contra a dengue. "
            "A vacina estará disponível em postos de saúde de 50 municípios prioritários a partir de julho. "
            "O número de casos confirmados da doença já supera 1,5 milhão em 2026. "
            "Autoridades reforçam a importância da eliminação de focos do mosquito Aedes aegypti. "
            "A campanha também incluirá ações educativas nas escolas e comunidades de baixa renda."
        ),
        "reference_title": "Ministério da Saúde amplia vacinação contra dengue em 50 municípios prioritários",
    },
    {
        "id": "sa_002", "editoria": "saude",
        "body": (
            "Pesquisadores brasileiros desenvolveram teste rápido para detectar resistência a antibióticos. "
            "O exame apresenta resultado em 40 minutos e tem acurácia de 97% em testes clínicos. "
            "O dispositivo foi desenvolvido pelo Instituto Butantan em parceria com a USP. "
            "A tecnologia pode reduzir o uso desnecessário de antibióticos e combater superbactérias. "
            "O Ministério da Saúde analisa a incorporação do teste ao SUS ainda este ano."
        ),
        "reference_title": "Butantan desenvolve teste de 40 minutos que detecta resistência a antibióticos",
    },
    {
        "id": "sa_003", "editoria": "saude",
        "body": (
            "O SUS incorporou novo medicamento para tratamento de câncer de pulmão em estágio avançado. "
            "A droga, um inibidor de checkpoint imunológico, aumenta a sobrevida média em 8 meses. "
            "A decisão da Conitec leva em conta custo-efetividade e impacto orçamentário. "
            "Pacientes com mutação específica no gene EGFR serão os principais beneficiados. "
            "Estima-se que 12 mil pacientes por ano poderão ter acesso ao medicamento pelo sistema público."
        ),
        "reference_title": "SUS passa a oferecer novo remédio que prolonga sobrevida de pacientes com câncer de pulmão",
    },
    {
        "id": "sa_004", "editoria": "saude",
        "body": (
            "O Brasil zerou os casos de sarampo pela segunda vez em sua história, anunciou o Ministério da Saúde. "
            "A conquista é resultado de campanhas intensivas de vacinação nos últimos 18 meses. "
            "A cobertura vacinal com duas doses da vacina tríplice viral chegou a 98% da população. "
            "O país havia perdido o status de livre de sarampo em 2019 após surto no Amazonas. "
            "A OMS reconheceu o Brasil como referência em controle de doenças imunopreveníveis."
        ),
        "reference_title": "Brasil elimina sarampo pela segunda vez após campanha que vacinou 98% da população",
    },
]


def save_pt_dataset():
    # JSON consolidado
    path_json = os.path.join(PT_DIR, "articles.json")
    with open(path_json, "w", encoding="utf-8") as f:
        json.dump(LLM_ARTICLES, f, ensure_ascii=False, indent=2)

    # .txt individual por artigo
    for art in LLM_ARTICLES:
        fname = os.path.join(PT_DIR, f"{art['id']}.txt")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(art["body"])

    print(f"[PT-BR] {len(LLM_ARTICLES)} artigos salvos em {PT_DIR}/")


def save_en_dataset(n: int = 10):
    try:
        from datasets import load_dataset
    except ImportError:
        print("[EN] 'datasets' não instalado — pulando CNN/DailyMail. (pip install datasets)")
        return

    print("[EN] Baixando CNN/DailyMail via Hugging Face…")
    ds = load_dataset("abisee/cnn_dailymail", "3.0.0", split="test", streaming=True)
    articles = []
    for i, item in enumerate(ds):
        if i >= n:
            break
        first_highlight = item["highlights"].split("\n")[0].strip()
        articles.append({
            "id": f"en_{i+1:03d}",
            "body": item["article"].strip(),
            "reference_title": first_highlight,
        })

    path_json = os.path.join(EN_DIR, "articles.json")
    with open(path_json, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    for art in articles:
        fname = os.path.join(EN_DIR, f"{art['id']}.txt")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(art["body"])

    print(f"[EN] {len(articles)} artigos salvos em {EN_DIR}/")


if __name__ == "__main__":
    ptonly = "--ptonly" in sys.argv
    save_pt_dataset()
    if not ptonly:
        save_en_dataset(n=10)
    print("\nDataset pronto. Rode: python scripts/evaluate.py")
