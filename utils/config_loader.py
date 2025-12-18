"""
Módulo de Carregamento de Configurações.

Funções para ler e processar arquivos YAML de configuração do projeto.
"""

from typing import Dict, Any
import yaml
import unicodedata
from pathlib import Path


# Caminhos padrão dos arquivos de configuração
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
CAMINHO_CONFIG_YAML = CONFIG_DIR / "config.yaml"
CAMINHO_CULTURAS_YAML = CONFIG_DIR / "culturas.yaml"


def normalizar_nome(s: str) -> str:
    """
    Normaliza acentos e caixa para comparação segura.
    
    Parâmetros:
        s : string a normalizar
    
    Retorna:
        string normalizada (sem acentos, minúsculas)
    """
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s.strip().lower()


def carregar_config(caminho_arquivo: str = None) -> Dict[str, Any]:
    """
    Carrega o arquivo config.yaml com parâmetros do mecanismo.
    
    Parâmetros:
        caminho_arquivo : caminho do arquivo (usa padrão se None)
    
    Retorna:
        dicionário com configurações
    """
    if caminho_arquivo is None:
        caminho_arquivo = CAMINHO_CONFIG_YAML
    
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    return config


def carregar_culturas(caminho_arquivo: str = None) -> Dict[str, Dict[str, Any]]:
    """
    Lê o YAML de culturas e retorna um dicionário indexado pelo nome da cultura.
    
    Estrutura de retorno:
    {
      "soja": {
        "row_spacing_m": [0.45, 0.50],
        "plant_density_per_hectare": {"min": 250000, "max": 400000, "step": 25000},
        "planting_speed_kmh": {"min": 5.0, "max": 7.0, "step": 0.5},
        "germination_rate": {"min": 0.85, "max": 0.95, "step": 0.01}
      },
      ...
    }
    
    Parâmetros:
        caminho_arquivo : caminho do arquivo (usa padrão se None)
    
    Retorna:
        dicionário de culturas
    """
    if caminho_arquivo is None:
        caminho_arquivo = CAMINHO_CULTURAS_YAML
    
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    if not isinstance(data, dict) or "crops" not in data or not isinstance(data["crops"], list):
        raise ValueError("Arquivo YAML inválido: esperava chave 'crops' contendo uma lista.")
    
    out: Dict[str, Dict[str, Any]] = {}
    for item in data["crops"]:
        if not isinstance(item, dict) or "name" not in item:
            continue
        name = normalizar_nome(item["name"])
        
        # Normaliza o espaçamento entre linhas para uma lista simples
        row_spacing = item.get("row_spacing_m", {})
        if isinstance(row_spacing, dict) and "options" in row_spacing:
            row_spacing_list = [float(x) for x in row_spacing["options"]]
        elif isinstance(row_spacing, list):
            row_spacing_list = [float(x) for x in row_spacing]
        else:
            row_spacing_list = []
        
        out[name] = {
            "row_spacing_m": row_spacing_list,
            "plant_density_per_hectare": item.get("plant_density_per_hectare", {}),
            "planting_speed_kmh": item.get("planting_speed_kmh", {}),
            "germination_rate": item.get("germination_rate", {}),
        }
    
    if not out:
        raise ValueError("Nenhuma cultura válida encontrada no YAML.")
    
    return out


def extrair_faixas_cultura(cultura: str) -> Dict[str, float]:
    """
    Extrai as faixas de densidade e germinação de uma cultura específica.
    
    Parâmetros:
        cultura : nome da cultura
    
    Retorna:
        dict com:
            "density_min": float,
            "density_max": float,
            "germ_min": float,
            "germ_max": float,
    """
    culturas = carregar_culturas()
    
    key = normalizar_nome(cultura)
    if key not in culturas:
        raise ValueError(f"Cultura '{cultura}' não encontrada. Disponíveis: {list(culturas.keys())}")
    
    dens = culturas[key].get("plant_density_per_hectare", {})
    germ = culturas[key].get("germination_rate", {})
    
    for nome, bloco in (("plant_density_per_hectare", dens), ("germination_rate", germ)):
        if not all(k in bloco for k in ("min", "max")):
            raise ValueError(f"Cultura '{cultura}': bloco '{nome}' precisa ter chaves 'min' e 'max'.")
    
    return {
        "density_min": float(dens["min"]),
        "density_max": float(dens["max"]),
        "germ_min": float(germ["min"]),
        "germ_max": float(germ["max"]),
    }


def velocidade_maxima_cultura(cultura: str) -> float:
    """
    Retorna a velocidade máxima de plantio (km/h) para a cultura informada.
    
    Parâmetros:
        cultura : nome da cultura
    
    Retorna:
        velocidade máxima em km/h
    """
    culturas = carregar_culturas()
    
    key = normalizar_nome(cultura)
    if key not in culturas:
        raise ValueError(f"Cultura '{cultura}' não encontrada.")
    
    speed = culturas[key].get("planting_speed_kmh", {})
    if "max" not in speed:
        raise ValueError(f"Cultura '{cultura}': sem chave 'max' em 'planting_speed_kmh'.")
    
    return float(speed["max"])
