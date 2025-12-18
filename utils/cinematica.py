import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import fsolve
from . import load


def espaco(theta: int, r: float, L: float, h: float) -> float:
    """
    Calcula a posição y da haste de perfuração em função do ângulo theta da biela.
    """

    y = np.sqrt(L**2 - (r * np.sin(theta))**2) - r * np.cos(theta) + h
    return y


def velocidade(theta: int, omega: float, r: float, L: float) -> float:
    """
    Calcula a velocidade da haste de perfuração em função do ângulo theta da biela.
    """

    dy_dt = r * np.sin(theta) * (1 - (r * np.cos(theta))/(np.sqrt(L**2 - r**2 * np.sin(theta)**2))) * omega

    return dy_dt 


def aceleracao(theta: int, omega: float, r: float, L: float, alpha: float) -> float:
    """
    Calcula a aceleração da haste de perfuração em função do ângulo theta da biela.
    """

    d2y_dt2 = (r * np.cos(theta) 
               - (r**2 * 
                  (4 * (L**2 - (r*np.sin(theta))**2) * np.cos(2*theta) + (r*np.sin(2*theta))**2)) / 
                  (4 * np.power((L**2 - (r*np.sin(theta))**2), 1.5))) * omega**2 + velocidade(theta, omega, r, L) * alpha
    
    return d2y_dt2


def jerk(theta: int, omega: float, alpha: float, r: float, L: float, beta: float) -> float:
    """
    Calcula o jerk da haste de perfuração em função do ângulo theta da biela.
    """

    d3y_dt3 = ((r**2 * np.sin(2*theta) * (16 * (L**2 - (r*np.sin(theta))**2)**2 - 
                                          3 * r**2 * (4 * 
                                                      (L**2 - (r*np.sin(theta))**2) *np.cos(2*theta) + 
                                                      (r*np.sin(2*theta))**2))) / 
               (8 * np.power((L**2 - (r*np.sin(theta))**2), 2.5))) * omega**3 
    + 3 * aceleracao(theta, omega, alpha, r, L) * omega *alpha 
    + velocidade(theta, omega, r, L) * beta
    
    return d3y_dt3


def sementes_por_metro(plantas_min: int, plantas_max: int, rendimento_min: int, rendimento_max: int) -> float:
    """
    Define a quantidade de sementes por metro linear com base na densidade de plantio e rendimento.
    """

    N = ((plantas_min + plantas_max) / 40000) / ((rendimento_min + rendimento_max) / 2)

    return N


def velocidade_angular(cultura: str) -> float:
    """
    Calcula a velocidade angular de rotação da biela de acordo com a velocidade do trator e a cultura escolhida.

    Onde: 
    vt: Velocidade do trator em km/h
    cultura: Nome da cultura (ex: "soja", "milho", etc.)
    """

    cultura = load._norm(cultura)

    vt = load.velocidade_maxima_cultura(cultura)

    faixas = load.extrair_faixas_cultura(cultura)

    N = sementes_por_metro(faixas["density_min"], faixas["density_max"], faixas["germ_min"], faixas["germ_max"])

    omega = 2 * np.pi * vt * N / 3.6

    return omega

def omega_rpm(omega: float) -> float:
    """
    Retorna a velocidade angular em rotações por minuto (RPM) para a cultura informada.
    """

    omega_rpm = omega * 60 / (2 * np.pi)

    return omega_rpm

def encontrar_theta_solo_preciso(r, L, h, altura_centro=591.47):
    """
    Encontra θ quando y=0 usando método numérico de Newton-Raphson.

    Args:
        r: raio da manivela (mm)
        L: comprimento da biela (mm)
        h: altura da haste (mm)
        altura_centro: altura do centro da manivela em relação ao solo (mm)

    Returns:
        dict: {'descida': θ1, 'subida': θ2} em graus
    """

    def equacao(theta):
        """Equação a resolver: y_solo(θ) = 0"""

        y_original = np.sqrt(L**2 - (r * np.sin(theta))**2) - r * np.cos(theta) + h
        y_solo = altura_centro - y_original

        return y_solo
    # Chute inicial 1: entre 90° e 180° (descida)

    theta_descida_rad = fsolve(equacao, np.deg2rad(135))[0]
    theta_descida_deg = np.rad2deg(theta_descida_rad) % 360

    # Chute inicial 2: entre 180° e 270° (subida)

    theta_subida_rad = fsolve(equacao, np.deg2rad(225))[0]
    theta_subida_deg = np.rad2deg(theta_subida_rad) % 360

    return {
        'descida': theta_descida_deg,
        'descida_rad': theta_descida_rad,
        'subida': theta_subida_deg,
        'subida_rad': theta_subida_rad
    }