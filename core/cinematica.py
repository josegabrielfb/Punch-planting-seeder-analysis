"""
Módulo de Cinemática do Mecanismo de Dosagem de Sementes.

Contém todas as funções relacionadas ao cálculo de posição, velocidade,
aceleração e jerk da haste de perfuração em função do ângulo da manivela.
"""

import numpy as np
from scipy.optimize import fsolve


# ========================================================================
# POSIÇÃO (ESPAÇO)
# ========================================================================

def espaco(theta: np.ndarray, r: float, L: float, h: float) -> np.ndarray:
    """
    Calcula a posição y da haste de perfuração em função do ângulo theta.
    
    Referencial: centro da manivela.
    
    Parâmetros:
        theta : array de ângulos em radianos
        r     : raio da manivela (mm)
        L     : comprimento da biela (mm)
        h     : offset vertical (mm)
    
    Retorna:
        y : posição vertical da ponta da haste (mm)
    """
    y = np.sqrt(L**2 - (r * np.sin(theta))**2) - r * np.cos(theta) + h
    return y


def y_solo_mm(theta: np.ndarray, r: float, L: float, h: float, 
              altura_centro_m: float) -> np.ndarray:
    """
    Posição da ponta da haste em relação ao SOLO (mm).
    
    Convenção:
        y_solo = 0   -> tocando o solo
        y_solo < 0   -> enterrado (profundidade negativa)
        y_solo > 0   -> acima do solo
    
    Parâmetros:
        theta           : array de ângulos em radianos
        r, L, h         : geometria (mm)
        altura_centro_m : altura do centro da manivela em relação ao solo (mm)
    
    Retorna:
        y_solo : posição em relação ao solo (mm)
    """
    y_m = espaco(theta, r, L, h)
    y_solo = altura_centro_m - y_m
    return y_solo


# ========================================================================
# VELOCIDADE
# ========================================================================

def velocidade(theta: np.ndarray, omega: float, r: float, L: float) -> np.ndarray:
    """
    Calcula a velocidade dy/dt da haste em função do ângulo theta.
    
    Parâmetros:
        theta : array de ângulos em radianos
        omega : velocidade angular da manivela (rad/s)
        r     : raio da manivela (mm)
        L     : comprimento da biela (mm)
    
    Retorna:
        dy_dt : velocidade vertical da haste (mm/s)
    """
    s = np.sin(theta)
    c = np.cos(theta)
    inside = L**2 - r**2 * s**2
    
    dy_dt = r * s * (1 - (r * c) / np.sqrt(inside)) * omega
    
    return dy_dt


# ========================================================================
# ACELERAÇÃO
# ========================================================================

def aceleracao(theta: np.ndarray, omega: float, r: float, L: float, 
               alpha: float = 0.0) -> np.ndarray:
    """
    Calcula a aceleração d²y/dt² da haste em função do ângulo theta.
    
    Parâmetros:
        theta : array de ângulos em radianos
        omega : velocidade angular da manivela (rad/s)
        r     : raio da manivela (mm)
        L     : comprimento da biela (mm)
        alpha : aceleração angular da manivela (rad/s²), padrão = 0
    
    Retorna:
        d2y_dt2 : aceleração vertical da haste (mm/s²)
    """
    s = np.sin(theta)
    c = np.cos(theta)
    s2 = np.sin(2 * theta)
    c2 = np.cos(2 * theta)
    
    inside = L**2 - r**2 * s**2
    
    numerador = r**2 * (4 * inside * c2 + (r * s2)**2)
    denominador = 4 * np.power(inside, 1.5)
    
    d2y_dt2 = (r * c - numerador / denominador) * omega**2
    
    if alpha != 0.0:
        v = velocidade(theta, omega, r, L)
        d2y_dt2 += v * alpha
    
    return d2y_dt2


# ========================================================================
# JERK
# ========================================================================

def jerk(theta: np.ndarray, omega: float, alpha: float, r: float, L: float, 
         beta: float = 0.0) -> np.ndarray:
    """
    Calcula o jerk d³y/dt³ da haste em função do ângulo theta.
    
    Parâmetros:
        theta : array de ângulos em radianos
        omega : velocidade angular da manivela (rad/s)
        alpha : aceleração angular da manivela (rad/s²)
        r     : raio da manivela (mm)
        L     : comprimento da biela (mm)
        beta  : derivada da aceleração angular (rad/s³), padrão = 0
    
    Retorna:
        d3y_dt3 : jerk vertical da haste (mm/s³)
    """
    s = np.sin(theta)
    s2 = np.sin(2 * theta)
    c2 = np.cos(2 * theta)
    
    inside = L**2 - r**2 * s**2
    
    termo1_num = r**2 * s2 * (16 * inside**2 - 3 * r**2 * (4 * inside * c2 + (r * s2)**2))
    termo1_den = 8 * np.power(inside, 2.5)
    termo1 = termo1_num / termo1_den
    
    termo2 = 3 * aceleracao(theta, omega, r, L, alpha) * omega * alpha
    termo3 = velocidade(theta, omega, r, L) * beta
    
    d3y_dt3 = termo1 * omega**3 + termo2 + termo3
    
    return d3y_dt3


# ========================================================================
# VELOCIDADE ANGULAR
# ========================================================================

def sementes_por_metro(plantas_min: int, plantas_max: int, 
                       rendimento_min: float, rendimento_max: float) -> float:
    """
    Calcula a quantidade de sementes por metro linear.
    
    Parâmetros:
        plantas_min     : densidade mínima de plantio (plantas/ha)
        plantas_max     : densidade máxima de plantio (plantas/ha)
        rendimento_min  : taxa de germinação mínima (0-1 ou 0-100)
        rendimento_max  : taxa de germinação máxima (0-1 ou 0-100)
    
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


def velocidade_angular(vt_kmh: float, N: float) -> float:
    """
    Calcula a velocidade angular da manivela em rad/s.
    
    Parâmetros:
        vt_kmh : velocidade do trator (km/h)
        N      : número de sementes por metro linear
    
    Retorna:
        omega : velocidade angular (rad/s)
    """
    omega = 2 * np.pi * vt_kmh * N / 3.6
    return omega


def omega_rpm(omega: float) -> float:
    """
    Converte velocidade angular de rad/s para RPM.
    
    Parâmetros:
        omega : velocidade angular (rad/s)
    
    Retorna:
        rpm : velocidade angular em rotações por minuto
    """
    rpm = omega * 60 / (2 * np.pi)
    return rpm


# ========================================================================
# ENCONTRAR ÂNGULO DE CONTATO COM O SOLO
# ========================================================================

def encontrar_theta_solo(r: float, L: float, h: float, 
                         altura_centro: float = 591.47) -> dict:
    """
    Encontra os ângulos θ quando a haste toca o solo (y_solo = 0).
    
    Usa método numérico de Newton-Raphson via fsolve.
    
    Parâmetros:
        r              : raio da manivela (mm)
        L              : comprimento da biela (mm)
        h              : offset vertical (mm)
        altura_centro  : altura do centro da manivela em relação ao solo (mm)
    
    Retorna:
        dict com:
            'descida' : ângulo quando a haste desce (graus)
            'subida'  : ângulo quando a haste sobe (graus)
    """
    def eq_solo(theta_rad):
        """Equação: y_solo(theta) = 0"""
        y_manivela = espaco(theta_rad, r, L, h)
        y_solo = altura_centro - y_manivela
        return y_solo
    
    # Descida: próximo de 120 graus
    theta_desc_rad = fsolve(eq_solo, np.deg2rad(120.0))[0]
    theta_desc_deg = np.rad2deg(theta_desc_rad)
    
    # Subida: próximo de 240 graus
    theta_sub_rad = fsolve(eq_solo, np.deg2rad(240.0))[0]
    theta_sub_deg = np.rad2deg(theta_sub_rad)
    
    return {
        'descida': theta_desc_deg,
        'subida': theta_sub_deg
    }


# ========================================================================
# FUNÇÕES AUXILIARES
# ========================================================================

def calcular_cinematica_completa(theta_deg: np.ndarray, r: float, L: float, h: float,
                                 altura_centro: float, omega: float, 
                                 alpha: float = 0.0, beta: float = 0.0) -> dict:
    """
    Calcula toda a cinemática (posição, velocidade, aceleração, jerk) de uma vez.
    
    Parâmetros:
        theta_deg      : array de ângulos em graus
        r, L, h        : geometria (mm)
        altura_centro  : altura do centro da manivela (mm)
        omega          : velocidade angular (rad/s)
        alpha          : aceleração angular (rad/s²)
        beta           : derivada da aceleração (rad/s³)
    
    Retorna:
        dict com arrays: 'posicao', 'velocidade', 'aceleracao', 'jerk'
    """
    theta_rad = np.deg2rad(theta_deg)
    
    pos = y_solo_mm(theta_rad, r, L, h, altura_centro)
    vel = velocidade(theta_rad, omega, r, L)
    acel = aceleracao(theta_rad, omega, r, L, alpha)
    jer = jerk(theta_rad, omega, alpha, r, L, beta)
    
    return {
        'theta_deg': theta_deg,
        'theta_rad': theta_rad,
        'posicao': pos,
        'velocidade': vel,
        'aceleracao': acel,
        'jerk': jer
    }
