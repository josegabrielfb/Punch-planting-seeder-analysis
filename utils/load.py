from typing import Dict, Any
import yaml
import unicodedata

#CAMINHO_CULTURAS_YAML = "C:\\Users\\WZSXFK\\Desktop\\Estágio\\tcc-ctj\\Python\\config\\culturas.yaml"
CAMINHO_CULTURAS_YAML = "C:\\Users\\User\\OneDrive\\TCC\\Python\\config\\culturas.yaml"


def carregar_culturas_yaml(caminho_arquivo: str = CAMINHO_CULTURAS_YAML) -> Dict[str, Dict[str, Any]]:
    """
    Lê o YAML de culturas e retorna um dicionário indexado pelo nome da cultura (minúsculas).
    Estrutura de retorno (exemplo):
    {
      "soja": {
        "row_spacing_m": [0.45, 0.50],
        "plant_density_per_hectare": {"min": 250000, "max": 400000, "step": 25000},
        "planting_speed_kmh": {"min": 5.0, "max": 7.0, "step": 0.5},
        "germination_rate": {"min": 0.85, "max": 0.95, "step": 0.01}
      },
      ...
    }
    """

    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or "crops" not in data or not isinstance(data["crops"], list):
        raise ValueError("Arquivo YAML inválido: esperava chave 'crops' contendo uma lista.")

    out: Dict[str, Dict[str, Any]] = {}
    for item in data["crops"]:
        if not isinstance(item, dict) or "name" not in item:
            continue
        name = str(item["name"]).strip().lower()

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


def _norm(s: str) -> str:
    """Normaliza acentos e caixa para comparação segura."""
    
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s.strip().lower()


def extrair_faixas_cultura(cultura: str) -> Dict[str, float]:
    """
    Recebe o dicionário de culturas (saída de carregar_culturas_yaml) e o nome da cultura,
    e retorna um dicionário com min/max de densidade (ha) e de taxa de germinação.

    Retorno:
      {
        "density_min": float,
        "density_max": float,
        "germ_min": float,
        "germ_max": float,
      }
    """
    culturas = carregar_culturas_yaml()

    key = cultura.strip().lower()
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
    Retorna somente a velocidade máxima de plantio (km/h) para a cultura informada.
    Espera a chave EXACTA do dicionário carregado (ex.: 'soja', 'milho', 'feijao').

    Ex.: velocidade_maxima_cultura("soja") -> 7.0
    """
    culturas: Dict[str, Dict[str, Any]] = carregar_culturas_yaml()

    if cultura not in culturas:
        disponiveis = ", ".join(sorted(culturas.keys()))
        raise KeyError(f"Cultura '{cultura}' não encontrada. Disponíveis: {disponiveis}")

    bloco = culturas[cultura].get("planting_speed_kmh")
    if not isinstance(bloco, dict) or "max" not in bloco:
        raise ValueError(f"Cultura '{cultura}' sem 'planting_speed_kmh.max' válido no YAML.")

    try:
        return float(bloco["max"])
    except (TypeError, ValueError):
        raise ValueError(f"Valor 'max' inválido para 'planting_speed_kmh' de '{cultura}'.")