# 🧪 Testes e Exemplos

Esta pasta contém scripts de teste e exemplos de uso do sistema.

## 📄 Arquivos Disponíveis

### [`exemplo_uso.py`](exemplo_uso.py)
**Exemplos Completos de Uso do Sistema**

Menu interativo com 7 exemplos:
1. Análise Cinemática Básica
2. Comparação entre Culturas
3. Torque com F_VS Variável
4. Distribuição de Sementes
5. Carregamento de Configurações
6. Dados IBGE (opcional)
7. Geração de Gráficos

**Como executar:**
```bash
cd tests
python exemplo_uso.py
```

---

### [`test_cinematica.py`](test_cinematica.py)
**Teste Completo de Cinemática**

Testa todas as funções de cinemática:
- ✅ Posição da haste
- ✅ Ângulos de contato com o solo
- ✅ Velocidade
- ✅ Aceleração
- ✅ Jerk
- ✅ Velocidade angular por cultura
- ✅ Geração de gráficos

**Como executar:**
```bash
cd tests
python test_cinematica.py
```

**Resultados esperados:**
- Profundidade máxima: -47.15 mm
- θ descida: 123.28°
- θ subida: 236.72°
- Velocidade máxima: ~2841 mm/s
- Aceleração máxima: ~95823 mm/s²

---

### [`test_torque.py`](test_torque.py)
**Teste Completo de Torque e Forças**

Testa o modelo completo de torque:
- ✅ Construção do F_VS variável
- ✅ Cálculo de forças (F_B e F_M)
- ✅ Cálculo de torque
- ✅ Validação com valores esperados
- ✅ Comparação entre modelos F_VS
- ✅ Geração de gráficos

**Como executar:**
```bash
cd tests
python test_torque.py
```

**Resultados esperados:**
- F_VS máximo: 419.25 N
- θ pico: 168.00°
- F_B máximo: 361.65 N
- F_M máximo: 373.84 N
- Torque máximo: 12.0015 N·m

---

## 🚀 Execução Rápida

### Teste Individual

```bash
# Teste de cinemática
python tests/test_cinematica.py

# Teste de torque
python tests/test_torque.py

# Exemplos de uso
python tests/exemplo_uso.py
```

### Executar Todos os Testes

```bash
# Windows
cd tests
python test_cinematica.py; python test_torque.py

# Linux/Mac
cd tests
python test_cinematica.py && python test_torque.py
```

---

## 📊 Saídas dos Testes

### Gráficos Gerados

Os testes podem gerar gráficos em:
```
output/images/tests/
├── grafico_posicao_haste.png
├── grafico_velocidade_haste.png
├── grafico_aceleracao_haste.png
├── grafico_jerk_haste.png
├── grafico_cinematica_completo.png
├── grafico_torque.png
└── grafico_forcas_FB_FM.png
```

### Saída no Terminal

Cada teste exibe:
- ✅ Parâmetros utilizados
- 📊 Resultados calculados
- 🔍 Validação (valores esperados)
- ⚠️  Avisos se houver divergências

---

## ✅ Validação

### Test Cinematica

| Parâmetro | Valor Esperado | Status |
|-----------|----------------|--------|
| Profundidade máxima | -47.15 mm | ✅ |
| θ descida | 123.28° | ✅ |
| θ subida | 236.72° | ✅ |

### Test Torque

| Parâmetro | Valor Esperado | Status |
|-----------|----------------|--------|
| F_VS máximo | 419.25 N | ✅ |
| θ pico | 168.00° | ✅ |
| F_B máximo | 361.65 N | ✅ |
| F_M máximo | 373.84 N | ✅ |
| Torque máximo | 12.0015 N·m | ✅ |

---

## 🔧 Personalização

### Modificar Parâmetros

Edite as constantes no início de cada arquivo:

```python
# test_cinematica.py ou test_torque.py
R_MM = 84.01              # Raio da manivela
L_MM = 210.0              # Comprimento da biela
H_MM = 347.46             # Altura da haste
ALTURA_CENTRO_MM = 591.47 # Altura do centro
OMEGA_TESTE = 20.0        # Velocidade angular
```

### Adicionar Novos Testes

Siga o modelo dos arquivos existentes:

```python
# Seu novo teste
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import cinematica as cin
# ... seu código
```

---

## 📖 Documentação Adicional

- **README principal:** [`../README.md`](../README.md)
- **Início Rápido:** [`../docs/INICIO_RAPIDO.md`](../docs/INICIO_RAPIDO.md)
- **Guia de Reestruturação:** [`../docs/GUIA_REESTRUTURACAO.md`](../docs/GUIA_REESTRUTURACAO.md)
- **TCC completo:** [https://repositorio.ufsc.br/handle/123456789/270766](https://repositorio.ufsc.br/handle/123456789/270766)

---

## 💡 Dicas

1. **Execute os testes após modificar o código** para validar as mudanças
2. **Use `exemplo_uso.py`** para aprender a usar cada módulo
3. **Gere os gráficos** para visualizar os resultados
4. **Compare com valores esperados** para garantir precisão
5. **Consulte o TCC** para entender a teoria por trás dos cálculos

---

**Última atualização:** Dezembro 2025
