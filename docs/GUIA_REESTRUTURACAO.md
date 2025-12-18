# 📘 GUIA DE REESTRUTURAÇÃO DO PROJETO

## 🎯 Resumo das Mudanças

Seu projeto de TCC foi **completamente reorganizado** com uma arquitetura profissional, modular e escalável.

---

## 🏗️ Nova Estrutura

### **Antes (Código Antigo)**
```
dados/
├── espacamento.py              # Código misturado
├── graficos_cinematica.py      # Código misturado
├── ibge_graos.py               # Código misturado
├── torque.py                   # Código misturado
├── config/
└── utils/
    ├── cinematica.py
    └── load.py
```

### **Depois (Código Novo)**
```
dados/
├── main.py                     # ✨ NOVO: Interface CLI principal
├── exemplo_uso.py              # ✨ NOVO: Exemplos de uso
├── README.md                   # ✨ NOVO: Documentação completa
├── requirements.txt            # ✨ NOVO: Dependências
│
├── config/                     # Configurações (mantido)
│   ├── config.yaml
│   └── culturas.yaml
│
├── core/                       # ✨ NOVO: Lógica de negócio
│   ├── cinematica.py          # Funções consolidadas
│   ├── forcas_torque.py       # Cálculos de torque
│   └── espacamento.py         # Espaçamento de sementes
│
├── data/                       # ✨ NOVO: Processamento de dados
│   └── ibge_loader.py         # Dados IBGE
│
├── visualization/              # ✨ NOVO: Todos os gráficos
│   ├── plot_cinematica.py
│   ├── plot_torque.py
│   ├── plot_espacamento.py
│   └── plot_ibge.py
│
├── utils/                      # Utilitários (refatorado)
│   └── config_loader.py       # Carregamento de configs
│
└── output/                     # ✨ NOVO: Saídas organizadas
    └── images/
```

---

## 📋 Principais Melhorias

### 1. **Separação de Responsabilidades**
- ✅ **Cálculos** → `core/`
- ✅ **Visualização** → `visualization/`
- ✅ **Dados** → `data/`
- ✅ **Configuração** → `utils/config_loader.py`

### 2. **Eliminação de Duplicação**
- ❌ Antes: Mesmas funções em múltiplos arquivos
- ✅ Agora: Funções únicas e reutilizáveis

### 3. **Interface Unificada**
- ❌ Antes: Scripts isolados, difícil de usar
- ✅ Agora: `main.py` com menu interativo

### 4. **Documentação**
- ❌ Antes: Sem documentação
- ✅ Agora: README completo, docstrings, exemplos

### 5. **Modularidade**
- ❌ Antes: Código monolítico
- ✅ Agora: Módulos independentes e testáveis

---

## 🚀 Como Começar

### Opção 1: Interface CLI (Recomendado)

```bash
python main.py
```

**Menu interativo com todas as funcionalidades:**
- Análise cinemática
- Cálculo de torque
- Distribuição de sementes
- Dados IBGE

### Opção 2: Uso Programático

```bash
python exemplo_uso.py
```

**Executa exemplos de todos os módulos.**

### Opção 3: Importar Módulos

```python
from core import cinematica as cin
from visualization import plot_cinematica

# Seu código aqui
```

---

## 📦 Instalação das Dependências

```bash
pip install -r requirements.txt
```

**Dependências principais:**
- numpy, scipy (cálculos)
- matplotlib (gráficos)
- pandas (dados)
- pyyaml (configuração)

---

## 🔄 Mapeamento de Funcionalidades

### Cinemática

| Função Antiga | Nova Localização | Módulo |
|--------------|------------------|---------|
| `espaco()` | `core.cinematica.espaco()` | `core/cinematica.py` |
| `velocidade()` | `core.cinematica.velocidade()` | `core/cinematica.py` |
| `aceleracao()` | `core.cinematica.aceleracao()` | `core/cinematica.py` |
| `jerk()` | `core.cinematica.jerk()` | `core/cinematica.py` |

### Torque e Forças

| Função Antiga | Nova Localização | Módulo |
|--------------|------------------|---------|
| `torque()` | `core.forcas_torque.torque()` | `core/forcas_torque.py` |
| `forcas_FB_FM()` | `core.forcas_torque.forcas_FB_FM()` | `core/forcas_torque.py` |

### Espaçamento

| Função Antiga | Nova Localização | Módulo |
|--------------|------------------|---------|
| `quantidade()` | `core.espacamento.sementes_por_metro()` | `core/espacamento.py` |

### Visualização

| Script Antigo | Nova Localização | Módulo |
|--------------|------------------|---------|
| `graficos_cinematica.py` | `visualization/plot_cinematica.py` | Múltiplas funções |
| `espacamento.py` (plot) | `visualization/plot_espacamento.py` | `plotar_distribuicao_sementes()` |
| `ibge_graos.py` (plots) | `visualization/plot_ibge.py` | Múltiplas funções |

### Dados

| Script Antigo | Nova Localização | Módulo |
|--------------|------------------|---------|
| `ibge_graos.py` (dados) | `data/ibge_loader.py` | Múltiplas funções |

### Configuração

| Script Antigo | Nova Localização | Módulo |
|--------------|------------------|---------|
| `utils/load.py` | `utils/config_loader.py` | Refatorado |

---

## 📊 Exemplos de Uso

### Exemplo 1: Análise Cinemática

```python
from core import cinematica as cin
import numpy as np

# Parâmetros
r, L, h = 84.01, 210.0, 347.46  # mm
theta = np.deg2rad(np.arange(0, 361))
omega = 20.0  # rad/s

# Calcular
y = cin.espaco(theta, r, L, h)
v = cin.velocidade(theta, omega, r, L)

print(f"Posição máxima: {np.max(y):.2f} mm")
```

### Exemplo 2: Gerar Todos os Gráficos de Cinemática

```python
from visualization import plot_cinematica
from core import cinematica as cin
import numpy as np

# Preparar dados
theta_deg = np.arange(0, 361)
# ... (calcular dados)

# Plotar tudo de uma vez
plot_cinematica.plotar_cinematica_completa(
    theta_deg, y_solo, 
    velocidades_dict, aceleracoes_dict, jerks_dict,
    theta_solo, 
    output_dir='output/images',
    mostrar=True, 
    salvar=True
)
```

### Exemplo 3: Carregar Configuração

```python
from utils import config_loader

# Carregar culturas
culturas = config_loader.carregar_culturas()
print(culturas.keys())  # ['soja', 'milho', 'sorgo', ...]

# Extrair dados de uma cultura
faixas = config_loader.extrair_faixas_cultura('soja')
print(faixas)
# {'density_min': 250000, 'density_max': 400000, ...}
```

---

## 🎨 Gráficos Gerados

Todos os gráficos são salvos automaticamente em `output/images/`:

### Cinemática
- `grafico_posicao_haste.png`
- `grafico_velocidade_haste.png`
- `grafico_aceleracao_haste.png`
- `grafico_jerk_haste.png`
- `grafico_cinematica_completo.png` (4 em 1)

### Torque
- `grafico_torque.png`
- `grafico_forcas.png`

### Espaçamento
- `distribuicao_sementes.png`

### IBGE
- `area_culturas_brasil.png`
- `ranking_estados_*.png`
- `mapa_*_ha.png`

---

## ⚙️ Configuração

### Adicionar Nova Cultura

Edite `config/culturas.yaml`:

```yaml
crops:
  - name: "nova_cultura"
    row_spacing_m:
      options: [0.50, 0.70]
    plant_density_per_hectare:
      min: 100000
      max: 200000
      step: 10000
    planting_speed_kmh:
      min: 4.0
      max: 6.0
      step: 0.5
    germination_rate:
      min: 0.80
      max: 0.90
      step: 0.01
```

### Modificar Parâmetros do Mecanismo

Edite `config/config.yaml`:

```yaml
mechanics:
  crank_radius_mm: 84.01
  rod_length_mm: 210.0
  offset_h_mm: 347.46
```

---

## 🔍 Verificação

### Testar a Instalação

```bash
# 1. Executar exemplos
python exemplo_uso.py

# 2. Verificar interface
python main.py

# 3. Testar importações
python -c "from core import cinematica; print('OK')"
```

### Estrutura Esperada

Execute para verificar:

```bash
python -c "import os; print('\n'.join([d for d in os.listdir('.') if os.path.isdir(d)]))"
```

**Saída esperada:**
```
config
core
data
output
utils
visualization
```

---

## 📝 Próximos Passos

1. ✅ **Instalação**: Execute `pip install -r requirements.txt`
2. ✅ **Teste**: Execute `python exemplo_uso.py`
3. ✅ **Explore**: Execute `python main.py`
4. ✅ **Documente**: Leia o `README.md` completo
5. ✅ **Personalize**: Ajuste `config/*.yaml` conforme necessário

---

## 💡 Dicas de Uso

### Para Desenvolvimento
```python
# Importar tudo de uma vez
from core import cinematica as cin, forcas_torque as ft, espacamento as esp
from visualization import plot_cinematica as pltcin
from utils import config_loader as cfg
```

### Para Análises Rápidas
```bash
# Use o menu interativo
python main.py
```

### Para Scripts Personalizados
```python
# Base seu código em exemplo_uso.py
# Copie e adapte as funções conforme necessário
```

---

## 🎓 Conclusão

Seu projeto agora está:

✅ **Organizado** - Estrutura clara e profissional  
✅ **Modular** - Fácil de manter e estender  
✅ **Documentado** - README completo e docstrings  
✅ **Testável** - Módulos independentes  
✅ **Escalável** - Fácil adicionar novas funcionalidades  
✅ **Profissional** - Padrões de indústria  

**Perfeito para apresentar no TCC!** 🎉

---

**Última atualização:** Dezembro 2025
