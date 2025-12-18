"""
Módulo de Visualização - Gráficos de Cinemática.

Funções para plotar posição, velocidade, aceleração e jerk da haste.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path


def _configurar_eixo_x(ax):
    """Configura eixo X com marcadores a cada 45 graus."""
    ax.set_xticks(np.arange(0, 361, 45))
    ax.set_xlabel("θ (graus)", fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3)


def _adicionar_linhas_contato(ax, theta_descida, theta_subida):
    """Adiciona linhas verticais indicando contato com solo."""
    ax.axvline(x=theta_descida, color='green', linestyle=':', linewidth=1.5, 
               label=f'Toque solo (descida): {theta_descida:.1f}°', alpha=0.7)
    ax.axvline(x=theta_subida, color='orange', linestyle=':', linewidth=1.5, 
               label=f'Saída solo (subida): {theta_subida:.1f}°', alpha=0.7)


def plotar_posicao(theta_deg, y_mm, theta_solo, output_dir='output/images', 
                   mostrar=False, salvar=True):
    """
    Plota o gráfico de posição da haste em relação ao solo.
    
    Parâmetros:
        theta_deg   : array de ângulos (graus)
        y_mm        : posição em relação ao solo (mm)
        theta_solo  : dict com ângulos de contato {'descida': ..., 'subida': ...}
        output_dir  : diretório de saída
        mostrar     : se True, exibe o gráfico
        salvar      : se True, salva o gráfico
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Converter para metros se necessário
    use_metros = True
    y_plot = y_mm / 1000.0 if use_metros else y_mm
    unit = "m" if use_metros else "mm"
    
    ax.plot(theta_deg, y_plot, label="Posição da extremidade da haste",
            linewidth=2.5, color='blue')
    ax.axhline(y=0, color='brown', linestyle='--', linewidth=2,
               label='Nível do solo (y=0)', zorder=3)
    ax.axhline(y=-0.05 if use_metros else -50, color='red', linestyle='--',
               linewidth=2, label='Profundidade máxima (-50 mm)', zorder=3)
    
    _adicionar_linhas_contato(ax, theta_solo['descida'], theta_solo['subida'])
    
    ax.set_ylabel(f"Posição [{unit}]", fontsize=11, fontweight='bold')
    _configurar_eixo_x(ax)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)
    
    plt.tight_layout()
    
    if salvar:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        caminho = os.path.join(output_dir, 'grafico_posicao_haste.png')
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico salvo: {caminho}")
    
    if mostrar:
        plt.show()
    else:
        plt.close()


def plotar_velocidade(theta_deg, velocidades_dict, theta_solo, 
                      output_dir='output/images', mostrar=False, salvar=True):
    """
    Plota o gráfico de velocidade da haste para múltiplas culturas.
    
    Parâmetros:
        theta_deg        : array de ângulos (graus)
        velocidades_dict : dict {'cultura': {'velocidade': array, 'omega_rpm': float}}
        theta_solo       : dict com ângulos de contato
        output_dir       : diretório de saída
        mostrar          : se True, exibe o gráfico
        salvar           : se True, salva o gráfico
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    use_metros = True
    unit = "m/s" if use_metros else "mm/s"
    
    for cultura, dados in velocidades_dict.items():
        v = dados['velocidade']
        v_plot = v / 1000.0 if use_metros else v
        label = f"{cultura.capitalize()} ({dados['omega_rpm']:.0f} RPM)"
        ax.plot(theta_deg, v_plot, label=label, linewidth=2)
    
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=1, alpha=0.5)
    _adicionar_linhas_contato(ax, theta_solo['descida'], theta_solo['subida'])
    
    ax.set_ylabel(f"Velocidade [{unit}]", fontsize=11, fontweight='bold')
    _configurar_eixo_x(ax)
    ax.legend(loc="best", fontsize=9, framealpha=0.9, ncol=2)
    
    plt.tight_layout()
    
    if salvar:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        caminho = os.path.join(output_dir, 'grafico_velocidade_haste.png')
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico salvo: {caminho}")
    
    if mostrar:
        plt.show()
    else:
        plt.close()


def plotar_aceleracao(theta_deg, aceleracoes_dict, theta_solo, 
                      output_dir='output/images', mostrar=False, salvar=True):
    """
    Plota o gráfico de aceleração da haste para múltiplas culturas.
    
    Parâmetros:
        theta_deg         : array de ângulos (graus)
        aceleracoes_dict  : dict {'cultura': {'aceleracao': array, 'omega_rpm': float}}
        theta_solo        : dict com ângulos de contato
        output_dir        : diretório de saída
        mostrar           : se True, exibe o gráfico
        salvar            : se True, salva o gráfico
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    use_metros = True
    unit = "m/s²" if use_metros else "mm/s²"
    
    for cultura, dados in aceleracoes_dict.items():
        a = dados['aceleracao']
        a_plot = a / 1000.0 if use_metros else a
        label = f"{cultura.capitalize()} ({dados['omega_rpm']:.0f} RPM)"
        ax.plot(theta_deg, a_plot, label=label, linewidth=2)
    
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=1, alpha=0.5)
    _adicionar_linhas_contato(ax, theta_solo['descida'], theta_solo['subida'])
    
    ax.set_ylabel(f"Aceleração [{unit}]", fontsize=11, fontweight='bold')
    _configurar_eixo_x(ax)
    ax.legend(loc="best", fontsize=9, framealpha=0.9, ncol=2)
    
    plt.tight_layout()
    
    if salvar:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        caminho = os.path.join(output_dir, 'grafico_aceleracao_haste.png')
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico salvo: {caminho}")
    
    if mostrar:
        plt.show()
    else:
        plt.close()


def plotar_jerk(theta_deg, jerks_dict, theta_solo, 
                output_dir='output/images', mostrar=False, salvar=True):
    """
    Plota o gráfico de jerk da haste para múltiplas culturas.
    
    Parâmetros:
        theta_deg   : array de ângulos (graus)
        jerks_dict  : dict {'cultura': {'jerk': array, 'omega_rpm': float}}
        theta_solo  : dict com ângulos de contato
        output_dir  : diretório de saída
        mostrar     : se True, exibe o gráfico
        salvar      : se True, salva o gráfico
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    use_metros = True
    unit = "m/s³" if use_metros else "mm/s³"
    
    for cultura, dados in jerks_dict.items():
        j = dados['jerk']
        j_plot = j / 1000.0 if use_metros else j
        label = f"{cultura.capitalize()} ({dados['omega_rpm']:.0f} RPM)"
        ax.plot(theta_deg, j_plot, label=label, linewidth=2)
    
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=1, alpha=0.5)
    _adicionar_linhas_contato(ax, theta_solo['descida'], theta_solo['subida'])
    
    ax.set_ylabel(f"Jerk [{unit}]", fontsize=11, fontweight='bold')
    _configurar_eixo_x(ax)
    ax.legend(loc="best", fontsize=9, framealpha=0.9, ncol=2)
    
    plt.tight_layout()
    
    if salvar:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        caminho = os.path.join(output_dir, 'grafico_jerk_haste.png')
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico salvo: {caminho}")
    
    if mostrar:
        plt.show()
    else:
        plt.close()


def plotar_cinematica_completa(theta_deg, y_mm, velocidades_dict, 
                               aceleracoes_dict, jerks_dict, theta_solo,
                               output_dir='output/images', mostrar=False, salvar=True):
    """
    Plota todos os gráficos de cinemática em um grid 2x2.
    
    Parâmetros:
        theta_deg        : array de ângulos (graus)
        y_mm             : posição em relação ao solo (mm)
        velocidades_dict : dict com velocidades por cultura
        aceleracoes_dict : dict com acelerações por cultura
        jerks_dict       : dict com jerks por cultura
        theta_solo       : dict com ângulos de contato
        output_dir       : diretório de saída
        mostrar          : se True, exibe o gráfico
        salvar           : se True, salva o gráfico
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
    ax_y, ax_v = axes[0]
    ax_a, ax_j = axes[1]
    
    use_metros = True
    y_plot = y_mm / 1000.0 if use_metros else y_mm
    unit_len = "m" if use_metros else "mm"
    
    # Posição
    ax_y.plot(theta_deg, y_plot, linewidth=2, color='blue')
    ax_y.axhline(y=0, color='brown', linestyle='--', linewidth=1.5)
    ax_y.axhline(y=-0.05 if use_metros else -50, color='red', linestyle='--', linewidth=1.5)
    _adicionar_linhas_contato(ax_y, theta_solo['descida'], theta_solo['subida'])
    ax_y.set_title("Posição", fontweight='bold')
    ax_y.set_ylabel(f"[{unit_len}]")
    ax_y.grid(True, alpha=0.3)
    ax_y.legend(fontsize=7, loc='upper right')
    
    # Velocidade
    for cultura, dados in velocidades_dict.items():
        v_plot = dados['velocidade'] / 1000.0 if use_metros else dados['velocidade']
        ax_v.plot(theta_deg, v_plot, label=f"{cultura.capitalize()}", linewidth=1.5)
    ax_v.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    _adicionar_linhas_contato(ax_v, theta_solo['descida'], theta_solo['subida'])
    ax_v.set_title("Velocidade", fontweight='bold')
    ax_v.set_ylabel(f"[{unit_len}/s]")
    ax_v.grid(True, alpha=0.3)
    ax_v.legend(fontsize=7, ncol=2)
    
    # Aceleração
    for cultura, dados in aceleracoes_dict.items():
        a_plot = dados['aceleracao'] / 1000.0 if use_metros else dados['aceleracao']
        ax_a.plot(theta_deg, a_plot, label=f"{cultura.capitalize()}", linewidth=1.5)
    ax_a.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    _adicionar_linhas_contato(ax_a, theta_solo['descida'], theta_solo['subida'])
    ax_a.set_title("Aceleração", fontweight='bold')
    ax_a.set_ylabel(f"[{unit_len}/s²]")
    ax_a.set_xlabel("θ (graus)")
    ax_a.grid(True, alpha=0.3)
    ax_a.legend(fontsize=7, ncol=2)
    
    # Jerk
    for cultura, dados in jerks_dict.items():
        j_plot = dados['jerk'] / 1000.0 if use_metros else dados['jerk']
        ax_j.plot(theta_deg, j_plot, label=f"{cultura.capitalize()}", linewidth=1.5)
    ax_j.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    _adicionar_linhas_contato(ax_j, theta_solo['descida'], theta_solo['subida'])
    ax_j.set_title("Jerk", fontweight='bold')
    ax_j.set_ylabel(f"[{unit_len}/s³]")
    ax_j.set_xlabel("θ (graus)")
    ax_j.grid(True, alpha=0.3)
    ax_j.legend(fontsize=7, ncol=2)
    
    # Configurar eixo X para todos
    for ax in axes.flat:
        ax.set_xticks(np.arange(0, 361, 45))
    
    plt.tight_layout()
    
    if salvar:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        caminho = os.path.join(output_dir, 'grafico_cinematica_completo.png')
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico consolidado salvo: {caminho}")
    
    if mostrar:
        plt.show()
    else:
        plt.close()
