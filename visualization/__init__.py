"""
Módulo de Visualização - Todos os gráficos do projeto.

Contém funções para plotar cinemática, torque, espaçamento e dados do IBGE.
"""

from .plot_cinematica import (
    plotar_posicao,
    plotar_velocidade,
    plotar_aceleracao,
    plotar_jerk,
    plotar_cinematica_completa
)

from .plot_torque import (
    plotar_torque,
    plotar_forcas
)

from .plot_espacamento import (
    plotar_distribuicao_sementes
)

from .plot_ibge import (
    plotar_area_culturas,
    plotar_ranking_estados,
    plotar_mapa_cultura,
    plotar_mapa_total
)

__all__ = [
    # Cinemática
    'plotar_posicao',
    'plotar_velocidade',
    'plotar_aceleracao',
    'plotar_jerk',
    'plotar_cinematica_completa',
    # Torque
    'plotar_torque',
    'plotar_forcas',
    # Espaçamento
    'plotar_distribuicao_sementes',
    # IBGE
    'plotar_area_culturas',
    'plotar_ranking_estados',
    'plotar_mapa_cultura',
    'plotar_mapa_total',
]
