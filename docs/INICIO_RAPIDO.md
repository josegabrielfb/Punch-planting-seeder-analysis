# 🚀 INÍCIO RÁPIDO

## ⚡ Em 3 Passos

### 1️⃣ Instalar Dependências
```bash
pip install numpy scipy matplotlib pandas pyyaml unidecode
```

### 2️⃣ Executar o Sistema
```bash
python main.py
```

### 3️⃣ Escolher uma Análise
```
1. Análise Cinemática Completa
2. Análise de Torque e Forças
3. Distribuição de Sementes
4. Dados IBGE
```

---

## 📁 Estrutura Simplificada

```
dados/
├── main.py              ← Começe aqui! (Menu principal)
├── exemplo_uso.py       ← Exemplos práticos
│
├── core/                ← Cálculos principais
│   ├── cinematica.py
│   ├── forcas_torque.py
│   └── espacamento.py
│
├── visualization/       ← Gráficos
│   ├── plot_cinematica.py
│   ├── plot_torque.py
│   ├── plot_espacamento.py
│   └── plot_ibge.py
│
├── config/              ← Configurações
│   ├── config.yaml      ← Parâmetros do mecanismo
│   └── culturas.yaml    ← Dados das culturas
│
└── output/images/       ← Gráficos salvos aqui
```

---

## 💻 Exemplos Rápidos

### Calcular Cinemática
```python
from core import cinematica as cin
import numpy as np

theta = np.deg2rad(np.arange(0, 361))
y = cin.espaco(theta, r=84.01, L=210.0, h=347.46)
print(f"Profundidade máxima: {np.min(y):.2f} mm")
```

### Gerar Gráfico
```python
from visualization import plot_cinematica

plot_cinematica.plotar_posicao(
    theta_deg, y_solo, theta_solo,
    output_dir='output/images',
    mostrar=True
)
```

### Carregar Configuração
```python
from utils import config_loader

culturas = config_loader.carregar_culturas()
print(list(culturas.keys()))
```

---

## 🎯 Comandos Úteis

```bash
# Menu principal
python main.py

# Exemplos práticos
python exemplo_uso.py

# Testar importação
python -c "from core import cinematica; print('✅ OK')"
```

---

## 📚 Documentação Completa

- **README.md** - Documentação detalhada
- **GUIA_REESTRUTURACAO.md** - Como foi reorganizado
- Este arquivo - Início rápido

---

## ❓ Problemas Comuns

### Erro de Importação
```bash
# Certifique-se de estar na pasta correta
cd c:\Projeto\dados
python main.py
```

### Módulo não encontrado
```bash
# Instale as dependências
pip install -r requirements.txt
```

### Gráfico não aparece
- Os gráficos são salvos em `output/images/`
- Use `mostrar=True` na função de plot para exibir

---

## 🎓 Para o TCC

### Análise Completa
1. Execute `python main.py`
2. Escolha opção **1** (Análise Cinemática)
3. Selecione "Todas as culturas"
4. Todos os gráficos serão salvos em `output/images/`

### Comparar Culturas
- Use opção **1** no menu
- Escolha "Todas as culturas"
- Gera gráfico comparativo 4-em-1

### Dados para Apresentação
- Opção **4** para dados do IBGE
- Gera mapas e gráficos de área plantada

---

## ✅ Checklist de Verificação

- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] `python main.py` funciona
- [ ] Pasta `output/images/` foi criada
- [ ] Consegue gerar pelo menos um gráfico
- [ ] Leu o README.md

---

**Pronto para começar!** 🎉

Para mais detalhes, veja **README.md** e **GUIA_REESTRUTURACAO.md**.
