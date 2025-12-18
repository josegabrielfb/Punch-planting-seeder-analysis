"""
Teste de Análise Cinemática Completa
=====================================

Este script testa todas as funções de cinemática do mecanismo:
- Posição (y)
- Velocidade (v)
- Aceleração (a)
- Jerk (j)
- Ângulos de contato com o solo
- Velocidade angular por cultura

Autor: José Gabriel Furlan De Barros
"""

import numpy as np
import sys
import os

# Adicionar o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import cinematica as cin
from visualization import plot_cinematica
from utils import config_loader

# =============================================================================
# CONFIGURAÇÃO DOS PARÂMETROS
# =============================================================================

print("=" * 70)
print("TESTE DE CINEMÁTICA - Dosador de Sementes")
print("=" * 70)

# Parâmetros geométricos (mm)
R_MM = 84.01
L_MM = 210.0
H_MM = 347.46
ALTURA_CENTRO_MM = 591.47

# Velocidade angular de teste (rad/s)
OMEGA_TESTE = 20.0

# Vetor de ângulos
theta_deg = np.arange(0, 361)
theta_rad = np.deg2rad(theta_deg)

print(f"\n📐 Parâmetros Geométricos:")
print(f"  r (raio da manivela):     {R_MM:.2f} mm")
print(f"  L (comprimento da biela): {L_MM:.2f} mm")
print(f"  h (altura da haste):      {H_MM:.2f} mm")
print(f"  Altura do centro:         {ALTURA_CENTRO_MM:.2f} mm")
print(f"\n⚙️  Velocidade de teste:      {OMEGA_TESTE:.2f} rad/s ({cin.omega_rpm(OMEGA_TESTE):.0f} RPM)")

# =============================================================================
# TESTE 1: POSIÇÃO DA HASTE
# =============================================================================

print("\n" + "-" * 70)
print("TESTE 1: POSIÇÃO DA HASTE")
print("-" * 70)

y_original = cin.espaco(theta_rad, R_MM, L_MM, H_MM)
y_solo = cin.y_solo_mm(theta_rad, R_MM, L_MM, H_MM, ALTURA_CENTRO_MM)

y_max = np.max(y_solo)
y_min = np.min(y_solo)
idx_max = np.argmax(y_solo)
idx_min = np.argmin(y_solo)

print(f"\n✓ Cálculo concluído: {len(y_solo)} pontos")
print(f"\n📊 Resultados:")
print(f"  Posição máxima:       {y_max:.2f} mm em θ = {theta_deg[idx_max]:.0f}°")
print(f"  Posição mínima:       {y_min:.2f} mm em θ = {theta_deg[idx_min]:.0f}°")
print(f"  Curso total:          {y_max - y_min:.2f} mm")
print(f"  Profundidade máxima:  {abs(y_min):.2f} mm abaixo do solo")

# =============================================================================
# TESTE 2: ÂNGULOS DE CONTATO COM O SOLO
# =============================================================================

print("\n" + "-" * 70)
print("TESTE 2: ÂNGULOS DE CONTATO COM O SOLO")
print("-" * 70)

theta_solo = cin.encontrar_theta_solo(R_MM, L_MM, H_MM, ALTURA_CENTRO_MM)

print(f"\n✓ Ângulos calculados:")
print(f"  θ descida (penetra): {theta_solo['descida']:.2f}°")
print(f"  θ subida (sai):      {theta_solo['subida']:.2f}°")
print(f"  Tempo no solo:       {theta_solo['subida'] - theta_solo['descida']:.2f}°")

# =============================================================================
# TESTE 3: VELOCIDADE DA HASTE
# =============================================================================

print("\n" + "-" * 70)
print("TESTE 3: VELOCIDADE DA HASTE")
print("-" * 70)

v = cin.velocidade(theta_rad, OMEGA_TESTE, R_MM, L_MM)

v_max = np.max(np.abs(v))
idx_v_max = np.argmax(np.abs(v))
v_max_val = v[idx_v_max]

print(f"\n✓ Cálculo concluído: {len(v)} pontos")
print(f"\n📊 Resultados:")
print(f"  Velocidade máxima (|v|): {v_max:.2f} mm/s")
print(f"    em θ = {theta_deg[idx_v_max]:.0f}° (v = {v_max_val:.2f} mm/s)")
print(f"  Velocidade em m/s:       {v_max / 1000:.2f} m/s")

# =============================================================================
# TESTE 4: ACELERAÇÃO DA HASTE
# =============================================================================

print("\n" + "-" * 70)
print("TESTE 4: ACELERAÇÃO DA HASTE")
print("-" * 70)

a = cin.aceleracao(theta_rad, OMEGA_TESTE, R_MM, L_MM, alpha=0)

a_max = np.max(np.abs(a))
idx_a_max = np.argmax(np.abs(a))
a_max_val = a[idx_a_max]

print(f"\n✓ Cálculo concluído: {len(a)} pontos")
print(f"\n📊 Resultados:")
print(f"  Aceleração máxima (|a|): {a_max:.2f} mm/s²")
print(f"    em θ = {theta_deg[idx_a_max]:.0f}° (a = {a_max_val:.2f} mm/s²)")
print(f"  Aceleração em m/s²:      {a_max / 1000:.2f} m/s²")
print(f"  Aceleração em g's:       {a_max / 1000 / 9.81:.2f} g")

# =============================================================================
# TESTE 5: JERK DA HASTE
# =============================================================================

print("\n" + "-" * 70)
print("TESTE 5: JERK DA HASTE")
print("-" * 70)

j = cin.jerk(theta_rad, OMEGA_TESTE, alpha=0, r=R_MM, L=L_MM, beta=0)

j_max = np.max(np.abs(j))
idx_j_max = np.argmax(np.abs(j))
j_max_val = j[idx_j_max]

print(f"\n✓ Cálculo concluído: {len(j)} pontos")
print(f"\n📊 Resultados:")
print(f"  Jerk máximo (|j|):   {j_max:.2f} mm/s³")
print(f"    em θ = {theta_deg[idx_j_max]:.0f}° (j = {j_max_val:.2f} mm/s³)")
print(f"  Jerk em m/s³:        {j_max / 1000:.2f} m/s³")

# =============================================================================
# TESTE 6: VELOCIDADE ANGULAR POR CULTURA
# =============================================================================

print("\n" + "-" * 70)
print("TESTE 6: VELOCIDADE ANGULAR POR CULTURA")
print("-" * 70)

try:
    culturas_yaml = config_loader.carregar_culturas()
    
    print(f"\n✓ Culturas carregadas: {len(culturas_yaml)}")
    print(f"\n📊 Velocidades angulares:")
    
    omegas_culturas = {}
    for nome, dados in culturas_yaml.items():
        vt_max = dados['planting_speed_kmh']['max']
        dens = dados['plant_density_per_hectare']
        germ = dados['germination_rate']
        
        N = cin.numero_sementes_por_metro(
            dens['min'], dens['max'],
            germ['min'], germ['max']
        )
        
        omega = cin.velocidade_angular(vt_max, N)
        omega_rpm = cin.omega_rpm(omega)
        
        omegas_culturas[nome] = omega
        
        print(f"  {nome.capitalize():12s} - {omega:7.2f} rad/s ({omega_rpm:5.0f} RPM) @ {vt_max:.1f} km/h")
    
    omega_max_cultura = max(omegas_culturas.items(), key=lambda x: x[1])
    omega_min_cultura = min(omegas_culturas.items(), key=lambda x: x[1])
    
    print(f"\n  Maior ω: {omega_max_cultura[0].capitalize()} ({omega_max_cultura[1]:.2f} rad/s)")
    print(f"  Menor ω: {omega_min_cultura[0].capitalize()} ({omega_min_cultura[1]:.2f} rad/s)")
    
except Exception as e:
    print(f"\n❌ Erro ao carregar culturas: {e}")

# =============================================================================
# TESTE 7: GERAÇÃO DE GRÁFICOS
# =============================================================================

print("\n" + "-" * 70)
print("TESTE 7: GERAÇÃO DE GRÁFICOS")
print("-" * 70)

gerar_graficos = input("\nGerar gráficos de teste? (s/n): ").strip().lower()

if gerar_graficos == 's':
    output_dir = 'output/images/tests'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n🎨 Gerando gráficos em {output_dir}...")
    
    # Preparar dados de múltiplas culturas para comparação
    velocidades_dict = {}
    aceleracoes_dict = {}
    jerks_dict = {}
    
    culturas_plot = ['soja', 'milho', 'sorgo']
    for cultura in culturas_plot:
        if cultura in omegas_culturas:
            omega_cult = omegas_culturas[cultura]
            velocidades_dict[cultura] = cin.velocidade(theta_rad, omega_cult, R_MM, L_MM)
            aceleracoes_dict[cultura] = cin.aceleracao(theta_rad, omega_cult, R_MM, L_MM, 0)
            jerks_dict[cultura] = cin.jerk(theta_rad, omega_cult, 0, R_MM, L_MM, 0)
    
    # Plotar cinemática completa
    plot_cinematica.plotar_cinematica_completa(
        theta_deg, y_solo,
        velocidades_dict, aceleracoes_dict, jerks_dict,
        theta_solo,
        output_dir=output_dir,
        mostrar=False,
        salvar=True
    )
    
    print(f"✅ Gráficos salvos em {output_dir}/")

# =============================================================================
# RESUMO FINAL
# =============================================================================

print("\n" + "=" * 70)
print("RESUMO DO TESTE DE CINEMÁTICA")
print("=" * 70)

print(f"\n✅ Testes concluídos com sucesso!")
print(f"\n📊 Resumo dos resultados:")
print(f"  • Curso total:              {y_max - y_min:.2f} mm")
print(f"  • Profundidade máxima:      {abs(y_min):.2f} mm")
print(f"  • Tempo no solo:            {theta_solo['subida'] - theta_solo['descida']:.2f}°")
print(f"  • Velocidade máxima:        {v_max:.2f} mm/s")
print(f"  • Aceleração máxima:        {a_max / 1000:.2f} m/s² ({a_max / 1000 / 9.81:.2f} g)")
print(f"  • Jerk máximo:              {j_max / 1000:.2f} m/s³")

print("\n" + "=" * 70)
print("Teste finalizado!")
print("=" * 70)
