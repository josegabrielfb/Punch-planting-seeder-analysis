"""
Módulo de Visualização - Gráficos de Espaçamento de Sementes.

Funções para plotar a distribuição de sementes por cultura.
"""

import matplotlib.pyplot as plt
import os
from pathlib import Path


def plotar_distribuicao_sementes(espacamentos_dict, distancia_metros=3.0,
                                 output_dir='output/images', mostrar=False, salvar=True):
    """
    Plota a distribuição de sementes para múltiplas culturas.
    
    Parâmetros:
        espacamentos_dict : dict com dados de espaçamento por cultura
                           (resultado de calcular_espacamento_culturas)
        distancia_metros  : distância total em metros
        output_dir        : diretório de saída
        mostrar           : se True, exibe o gráfico
        salvar            : se True, salva o gráfico
    """
    culturas_ordenadas = sorted(espacamentos_dict.keys())
    n_culturas = len(culturas_ordenadas)
    
    fig, ax = plt.subplots(figsize=(12, 4))
    
    margem_texto = 0.3  # margem à direita para o texto
    
    for i, cultura in enumerate(culturas_ordenadas):
        dados = espacamentos_dict[cultura]
        posicoes = dados['posicoes_m']
        sementes_por_m = dados['sementes_por_metro']
        
        y = [i] * len(posicoes)
        ax.scatter(posicoes, y, s=25)
        
        # Exibir o valor de sementes por metro no final da linha
        ax.text(distancia_metros + 0.1, i, 
                f"{sementes_por_m:.1f} sem/m", 
                va='center', fontsize=11)
    
    # Ajustar limites do eixo X para incluir o texto
    ax.set_xlim(0, distancia_metros + margem_texto)
    ax.set_yticks(range(n_culturas))
    ax.set_yticklabels([c.capitalize() for c in culturas_ordenadas], fontsize=11)
    ax.set_xlabel("Distância (m)", fontsize=11, fontweight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    
    if salvar:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        caminho = os.path.join(output_dir, 'distribuicao_sementes.png')
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico salvo: {caminho}")
    
    if mostrar:
        plt.show()
    else:
        plt.close()
