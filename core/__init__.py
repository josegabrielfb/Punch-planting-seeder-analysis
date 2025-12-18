"""
Core - Módulo principal de cálculos do dosador de sementes.
Contém toda a lógica de negócio: cinemática, forças, torque e espaçamento.
"""

from .cinematica import (
    espaco,
    velocidade,
    aceleracao,
    jerk,
    velocidade_angular,
    omega_rpm,
    encontrar_theta_solo,
    y_solo_mm
)

from .forcas_torque import (
    y_theta,
    y_ddot_theta,
    beta_theta,
    a_biela_parallel,
    forcas_FB_FM,
    torque,
    construir_F_VS_variavel
)

from .espacamento import (
    sementes_por_metro,
    calcular_espacamento
)

__all__ = [
    # Cinemática
    'espaco',
    'velocidade',
    'aceleracao',
    'jerk',
    'velocidade_angular',
    'omega_rpm',
    'encontrar_theta_solo',
    'y_solo_mm',
    # Forças e Torque
    'y_theta',
    'y_ddot_theta',
    'beta_theta',
    'a_biela_parallel',
    'forcas_FB_FM',
    'torque',
    'construir_F_VS_variavel',
    # Espaçamento
    'sementes_por_metro',
    'calcular_espacamento',
]
