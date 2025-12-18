"""
Módulo de Visualização - Gráficos de Torque e Forças.

Funções para plotar torque no eixo e forças na biela/manivela.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path


def plotar_torque(theta_deg, tau_vals, theta_range=None, F_VS_max=None,
                  output_dir='output/images', mostrar=False, salvar=True):
    """
    Plota o gráfico de torque no eixo da manivela.
    
    Parâmetros:
        theta_deg   : array de ângulos (graus)
        tau_vals    : array de torque (N·m)
        theta_range : tupla (theta_min, theta_max) para destacar região de F_VS
        F_VS_max    : valor máximo de F_VS para anotação
        output_dir  : diretório de saída
        mostrar     : se True, exibe o gráfico
        salvar      : se True, salva o gráfico
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.plot(theta_deg, tau_vals, label='Torque τ(θ)', lw=2, color='darkblue')
    
    # Destacar região de atuação de F_VS se fornecida
    if theta_range is not None:
        theta_min, theta_max = theta_range
        
        # Região de F_VS (amarela para visualizar melhor)
        ax.axvspan(theta_min, theta_max, alpha=0.15, color='yellow', 
                   label=f'Região F_VS: [{theta_min:.1f}°, {theta_max:.1f}°]', zorder=1)
    
    # Encontrar e marcar o torque máximo
    if not np.all(np.isnan(tau_vals)):
        idx_max = np.nanargmax(np.abs(tau_vals))
        tau_max = tau_vals[idx_max]
        tau_max_abs = np.abs(tau_max)
        theta_max_torque = theta_deg[idx_max]
        
        ax.scatter([theta_max_torque], [tau_max], color='red', s=80, zorder=5,
                   label=f'Máx: {tau_max:.2f} N·m em {theta_max_torque:.1f}°')
        ax.annotate(f'{tau_max:.4f} N·m', 
                    xy=(theta_max_torque, tau_max),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', color='red'))
    
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
    ax.set_xlim(0, 360)
    ax.set_xlabel("θ (graus)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Torque [N·m]", fontsize=11, fontweight='bold')
    ax.set_xticks(np.arange(0, 361, 45))
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=9, framealpha=0.9)
    
    plt.tight_layout()
    
    if salvar:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        caminho = os.path.join(output_dir, 'grafico_torque.png')
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico salvo: {caminho}")
    
    if mostrar:
        plt.show()
    else:
        plt.close()


def plotar_forcas(theta_deg, F_B_vals, F_M_vals, theta_range=None,
                  output_dir='output/images', mostrar=False, salvar=True):
    """
    Plota os gráficos de forças F_B e F_M em um único gráfico.
    
    Parâmetros:
        theta_deg   : array de ângulos (graus)
        F_B_vals    : array de força na biela (N)
        F_M_vals    : array de força na manivela (N)
        theta_range : tupla (theta_min, theta_max) para destacar região de F_VS
        output_dir  : diretório de saída
        mostrar     : se True, exibe o gráfico
        salvar      : se True, salva o gráfico
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plotar ambas as forças
    ax.plot(theta_deg, F_B_vals, lw=2, label=r'$F_B(\theta)$', color='darkgreen')
    ax.plot(theta_deg, F_M_vals, lw=2, label=r'$F_M(\theta)$', color='darkred')
    
    # Máximos em módulo
    idx_FB_max = np.nanargmax(np.abs(F_B_vals))
    FB_max = F_B_vals[idx_FB_max]
    FB_max_abs = np.abs(FB_max)
    theta_FB_max_deg = theta_deg[idx_FB_max]
    
    idx_FM_max = np.nanargmax(np.abs(F_M_vals))
    FM_max = F_M_vals[idx_FM_max]
    FM_max_abs = np.abs(FM_max)
    theta_FM_max_deg = theta_deg[idx_FM_max]
    
    ax.scatter([theta_FB_max_deg], [FB_max], zorder=5, s=80, color='darkgreen',
               label=fr'Máx $F_B$: {FB_max_abs:.1f} N em {theta_FB_max_deg:.1f}°')
    ax.scatter([theta_FM_max_deg], [FM_max], zorder=5, s=80, color='darkred',
               label=fr'Máx $F_M$: {FM_max_abs:.1f} N em {theta_FM_max_deg:.1f}°')
    
    # Destacar região de F_VS
    if theta_range is not None:
        theta_min, theta_max = theta_range
        ax.axvspan(theta_min, theta_max, alpha=0.15, color='yellow', 
                   label=f'F_VS crescente', zorder=1)
    
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
    ax.set_xlim(0, 360)
    ax.set_xlabel(r'$\theta$ (graus)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Força (N)', fontsize=11, fontweight='bold')
    ax.set_xticks(np.arange(0, 361, 45))
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=9, framealpha=0.9)
    
    plt.tight_layout()
    
    if salvar:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        caminho = os.path.join(output_dir, 'grafico_forcas_FB_FM.png')
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico salvo: {caminho}")
    
    if mostrar:
        plt.show()
    else:
        plt.close()
