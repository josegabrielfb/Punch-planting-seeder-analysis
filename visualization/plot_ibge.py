"""
Módulo de Visualização - Gráficos de Dados do IBGE.

Funções para plotar dados de produção agrícola.
"""

import matplotlib.pyplot as plt
import os
from pathlib import Path


def plotar_area_culturas(tabela_sintese, output_dir='output/images', 
                        mostrar=False, salvar=True):
    """
    Plota gráfico de barras com área plantada por cultura.
    
    Parâmetros:
        tabela_sintese : DataFrame com dados de síntese
        output_dir     : diretório de saída
        mostrar        : se True, exibe o gráfico
        salvar         : se True, salva o gráfico
    """
    fig, ax = plt.subplots(figsize=(9, 5))
    tabela_sintese.plot(x="Produtos", y="Área plantada (Hectares)", 
                       kind="bar", ax=ax, legend=False)
    ax.set_xlabel("Cultura", fontsize=11, fontweight='bold')
    ax.set_ylabel("Área plantada (ha)", fontsize=11, fontweight='bold')
    ax.set_title("Área plantada por cultura – Brasil", fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if salvar:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        caminho = os.path.join(output_dir, 'area_culturas_brasil.png')
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico salvo: {caminho}")
    
    if mostrar:
        plt.show()
    else:
        plt.close()


def plotar_ranking_estados(top_df, cultura, output_dir='output/images',
                          mostrar=False, salvar=True):
    """
    Plota ranking de estados por área plantada de uma cultura.
    
    Parâmetros:
        top_df      : DataFrame com Estado e área (resultado de obter_top_estados)
        cultura     : nome da cultura
        output_dir  : diretório de saída
        mostrar     : se True, exibe o gráfico
        salvar      : se True, salva o gráfico
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    top_df.plot(x="Estado", y=cultura, kind="bar", ax=ax, legend=False, color='steelblue')
    ax.set_xlabel("Estado", fontsize=11, fontweight='bold')
    ax.set_ylabel(f"Área plantada de {cultura} (ha)", fontsize=11, fontweight='bold')
    ax.set_title(f"Top-{len(top_df)} estados – {cultura}", fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if salvar:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        nome_arquivo = f'ranking_estados_{cultura.lower()}.png'
        caminho = os.path.join(output_dir, nome_arquivo)
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico salvo: {caminho}")
    
    if mostrar:
        plt.show()
    else:
        plt.close()


def plotar_mapa_cultura(tabela_estados, cultura, scheme="Quantiles", k=5,
                       output_dir='output/images', mostrar=False, salvar=True):
    """
    Plota mapa coroplético por estado para uma cultura específica.
    
    Requer geopandas e geobr instalados.
    
    Parâmetros:
        tabela_estados : DataFrame com dados por estado
        cultura        : nome da cultura para plotar
        scheme         : esquema de classificação ("Quantiles", "FisherJenks", etc)
        k              : número de classes
        output_dir     : diretório de saída
        mostrar        : se True, exibe o gráfico
        salvar         : se True, salva o gráfico
    """
    try:
        import geopandas as gpd
        from geobr import read_state
        from unidecode import unidecode
    except ImportError:
        print("⚠ geopandas e/ou geobr não estão instalados. Mapa não será gerado.")
        return
    
    # Carregar shape dos estados
    br = read_state(year=2020)
    br["uf_norm"] = br["name_state"].apply(lambda x: unidecode(x).upper())
    
    # Juntar com dados
    g = br.merge(tabela_estados[["uf_norm", cultura]], on="uf_norm", how="left")
    g[cultura] = g[cultura].fillna(0)
    
    # Plotar
    fig, ax = plt.subplots(figsize=(7, 7))
    g.plot(column=cultura, ax=ax, scheme=scheme, k=k, legend=True,
           edgecolor="white", linewidth=0.3)
    ax.set_axis_off()
    ax.set_title(f"Área plantada de {cultura} (ha) por estado – Brasil",
                fontsize=12, fontweight='bold')
    plt.tight_layout()
    
    if salvar:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        nome_arquivo = f'mapa_{cultura.lower()}_ha.png'
        caminho = os.path.join(output_dir, nome_arquivo)
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"✓ Mapa salvo: {caminho}")
    
    if mostrar:
        plt.show()
    else:
        plt.close()


def plotar_mapa_total(tabela_estados, scheme="FisherJenks", k=5,
                     output_dir='output/images', mostrar=False, salvar=True):
    """
    Plota mapa coroplético por estado para área total plantada.
    
    Requer geopandas e geobr instalados.
    
    Parâmetros:
        tabela_estados : DataFrame com dados por estado
        scheme         : esquema de classificação
        k              : número de classes
        output_dir     : diretório de saída
        mostrar        : se True, exibe o gráfico
        salvar         : se True, salva o gráfico
    """
    try:
        import geopandas as gpd
        from geobr import read_state
        from unidecode import unidecode
    except ImportError:
        print("⚠ geopandas e/ou geobr não estão instalados. Mapa não será gerado.")
        return
    
    # Carregar shape dos estados
    br = read_state(year=2020)
    br["uf_norm"] = br["name_state"].apply(lambda x: unidecode(x).upper())
    
    # Juntar com dados
    g = br.merge(tabela_estados[["uf_norm", "Total"]], on="uf_norm", how="left")
    g["Total"] = g["Total"].fillna(0)
    
    # Plotar
    fig, ax = plt.subplots(figsize=(7, 7))
    g.plot(column="Total", ax=ax, scheme=scheme, k=k, legend=True,
           edgecolor="white", linewidth=0.3)
    ax.set_axis_off()
    ax.set_title("Total de hectares plantados por estado (todas as culturas)",
                fontsize=12, fontweight='bold')
    plt.tight_layout()
    
    if salvar:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        caminho = os.path.join(output_dir, 'mapa_total_ha.png')
        plt.savefig(caminho, dpi=600, bbox_inches='tight')
        print(f"✓ Mapa salvo: {caminho}")
    
    if mostrar:
        plt.show()
    else:
        plt.close()
