"""
Módulo de Dados do IBGE.

Carrega e processa dados de produção agrícola do IBGE.
"""

import pandas as pd
from unidecode import unidecode


def processar_tabela_sintese():
    """
    Retorna a tabela de síntese nacional por cultura (dados do IBGE).
    
    Retorna:
        DataFrame com colunas: Produtos, Área plantada, Área colhida,
        Quantidade produzida, Rendimento médio, Valor da produção
    """
    t1 = pd.DataFrame({
        "Produtos": ["Amendoim", "Soja", "Milho", "Sorgo", "Algodão", "Girassol", "Feijão"],
        "Área plantada (Hectares)": [286112, 46208798, 21436837, 1382091, 1990451, 59889, 2739357],
        "Área colhida (Hectares)": [281563, 45906902, 21186816, 1363415, 1990328, 59694, 2631805],
        "Quantidade produzida (Toneladas)": [806064, 144473768, 114953303, 4090428, 8523606, 90221, 3018459],
        "Rendimento médio (kg/ha)": [2863, 3147, 5426, 3000, 4283, 1511, 1147],
        "Valor da produção (R$)": [
            3334263000, 260233510000, 88118085000, 2706132000, 31331337000, 171748000, 12172130000
        ]
    })
    return t1


def processar_tabela_estados():
    """
    Retorna a tabela de área plantada por Estado para cada cultura (dados do IBGE).
    
    Retorna:
        DataFrame com colunas: Estado, Amendoim, Soja, Milho, Sorgo, Algodão, Girassol, Feijão
    """
    dados_estados = {
        "Estado": [
            "Rondônia", "Acre", "Amazonas", "Roraima", "Pará", "Amapá", "Tocantins", "Maranhão", "Piauí", "Ceará",
            "Rio Grande do Norte", "Paraíba", "Pernambuco", "Alagoas", "Sergipe", "Bahia", "Minas Gerais",
            "Espírito Santo", "Rio de Janeiro", "São Paulo", "Paraná", "Santa Catarina", "Rio Grande do Sul",
            "Mato Grosso do Sul", "Mato Grosso", "Goiás", "Distrito Federal"
        ],
        "Amendoim": [71, 50, 0, 0, 126, 0, 315, 101, 55, 563, 0, 808, 91, 2106, 960, 4090, 14336, 1, 0, 232169, 3140, 4, 1259, 21267, 1508, 3092, 0],
        "Soja": [643639, 17578, 24472, 117215, 1194024, 7500, 1428227, 1302915, 1080496, 3546, 100, 0, 0, 5054, 0, 1969339, 2274950, 504, 748, 1388333, 5773424, 814633, 6708397, 4043539, 12383077, 4942088, 85000],
        "Milho": [349695, 37625, 6147, 18158, 477962, 1800, 471066, 496073, 442105, 572432, 70955, 106853, 184668, 52459, 178893, 649224, 1115757, 16684, 1525, 747217, 2827906, 294946, 808916, 2216501, 7078785, 2159485, 53000],
        "Sorgo": [440, 60, 0, 0, 72945, 0, 37976, 13691, 39848, 40, 0, 0, 3000, 710, 0, 65409, 337296, 0, 0, 160362, 8829, 204, 408, 83852, 71130, 463891, 22000],
        "Algodão": [9862, 0, 0, 0, 250, 0, 8499, 32637, 23924, 2379, 956, 726, 167, 33, 0, 338737, 29863, 0, 0, 9001, 249, 0, 0, 32284, 1464481, 36403, 0],
        "Girassol": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6242, 0, 0, 918, 100, 0, 1662, 492, 4201, 45574, 700],
        "Feijão": [2802, 5139, 856, 2345, 21374, 800, 70005, 45917, 181507, 346595, 52380, 88283, 174802, 29198, 2693, 314388, 307895, 9023, 895, 71182, 544232, 65097, 50030, 16374, 171899, 145546, 18100]
    }
    
    t2 = pd.DataFrame(dados_estados)
    
    # Limpeza: garantir inteiros e substituir NaN por zero
    for col in t2.columns[1:]:
        t2[col] = pd.to_numeric(t2[col], errors="coerce").fillna(0).astype(int)
    
    # Normaliza nomes (para cruzar com shapes do IBGE/Geobr)
    t2["uf_norm"] = t2["Estado"].str.strip().apply(lambda x: unidecode(x).upper())
    
    # Adiciona coluna de total
    cult_cols = ["Amendoim", "Soja", "Milho", "Sorgo", "Algodão", "Girassol", "Feijão"]
    t2["Total"] = t2[cult_cols].sum(axis=1)
    
    return t2


def carregar_dados_ibge():
    """
    Carrega ambas as tabelas do IBGE.
    
    Retorna:
        tupla (tabela_sintese, tabela_estados)
    """
    return processar_tabela_sintese(), processar_tabela_estados()


def obter_top_estados(cultura, n=10):
    """
    Retorna os top N estados por área plantada para uma cultura específica.
    
    Parâmetros:
        cultura : nome da cultura (ex: "Soja")
        n       : número de estados no ranking (padrão: 10)
    
    Retorna:
        DataFrame com Estado e área plantada, ordenado
    """
    t2 = processar_tabela_estados()
    
    if cultura not in t2.columns:
        raise ValueError(f"Cultura '{cultura}' não encontrada. Disponíveis: {list(t2.columns[1:-2])}")
    
    top = t2[["Estado", cultura]].sort_values(cultura, ascending=False).head(n)
    return top


def obter_top_estados_total(n=10):
    """
    Retorna os top N estados por área plantada total (todas as culturas).
    
    Parâmetros:
        n : número de estados no ranking (padrão: 10)
    
    Retorna:
        DataFrame com Estado e Total, ordenado
    """
    t2 = processar_tabela_estados()
    top = t2[["Estado", "Total"]].sort_values("Total", ascending=False).head(n)
    return top
