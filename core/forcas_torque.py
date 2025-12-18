"""
Módulo de Forças e Torque do Mecanismo de Dosagem de Sementes.

Contém cálculos relacionados às forças na biela, manivela e torque no eixo.
"""

import numpy as np


# ========================================================================
# FUNÇÕES GEOMÉTRICAS E CINEMÁTICAS AUXILIARES
# ========================================================================

def y_theta(theta: np.ndarray, r: float, L: float, h: float) -> np.ndarray:
    """
    Posição vertical da ponta da haste (referencial do CENTRO da manivela).
    
    Parâmetros:
        theta : array em radianos
        r, L, h : geometria em metros
    
    Retorna:
        y : posição vertical em metros
    """
    return np.sqrt(L**2 - r**2 * np.sin(theta)**2) - r * np.cos(theta) + h


def y_ddot_theta(theta: np.ndarray, r: float, L: float, omega: float) -> np.ndarray:
    """
    Aceleração vertical da ponta da haste: y¨(theta).
    
    Assume alpha = 0 (velocidade angular constante).
    
    Parâmetros:
        theta : array em radianos
        r, L  : geometria em metros
        omega : velocidade angular em rad/s
    
    Retorna:
        y_ddot : aceleração vertical em m/s²
    """
    s = np.sin(theta)
    c = np.cos(theta)
    inside = L**2 - r**2 * s**2
    
    num1 = r * c
    num2 = (r**2 * (4 * inside * np.cos(2*theta) + (r * np.sin(2*theta))**2)) / (4 * inside**(1.5))
    
    return (num1 - num2) * omega**2


def beta_theta(theta: np.ndarray, r: float, L: float) -> np.ndarray:
    """
    Ângulo da biela com a vertical (beta(theta)).
    
    Relações:
        cos beta = sqrt(L² - r² sin² theta) / L
        sin beta = r sin theta / L
    
    Parâmetros:
        theta : array em radianos
        r, L  : geometria em metros
    
    Retorna:
        beta : ângulo em radianos
    """
    s = np.sin(theta)
    inside = L**2 - r**2 * s**2
    cos_beta = np.sqrt(inside) / L
    sin_beta = r * s / L
    return np.arctan2(sin_beta, cos_beta)


def a_biela_parallel(theta: np.ndarray, r: float, L: float, h: float, 
                     omega: float) -> np.ndarray:
    """
    Componente da aceleração do CG da biela ao longo do seu eixo (a_biela,||).
    
    Aproximação: a_CG = (a_A + a_B)/2
    onde A é o ponto na manivela e B é o ponto na haste.
    
    Parâmetros:
        theta : array em radianos
        r, L, h : geometria em metros
        omega : velocidade angular em rad/s
    
    Retorna:
        a_parallel : aceleração paralela ao eixo da biela em m/s²
    """
    s = np.sin(theta)
    c = np.cos(theta)
    
    # Aceleração do ponto A (manivela)
    aA_x = -omega**2 * r * s
    aA_y = -omega**2 * r * c
    
    # Aceleração do ponto B (haste) – somente y
    aB_y = y_ddot_theta(theta, r, L, omega)
    aB_x = 0.0
    
    # Aceleração do CG da biela
    aCG_x = 0.5 * (aA_x + aB_x)
    aCG_y = 0.5 * (aA_y + aB_y)
    
    # Versor ao longo da biela
    beta = beta_theta(theta, r, L)
    e_b_x = np.sin(beta)
    e_b_y = np.cos(beta)
    
    # Componente paralela à biela
    a_parallel = aCG_x * e_b_x + aCG_y * e_b_y
    return a_parallel


# ========================================================================
# FORÇAS
# ========================================================================

def forcas_FB_FM(theta: np.ndarray,
                 r: float, L: float, h: float,
                 m_haste: float, m_biela: float,
                 P_haste: float, P_biela: float,
                 F_VS_arr: np.ndarray,
                 omega: float) -> tuple:
    """
    Calcula F_B(theta) e F_M(theta) - forças na biela e na manivela.
    
    Hipóteses: sem atrito entre haste e guia.
    
    Parâmetros:
        theta    : array em radianos
        r, L, h  : geometria (m)
        m_haste, m_biela : massas (kg)
        P_haste, P_biela : pesos (N)
        F_VS_arr : força vertical do solo F_VS(theta) (N)
        omega    : velocidade angular da manivela (rad/s)
    
    Retorna:
        (F_B, F_M) : tupla com arrays de forças (N)
    """
    theta = np.array(theta, dtype=float)
    
    # 1) Aceleração da ponta da haste (a_B = y¨(theta))
    aB = y_ddot_theta(theta, r, L, omega)
    
    # 2) Força vertical no pino B: F_B,y = m_haste*aB - P_haste + F_VS(theta)
    F_B_y = m_haste * aB - P_haste + F_VS_arr
    
    # 3) cos(beta) para projetar
    s = np.sin(theta)
    inside = L**2 - r**2 * s**2
    root = np.sqrt(inside)
    cos_beta = root / L
    
    # Força axial na biela no pino B (módulo)
    F_B = F_B_y / cos_beta
    
    # 4) Componente da aceleração do CG da biela ao longo dela
    a_b_par = a_biela_parallel(theta, r, L, h, omega)
    
    # 5) Componente do peso da biela ao longo dela
    beta = beta_theta(theta, r, L)
    P_b_par = P_biela * np.cos(beta)
    
    # 6) Força que a manivela faz na biela no pino A
    F_M = m_biela * a_b_par - F_B - P_b_par
    
    return F_B, F_M


# ========================================================================
# TORQUE
# ========================================================================

def torque(theta: np.ndarray,
           r: float, L: float, h: float,
           m_haste: float, m_biela: float,
           P_haste: float, P_biela: float,
           F_VS: np.ndarray,
           omega: float,
           F_VS_theta_range_deg: tuple = None) -> np.ndarray:
    """
    Calcula o torque tau(theta) no eixo da manivela, desconsiderando atrito.
    
    Parâmetros:
        theta                : array em radianos
        r, L, h              : geometria (m)
        m_haste, m_biela     : massas (kg)
        P_haste, P_biela     : pesos (N)
        F_VS                 : força vertical do solo, escalar ou array (N)
        omega                : velocidade angular (rad/s)
        F_VS_theta_range_deg : tupla (theta_min, theta_max) para aplicar F_VS,
                               ou None para aplicar em todo o intervalo
    
    Retorna:
        tau : torque no eixo da manivela (N·m)
    """
    theta = np.array(theta, dtype=float)
    
    # Aplicar F_VS somente no intervalo pedido (se fornecido)
    if F_VS_theta_range_deg is not None:
        theta_min_deg, theta_max_deg = F_VS_theta_range_deg
        theta_deg = np.rad2deg(theta)
        mask = (theta_deg >= theta_min_deg) & (theta_deg <= theta_max_deg)
        
        F_VS_arr = np.zeros_like(theta)
        if np.isscalar(F_VS):
            F_VS_arr[mask] = F_VS
        else:
            F_VS_arr[mask] = F_VS[mask]
    else:
        if np.isscalar(F_VS):
            F_VS_arr = np.full_like(theta, F_VS)
        else:
            F_VS_arr = F_VS
    
    # 1) Aceleração da ponta da haste
    aB = y_ddot_theta(theta, r, L, omega)
    
    # 2) Força vertical no pino B (biela na haste)
    F_B_y = m_haste * aB - P_haste + F_VS_arr
    
    # 3) cos(beta) para projetar
    s = np.sin(theta)
    inside = L**2 - r**2 * s**2
    root = np.sqrt(inside)
    cos_beta = root / L
    
    # Força axial na biela no pino B (módulo)
    F_B = F_B_y / cos_beta
    
    # 4) Componente da aceleração do CG da biela ao longo dela
    a_b_par = a_biela_parallel(theta, r, L, h, omega)
    
    # 5) Componente do peso da biela ao longo dela
    beta = beta_theta(theta, r, L)
    P_b_par = P_biela * np.cos(beta)
    
    # 6) Força que a manivela faz na biela no pino A (ao longo da biela)
    F_M = m_biela * a_b_par - F_B - P_b_par
    
    # 7) Ângulo entre manivela e biela: phi = theta - beta
    phi = theta - beta
    
    # 8) Torque: tau = r * F_M * sin(phi)
    tau = r * F_M * np.sin(phi)
    
    return tau


# ========================================================================
# CONSTRUÇÃO DE F_VS VARIÁVEL
# ========================================================================

def construir_F_VS_variavel(theta_deg: np.ndarray, r: float, L: float, h: float,
                            altura_centro: float) -> tuple:
    """
    Constrói F_VS(θ) variável por partes, conforme modelo do solo.
    
    F_VS(θ) = k * y(θ)²      para 123.28° ≤ θ ≤ θ_pico
             = F_max_const   para θ_pico < θ ≤ 180°
             = 0             fora desse intervalo
    
    Parâmetros:
        theta_deg     : array de ângulos em graus
        r, L, h       : geometria (mm)
        altura_centro : altura do centro da manivela (mm)
    
    Retorna:
        (F_VS_array, F_max, theta_pico, info_dict)
    """
    # Converter para radianos e metros
    theta_rad = np.deg2rad(theta_deg)
    r_m = r / 1000.0
    L_m = L / 1000.0
    h_m = h / 1000.0
    altura_m = altura_centro / 1000.0
    
    # Calcular posição em relação ao solo
    y_m = y_theta(theta_rad, r_m, L_m, h_m)
    y_solo_m = altura_m - y_m
    y_mm = y_solo_m * 1000.0
    
    # Constantes
    THETA_INICIO = 123.28
    THETA_FIM = 180.0
    Y_ALVO_MM = -47.15
    
    # Encontrar θ onde y(θ) = Y_ALVO_MM
    mask_intervalo = (theta_deg >= THETA_INICIO) & (theta_deg <= THETA_FIM)
    idx_candidatos = np.where(mask_intervalo & (y_mm <= Y_ALVO_MM))[0]
    
    if len(idx_candidatos) > 0:
        idx_pico = idx_candidatos[0]
        theta_pico_deg = theta_deg[idx_pico]
    else:
        theta_pico_deg = THETA_FIM
        idx_pico = np.where(theta_deg == THETA_FIM)[0][0]
    
    # Constante k
    k = 134.10 * 6.17 * np.pi * (25.4 / 94.3)**2 / 1000.0
    
    # Construir F_VS
    F_VS_full = np.zeros_like(theta_deg, dtype=float)
    F_eq = k * (y_mm**2)
    
    # Parte crescente
    mask_cresc = (theta_deg >= THETA_INICIO) & (theta_deg <= theta_pico_deg)
    F_VS_full[mask_cresc] = F_eq[mask_cresc]
    
    # Valor máximo constante
    F_max_const = k * (Y_ALVO_MM**2)
    
    # Parte constante
    mask_const = (theta_deg > theta_pico_deg) & (theta_deg <= THETA_FIM)
    F_VS_full[mask_const] = F_max_const
    
    info = {
        'theta_inicio': THETA_INICIO,
        'theta_fim': THETA_FIM,
        'theta_pico': theta_pico_deg,
        'y_alvo_mm': Y_ALVO_MM,
        'k': k,
        'F_max': F_max_const
    }
    
    return F_VS_full, F_max_const, theta_pico_deg, info


# ========================================================================
# FUNÇÕES AUXILIARES
# ========================================================================

def calcular_forcas_completas(theta_deg: np.ndarray, r: float, L: float, h: float,
                              m_haste: float, m_biela: float, g: float,
                              F_VS: np.ndarray, omega: float) -> dict:
    """
    Calcula todas as forças e torque de uma vez.
    
    Parâmetros:
        theta_deg        : array de ângulos em graus
        r, L, h          : geometria (m)
        m_haste, m_biela : massas (kg)
        g                : aceleração da gravidade (m/s²)
        F_VS             : força vertical do solo (N)
        omega            : velocidade angular (rad/s)
    
    Retorna:
        dict com arrays: 'F_B', 'F_M', 'torque'
    """
    theta_rad = np.deg2rad(theta_deg)
    
    P_haste = m_haste * g
    P_biela = m_biela * g
    
    F_B, F_M = forcas_FB_FM(theta_rad, r, L, h, m_haste, m_biela, 
                            P_haste, P_biela, F_VS, omega)
    
    tau = torque(theta_rad, r, L, h, m_haste, m_biela, 
                 P_haste, P_biela, F_VS, omega)
    
    return {
        'theta_deg': theta_deg,
        'theta_rad': theta_rad,
        'F_B': F_B,
        'F_M': F_M,
        'torque': tau
    }
