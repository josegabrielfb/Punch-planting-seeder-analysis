"""
Módulo de Dados - Processamento e carregamento de dados externos.

Contém funções para trabalhar com dados do IBGE e outras fontes.
"""

from .ibge_loader import (
    carregar_dados_ibge,
    processar_tabela_sintese,
    processar_tabela_estados
)

__all__ = [
    'carregar_dados_ibge',
    'processar_tabela_sintese',
    'processar_tabela_estados',
]
