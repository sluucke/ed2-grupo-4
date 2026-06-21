import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.heuristic import apply_heuristic, _capitalize


# ── _capitalize ──────────────────────────────────────────────

def test_capitalize_primeira_letra():
    assert _capitalize("o brasil exportou soja.") == "O brasil exportou soja"


def test_capitalize_remove_ponto_final():
    assert _capitalize("Teste com ponto.") == "Teste com ponto"


def test_capitalize_string_vazia():
    assert _capitalize("") == ""


def test_capitalize_nao_altera_resto():
    assert _capitalize("o PIB cresceu 3,2%.") == "O PIB cresceu 3,2%"


# ── Caso ideal: 5–20 palavras (usa direto) ───────────────────

def test_frase_ideal_retorna_direto():
    frase = "O Brasil registrou recorde de exportações em maio"  # 8 palavras
    result = apply_heuristic(frase, [frase], [[]], [(1.0, 0)])
    assert result == "O Brasil registrou recorde de exportações em maio"


def test_frase_ideal_remove_ponto():
    frase = "A balança comercial fechou positiva."
    result = apply_heuristic(frase, [frase], [[]], [(1.0, 0)])
    assert result == "A balança comercial fechou positiva"


# ── Caso longa: > 20 palavras (trunca) ──────────────────────

def test_trunca_na_virgula():
    frase = "O governo federal anunciou novo programa de concessões de infraestrutura avaliado em noventa bilhões de reais, com foco em rodovias e portos"
    result = apply_heuristic(frase, [frase], [[]], [(1.0, 0)])
    assert "," not in result
    assert len(result.split()) <= 20


def test_trunca_no_ponto_e_virgula():
    frase = "A proposta inclui investimentos em educação e saúde para todos os estados do país; o governo espera aprovar o projeto até dezembro"
    result = apply_heuristic(frase, [frase], [[]], [(1.0, 0)])
    assert ";" not in result


def test_trunca_sem_separador_pega_20_palavras():
    frase = " ".join(["palavra"] * 25)  # 25 palavras sem vírgula
    result = apply_heuristic(frase, [frase], [[]], [(1.0, 0)])
    assert len(result.split()) == 20


# ── Caso curta: ≤ 5 palavras (mini TextRank) ────────────────

def test_curta_com_uma_so_frase_retorna_ela_mesma():
    frase = "Soja lidera."  # 2 palavras
    result = apply_heuristic(frase, [frase], [["soj"]], [(1.0, 0)])
    assert result == "Soja lidera"


import pytest

@pytest.mark.skipif(
    not callable(getattr(__import__("src.textrank", fromlist=["textrank"]), "textrank", None))
    or __import__("src.textrank", fromlist=["textrank"]).textrank([[0, 1], [1, 0]]) is None,
    reason="textrank.py ainda não implementado"
)
def test_curta_com_multiplas_frases_retorna_alguma():
    frase_curta = "Soja lidera."
    sentences = [
        "Soja lidera.",
        "O Brasil exportou soja e milho para a China.",
        "A balança comercial fechou com superávit.",
    ]
    processed = [
        ["soj", "lider"],
        ["brasil", "export", "soj", "milh", "chin"],
        ["balanç", "comerci", "fech", "superávit"],
    ]
    top_scores = [(0.9, 0), (0.7, 1), (0.5, 2)]
    result = apply_heuristic(frase_curta, sentences, processed, top_scores)
    assert isinstance(result, str)
    assert len(result) > 0


# ── Capitalização em todos os casos ──────────────────────────

def test_capitaliza_frase_minuscula():
    frase = "o agronegócio liderou os resultados"
    result = apply_heuristic(frase, [frase], [[]], [(1.0, 0)])
    assert result[0].isupper()
