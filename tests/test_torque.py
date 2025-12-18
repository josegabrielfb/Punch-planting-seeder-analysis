"""
Teste de Análise de Torque e Forças
====================================

Este script testa o cálculo de torque e forças no mecanismo:
- Construção do modelo F_VS variável
- Cálculo de forças na biela (F_B) e manivela (F_M)
- Cálculo de torque no eixo
- Validação com valores esperados

Autor: José Gabriel Furlan De Barros
"""

import numpy as np
import sys
import os

# Adicionar o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import forcas_torque as ft
from visualization import plot_torque

# =============================================================================
# CONFIGURAÇÃO DOS PARÂMETROS
# =============================================================================

print("=" * 70)
print("TESTE DE TORQUE E FORÇAS - Dosador de Sementes")
print("=" * 70)

# Parâmetros geométricos (mm)
R_MM = 84.01
L_MM = 210.0
H_MM = 347.46
ALTURA_CENTRO_MM = 591.47

# Massas (kg)
M_HASTE_KG = 1.16094
M_BIELA_KG = 0.75022

# Aceleração da gravidade
G = 9.81

# Pesos (N)
P_HASTE = M_HASTE_KG * G
P_BIELA = M_BIELA_KG * G

# Velocidade angular de teste (rad/s)
OMEGA = 20.0

# Vetor de ângulos
theta_deg = np.linspace(0.0, 360.0, 361)
theta_rad = np.deg2rad(theta_deg)

print(f"\n📐 Parâmetros Geométricos:")
print(f"  r (raio da manivela):     {R_MM:.2f} mm")
print(f"  L (comprimento da biela): {L_MM:.2f} mm")
print(f"  h (altura da haste):      {H_MM:.2f} mm")
print(f"  Altura do centro:         {ALTURA_CENTRO_MM:.2f} mm")

print(f"\n⚖️  Massas:")
print(f"  m_haste:                  {M_HASTE_KG:.5f} kg ({P_HASTE:.2f} N)")
print(f"  m_biela:                  {M_BIELA_KG:.5f} kg ({P_BIELA:.2f} N)")

print(f"\n⚙️  Velocidade angular:       {OMEGA:.2f} rad/s (191 RPM)")

# =============================================================================
# TESTE 1: CONSTRUÇÃO DO MODELO F_VS VARIÁVEL
# =============================================================================

print("\n" + "-" * 70)
print("TESTE 1: MODELO F_VS VARIÁVEL")
print("-" * 70)

print("\n🔧 Construindo F_VS variável...")

F_VS, F_max_const, theta_pico, info = ft.construir_F_VS_variavel(
    theta_deg, R_MM, L_MM, H_MM, ALTURA_CENTRO_MM
)

print(f"\n✓ F_VS construído com {len(F_VS)} pontos")

print(f"\n📊 Parâmetros do modelo:")
print(f"  θ início:    {info['theta_inicio']:.2f}°")
print(f"  θ pico:      {info['theta_pico']:.2f}°")
print(f"  θ fim:       {info['theta_fim']:.2f}°")
print(f"  F_VS máximo: {info['F_max']:.2f} N")
print(f"  y alvo:      {info['y_alvo_mm']:.2f} mm")
print(f"  k (const.):  {info['k']:.4f}")

# Validação dos valores esperados
print(f"\n🔍 Validação:")
esperado_theta_inicio = 123.28
esperado_theta_pico = 168.00
esperado_F_max = 419.25

diff_inicio = abs(info['theta_inicio'] - esperado_theta_inicio)
diff_pico = abs(info['theta_pico'] - esperado_theta_pico)
diff_fmax = abs(info['F_max'] - esperado_F_max)

if diff_inicio < 0.5 and diff_pico < 1.0 and diff_fmax < 1.0:
    print(f"  ✅ θ início correto ({info['theta_inicio']:.2f}° ≈ {esperado_theta_inicio}°)")
    print(f"  ✅ θ pico correto ({info['theta_pico']:.2f}° ≈ {esperado_theta_pico}°)")
    print(f"  ✅ F_max correto ({info['F_max']:.2f} N ≈ {esperado_F_max:.2f} N)")
else:
    print(f"  ⚠️  Valores divergem do esperado")
    print(f"     Δθ início: {diff_inicio:.2f}°")
    print(f"     Δθ pico: {diff_pico:.2f}°")
    print(f"     ΔF_max: {diff_fmax:.2f} N")

# Análise das regiões de F_VS
regioes = {
    'crescente': 0,
    'constante': 0,
    'zero': 0
}

for i, fvs in enumerate(F_VS):
    if fvs == 0:
        regioes['zero'] += 1
    elif fvs < info['F_max'] * 0.99:
        regioes['crescente'] += 1
    else:
        regioes['constante'] += 1

print(f"\n📊 Distribuição de F_VS:")
print(f"  Região crescente: {regioes['crescente']} pontos ({regioes['crescente']/len(F_VS)*100:.1f}%)")
print(f"  Região constante: {regioes['constante']} pontos ({regioes['constante']/len(F_VS)*100:.1f}%)")
print(f"  Região zero:      {regioes['zero']} pontos ({regioes['zero']/len(F_VS)*100:.1f}%)")

# =============================================================================
# TESTE 2: CÁLCULO DE FORÇAS
# =============================================================================

print("\n" + "-" * 70)
print("TESTE 2: FORÇAS NA BIELA E MANIVELA")
print("-" * 70)

# Converter para metros
r_m = R_MM / 1000.0
L_m = L_MM / 1000.0
h_m = H_MM / 1000.0

print("\n🔧 Calculando forças...")

F_B, F_M = ft.forcas_FB_FM(
    theta_rad, r_m, L_m, h_m,
    M_HASTE_KG, M_BIELA_KG,
    P_HASTE, P_BIELA, F_VS, OMEGA
)

print(f"✓ Forças calculadas: {len(F_B)} pontos")

# Estatísticas F_B
FB_max = np.max(np.abs(F_B))
idx_FB = np.argmax(np.abs(F_B))
theta_FB = theta_deg[idx_FB]
FB_max_val = F_B[idx_FB]

print(f"\n📊 Força na Biela (F_B):")
print(f"  F_B máximo (|F_B|): {FB_max:.2f} N")
print(f"    em θ = {theta_FB:.2f}° (F_B = {FB_max_val:.2f} N)")

# Estatísticas F_M
FM_max = np.max(np.abs(F_M))
idx_FM = np.argmax(np.abs(F_M))
theta_FM = theta_deg[idx_FM]
FM_max_val = F_M[idx_FM]

print(f"\n📊 Força na Manivela (F_M):")
print(f"  F_M máximo (|F_M|): {FM_max:.2f} N")
print(f"    em θ = {theta_FM:.2f}° (F_M = {FM_max_val:.2f} N)")

# Validação
esperado_FB = 361.65
esperado_FM = 373.84

diff_FB = abs(FB_max - esperado_FB)
diff_FM = abs(FM_max - esperado_FM)

print(f"\n🔍 Validação:")
if diff_FB < 1.0 and diff_FM < 1.0:
    print(f"  ✅ F_B correto ({FB_max:.2f} N ≈ {esperado_FB:.2f} N)")
    print(f"  ✅ F_M correto ({FM_max:.2f} N ≈ {esperado_FM:.2f} N)")
else:
    print(f"  ⚠️  Valores divergem do esperado")
    print(f"     ΔF_B: {diff_FB:.2f} N")
    print(f"     ΔF_M: {diff_FM:.2f} N")

# =============================================================================
# TESTE 3: CÁLCULO DE TORQUE
# =============================================================================

print("\n" + "-" * 70)
print("TESTE 3: TORQUE NO EIXO")
print("-" * 70)

print("\n🔧 Calculando torque...")

tau = ft.torque(
    theta_rad, r_m, L_m, h_m,
    M_HASTE_KG, M_BIELA_KG,
    P_HASTE, P_BIELA, F_VS, OMEGA
)

print(f"✓ Torque calculado: {len(tau)} pontos")

# Estatísticas
tau_max_abs = np.max(np.abs(tau))
idx_max = np.argmax(np.abs(tau))
tau_max = tau[idx_max]
theta_max = theta_deg[idx_max]

tau_min_abs = np.min(np.abs(tau))
tau_medio = np.mean(np.abs(tau))

print(f"\n📊 Torque:")
print(f"  Torque máximo (|τ|): {tau_max_abs:.4f} N·m")
print(f"    em θ = {theta_max:.2f}° (τ = {tau_max:.4f} N·m)")
print(f"  Torque médio (|τ|):  {tau_medio:.4f} N·m")
print(f"  Torque mínimo (|τ|): {tau_min_abs:.4f} N·m")

# Validação
esperado_tau = 12.0015

diff_tau = abs(tau_max_abs - esperado_tau)

print(f"\n🔍 Validação:")
if diff_tau < 0.01:
    print(f"  ✅ Torque correto ({tau_max_abs:.4f} N·m ≈ {esperado_tau:.4f} N·m)")
else:
    print(f"  ⚠️  Valor diverge do esperado")
    print(f"     Δτ: {diff_tau:.4f} N·m")

# =============================================================================
# TESTE 4: COMPARAÇÃO COM DIFERENTES MODELOS DE F_VS
# =============================================================================

print("\n" + "-" * 70)
print("TESTE 4: COMPARAÇÃO DE MODELOS F_VS")
print("-" * 70)

# Sem F_VS (zero)
F_VS_zero = np.zeros_like(theta_deg)
tau_zero = ft.torque(theta_rad, r_m, L_m, h_m,
                     M_HASTE_KG, M_BIELA_KG,
                     P_HASTE, P_BIELA, F_VS_zero, OMEGA)

# F_VS constante
F_VS_const = np.full_like(theta_deg, 200.0)  # 200 N constante
tau_const = ft.torque(theta_rad, r_m, L_m, h_m,
                      M_HASTE_KG, M_BIELA_KG,
                      P_HASTE, P_BIELA, F_VS_const, OMEGA)

# F_VS variável (já calculado)
tau_var = tau

print(f"\n📊 Comparação de torque máximo:")
print(f"  Sem F_VS (zero):      {np.max(np.abs(tau_zero)):.4f} N·m")
print(f"  F_VS constante (200N): {np.max(np.abs(tau_const)):.4f} N·m")
print(f"  F_VS variável:        {np.max(np.abs(tau_var)):.4f} N·m")

influencia = ((np.max(np.abs(tau_var)) - np.max(np.abs(tau_zero))) / 
              np.max(np.abs(tau_zero)) * 100)

print(f"\n🔍 Influência da F_VS variável:")
print(f"  Aumento de torque: {influencia:.1f}%")

# =============================================================================
# TESTE 5: GERAÇÃO DE GRÁFICOS
# =============================================================================

print("\n" + "-" * 70)
print("TESTE 5: GERAÇÃO DE GRÁFICOS")
print("-" * 70)

gerar_graficos = input("\nGerar gráficos de teste? (s/n): ").strip().lower()

if gerar_graficos == 's':
    output_dir = 'output/images/tests'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n🎨 Gerando gráficos em {output_dir}...")
    
    theta_range = (info['theta_inicio'], info['theta_fim'])
    
    # Plotar torque
    plot_torque.plotar_torque(
        theta_deg, tau, theta_range, F_max_const,
        output_dir, mostrar=False, salvar=True
    )
    
    # Plotar forças
    plot_torque.plotar_forcas(
        theta_deg, F_B, F_M, theta_range,
        output_dir, mostrar=False, salvar=True
    )
    
    print(f"✅ Gráficos salvos em {output_dir}/")

# =============================================================================
# RESUMO FINAL
# =============================================================================

print("\n" + "=" * 70)
print("RESUMO DO TESTE DE TORQUE E FORÇAS")
print("=" * 70)

print(f"\n✅ Todos os testes concluídos!")

print(f"\n📊 Resumo dos resultados:")
print(f"  • F_VS máximo:            {info['F_max']:.2f} N")
print(f"  • F_B máximo:             {FB_max:.2f} N")
print(f"  • F_M máximo:             {FM_max:.2f} N")
print(f"  • Torque máximo:          {tau_max_abs:.4f} N·m")
print(f"  • Influência da F_VS:     {influencia:.1f}% de aumento")

print(f"\n🔍 Status da validação:")
if diff_inicio < 0.5 and diff_pico < 1.0 and diff_fmax < 1.0:
    print(f"  ✅ Modelo F_VS: CORRETO")
else:
    print(f"  ⚠️  Modelo F_VS: VERIFICAR")

if diff_FB < 1.0 and diff_FM < 1.0:
    print(f"  ✅ Forças: CORRETAS")
else:
    print(f"  ⚠️  Forças: VERIFICAR")

if diff_tau < 0.01:
    print(f"  ✅ Torque: CORRETO")
else:
    print(f"  ⚠️  Torque: VERIFICAR")

print("\n" + "=" * 70)
print("Teste finalizado!")
print("=" * 70)
