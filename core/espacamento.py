"""
Módulo de Espaçamento de Sementes.

Contém cálculos relacionados à distribuição de sementes por metro linear.
"""

import numpy as np


def sementes_por_metro(plantas_min: int, plantas_max: int, 
                       rendimento_min: float, rendimento_max: float) -> float:
    """
    Calcula a quantidade de sementes por metro linear.
    
    Fórmula baseada em densidade de plantio e taxa de germinação.
    
    Parâmetros:
        plantas_min     : densidade mínima de plantio (plantas/ha)
        plantas_max     : densidade máxima de plantio (plantas/ha)
        rendimento_min  : taxa de germinação mínima (decimal 0-1 ou percentual 0-100)
        rendimento_max  : taxa de germinação máxima (decimal 0-1 ou percentual 0-100)
    
    Retorna:
        N : número de sementes por metro linear
    """
    # Normaliza rendimento para fração (caso venha em %)
    if rendimento_min > 1:
        rendimento_min /= 100.0
    if rendimento_max > 1:
        rendimento_max /= 100.0
    
    N = ((plantas_min + plantas_max) / 40000) / ((rendimento_min + rendimento_max) / 2)
    
    return N


def calcular_espacamento(N: float, distancia_metros: float = 3.0) -> dict:
    """
    Calcula o espaçamento entre sementes e suas posições.
    
    Parâmetros:
        N                : número de sementes por metro linear
        distancia_metros : distância total a considerar (m)
    
    Retorna:
        dict com:
            'sementes_total' : número total de sementes no trecho
            'espacamento_m'  : espaçamento entre sementes (m)
            'espacamento_cm' : espaçamento entre sementes (cm)
            'posicoes_m'     : array com posições de cada semente (m)
    """
    sementes_total = int(N * distancia_metros)
    espacamento_m = distancia_metros / sementes_total
    espacamento_cm = espacamento_m * 100
    
    posicoes_m = np.array([j * espacamento_m for j in range(sementes_total)])
    
    return {
        'sementes_total': sementes_total,
        'sementes_por_metro': N,
        'espacamento_m': espacamento_m,
        'espacamento_cm': espacamento_cm,
        'posicoes_m': posicoes_m,
        'distancia_total_m': distancia_metros
    }


def calcular_espacamento_culturas(culturas_dict: dict, distancia_metros: float = 3.0) -> dict:
    """
    Calcula o espaçamento para múltiplas culturas.
    
    Parâmetros:
        culturas_dict    : dicionário com dados das culturas
                          (ex: {"soja": {"dens_min": ..., "dens_max": ..., ...}})
        distancia_metros : distância total a considerar (m)
    
    Retorna:
        dict onde a chave é o nome da cultura e o valor é o resultado
        de calcular_espacamento() para aquela cultura
    """
    resultados = {}
    
    for nome, dados in culturas_dict.items():
        N = sementes_por_metro(
            dados['dens_min'],
            dados['dens_max'],
            dados['germ_min'],
            dados['germ_max']
        )
        
        resultados[nome] = calcular_espacamento(N, distancia_metros)
    
    return resultados
