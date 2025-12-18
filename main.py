"""
DOSADOR DE SEMENTES - Sistema Principal
========================================

Interface de linha de comando para análise cinemática, cálculo de torque
e visualização de dados de plantio.

Autor: José Gabriel
Projeto: TCC - Dosador de Sementes
"""

import os
import numpy as np

# Importações dos módulos do projeto
from core import cinematica as cin
from core import forcas_torque as ft
from core import espacamento as esp
from data import ibge_loader
from visualization import (
    plot_cinematica, plot_torque, plot_espacamento, plot_ibge
)
from utils import config_loader


# ========================================================================
# CONSTANTES GLOBAIS (Configuração padrão)
# ========================================================================

# Geometria do mecanismo (mm)
R_MM = 84.01
L_MM = 210.0
H_MM = 347.46
ALTURA_CENTRO_MM = 591.47

# Massas e gravidade
M_HASTE_KG = 1.16094
M_BIELA_KG = 0.75022
G_MS2 = 9.81

# Condições cinemáticas
ALPHA_DEFAULT = 0.0
BETA_DEFAULT = 0.0

# Diretório de saída
OUTPUT_DIR = "output/images"


# ========================================================================
# MENU PRINCIPAL
# ========================================================================

def exibir_menu():
    """Exibe o menu principal do sistema."""
    print("\n" + "=" * 60)
    print(" Semeadura por Puncionamento - Sistema de Análise")
    print("=" * 60)
    print("\n📊 ANÁLISES DISPONÍVEIS:")
    print("\n  1. Análise Cinemática Completa")
    print("  2. Análise de Torque e Forças")
    print("  3. Distribuição de Sementes (Espaçamento)")
    print("  4. Dados IBGE - Área Plantada")
    print("\n⚙️  CONFIGURAÇÕES:")
    print("\n  5. Configurar Parâmetros do Mecanismo")
    print("  6. Adicionar Nova Cultura")
    print("  7. Sobre / Créditos")
    print("\n  0. Sair")
    print("\n" + "=" * 60)


def menu_cinematica():
    """Menu de análise cinemática."""
    print("\n" + "-" * 60)
    print("ANÁLISE CINEMÁTICA")
    print("-" * 60)

    # Carregar culturas
    try:
        culturas_yaml = config_loader.carregar_culturas()
        culturas_disponiveis = list(culturas_yaml.keys())

        print("\nCulturas disponíveis:")
        for i, cult in enumerate(culturas_disponiveis, 1):
            print(f"  {i}. {cult.capitalize()}")

        print(f"\n  {len(culturas_disponiveis) + 1}. Todas as culturas")

        escolha = input("\nEscolha uma cultura (número ou 0 para voltar): ").strip()

        if escolha == '0':
            return

        if escolha == str(len(culturas_disponiveis) + 1):
            culturas_selecionadas = culturas_disponiveis
        else:
            idx = int(escolha) - 1
            if 0 <= idx < len(culturas_disponiveis):
                culturas_selecionadas = [culturas_disponiveis[idx]]
            else:
                print("❌ Opção inválida!")
                return

        # Executar análise
        print("\n🔄 Processando análise cinemática...")
        executar_analise_cinematica(culturas_selecionadas, culturas_yaml)

    except Exception as e:
        print(f"❌ Erro: {e}")


def menu_torque():
    """Menu de análise de torque."""
    print("\n" + "-" * 60)
    print("ANÁLISE DE TORQUE E FORÇAS")
    print("-" * 60)

    try:
        # Configuração da força do solo
        print("\nConfiguração da Força Vertical do Solo (F_VS):")
        print("  1. Sem força do solo (F_VS = 0)")
        print("  2. Força constante")
        print("  3. Força variável (modelo completo - recomendado)")

        opcao_fvs = input("\nEscolha uma opção: ").strip()

        if opcao_fvs == '1':
            F_VS_config = {'tipo': 'zero'}
        elif opcao_fvs == '2':
            valor = float(input("Valor de F_VS constante (N): "))
            F_VS_config = {'tipo': 'constante', 'valor': valor}
        elif opcao_fvs == '3':
            F_VS_config = {'tipo': 'variavel'}
        else:
            print("❌ Opção inválida!")
            return

        # Velocidade angular
        print("\n" + "-" * 60)
        print("VELOCIDADE ANGULAR")
        print("-" * 60)
        print("\n  1. Velocidade de teste (recomendado)")
        print("  2. Usar velocidade angular por cultura")
        print("  3. Inserir velocidade angular manualmente")

        opcao_omega = input("\nEscolha uma opção: ").strip()

        if opcao_omega == '1':
            # Usar velocidade de teste padrão (igual ao teste_torque.py)
            omega = 20.0
            omega_rpm = cin.omega_rpm(omega)
            #print(f"\n✓ Usando velocidade de teste: {omega:.2f} rad/s ({omega_rpm:.0f} RPM)")

        elif opcao_omega == '2':
            # Carregar culturas e mostrar velocidades
            culturas_yaml = config_loader.carregar_culturas()

            print("\n📊 Velocidades angulares por cultura:")
            print("-" * 60)

            omegas_culturas = {}
            for nome, dados in culturas_yaml.items():
                vt_max = dados['planting_speed_kmh']['max']
                dens = dados['plant_density_per_hectare']
                germ = dados['germination_rate']

                N = cin.sementes_por_metro(dens['min'], dens['max'], germ['min'], germ['max'])
                omega = cin.velocidade_angular(vt_max, N)
                omega_rpm = cin.omega_rpm(omega)

                omegas_culturas[nome] = omega
                print(f"  {nome.capitalize():12s} - {omega:.2f} rad/s ({omega_rpm:.0f} RPM) @ {vt_max:.1f} km/h")

            print("\n" + "-" * 60)
            print("Escolha uma cultura:")
            culturas_lista = list(omegas_culturas.keys())
            for i, cult in enumerate(culturas_lista, 1):
                print(f"  {i}. {cult.capitalize()}")

            print(f"  {len(culturas_lista) + 1}. Usar a maior velocidade angular")

            escolha = input("\nEscolha (número): ").strip()

            if escolha == str(len(culturas_lista) + 1):
                omega = max(omegas_culturas.values())
                cultura_max = max(omegas_culturas.items(), key=lambda x: x[1])[0]
                print(f"\n✓ Usando omega máximo: {omega:.2f} rad/s ({cultura_max.capitalize()})")
            else:
                idx = int(escolha) - 1
                if 0 <= idx < len(culturas_lista):
                    cultura_escolhida = culturas_lista[idx]
                    omega = omegas_culturas[cultura_escolhida]
                    print(f"\n✓ Usando omega de {cultura_escolhida.capitalize()}: {omega:.2f} rad/s")
                else:
                    print("❌ Opção inválida!")
                    return

        elif opcao_omega == '3':
            omega = float(input("\nVelocidade angular da manivela (rad/s): "))
        else:
            print("❌ Opção inválida!")
            return

        print("\n🔄 Processando análise de torque...")
        executar_analise_torque(omega, F_VS_config)

    except Exception as e:
        print(f"❌ Erro: {e}")


def menu_espacamento():
    """Menu de distribuição de sementes."""
    print("\n" + "-" * 60)
    print("DISTRIBUIÇÃO DE SEMENTES")
    print("-" * 60)

    try:
        culturas_yaml = config_loader.carregar_culturas()

        # Preparar dados para cálculo
        culturas_dict = {}
        for nome, dados in culturas_yaml.items():
            dens = dados['plant_density_per_hectare']
            germ = dados['germination_rate']
            culturas_dict[nome] = {
                'dens_min': dens['min'],
                'dens_max': dens['max'],
                'germ_min': germ['min'],
                'germ_max': germ['max']
            }

        distancia = float(input("\nDistância a analisar (metros) [padrão: 3.0]: ") or "3.0")

        print("\n🔄 Calculando distribuição de sementes...")
        espacamentos = esp.calcular_espacamento_culturas(culturas_dict, distancia)

        # Exibir resultados
        print("\n📊 RESULTADOS:")
        for cultura, dados in espacamentos.items():
            print(f"\n{cultura.upper()}:")
            print(f"  Sementes/metro: {dados['sementes_por_metro']:.2f}")
            print(f"  Total em {distancia}m: {dados['sementes_total']}")
            print(f"  Espaçamento: {dados['espacamento_cm']:.2f} cm")

        # Gerar gráfico
        salvar = input("\nSalvar gráfico? (s/n): ").strip().lower() == 's'
        mostrar = input("Exibir gráfico? (s/n): ").strip().lower() == 's'

        plot_espacamento.plotar_distribuicao_sementes(
            espacamentos, distancia, OUTPUT_DIR, mostrar, salvar
        )

    except Exception as e:
        print(f"❌ Erro: {e}")


def menu_ibge():
    """Menu de dados do IBGE."""
    print("\n" + "-" * 60)
    print("DADOS IBGE - ÁREA PLANTADA")
    print("-" * 60)
    print("\n  1. Gráfico de área por cultura (Brasil)")
    print("  2. Ranking de estados por cultura")
    print("  3. Mapa coroplético por cultura")
    print("  4. Mapa total (todas as culturas)")
    print("  0. Voltar")

    opcao = input("\nEscolha uma opção: ").strip()

    try:
        if opcao == '1':
            t1, _ = ibge_loader.carregar_dados_ibge()
            mostrar = input("Exibir gráfico? (s/n): ").strip().lower() == 's'
            plot_ibge.plotar_area_culturas(t1, OUTPUT_DIR, mostrar, True)

        elif opcao == '2':
            cultura = input("Nome da cultura (ex: Soja): ").strip()
            n = int(input("Número de estados no ranking [10]: ") or "10")
            top = ibge_loader.obter_top_estados(cultura, n)
            mostrar = input("Exibir gráfico? (s/n): ").strip().lower() == 's'
            plot_ibge.plotar_ranking_estados(top, cultura, OUTPUT_DIR, mostrar, True)

        elif opcao == '3':
            _, t2 = ibge_loader.carregar_dados_ibge()
            cultura = input("Nome da cultura (ex: Soja): ").strip()
            mostrar = input("Exibir gráfico? (s/n): ").strip().lower() == 's'
            plot_ibge.plotar_mapa_cultura(t2, cultura, output_dir=OUTPUT_DIR,
                                         mostrar=mostrar, salvar=True)

        elif opcao == '4':
            _, t2 = ibge_loader.carregar_dados_ibge()
            mostrar = input("Exibir gráfico? (s/n): ").strip().lower() == 's'
            plot_ibge.plotar_mapa_total(t2, output_dir=OUTPUT_DIR,
                                       mostrar=mostrar, salvar=True)

    except Exception as e:
        print(f"❌ Erro: {e}")


# ========================================================================
# EXECUTORES DE ANÁLISE
# ========================================================================

def executar_analise_cinematica(culturas, culturas_yaml):
    """Executa análise cinemática completa."""

    # Malha de ângulos
    theta_deg = np.arange(0.0, 361.0, 1.0)
    theta_rad = np.deg2rad(theta_deg)

    # Encontrar ângulos de contato com solo
    theta_solo = cin.encontrar_theta_solo(R_MM, L_MM, H_MM, ALTURA_CENTRO_MM)

    print(f"\n✓ Ângulo de descida: {theta_solo['descida']:.2f}°")
    print(f"✓ Ângulo de subida: {theta_solo['subida']:.2f}°")

    # Calcular posição (independe da cultura)
    y_solo = cin.y_solo_mm(theta_rad, R_MM, L_MM, H_MM, ALTURA_CENTRO_MM)

    # Calcular para cada cultura
    velocidades_dict = {}
    aceleracoes_dict = {}
    jerks_dict = {}

    for cultura in culturas:
        dados = culturas_yaml[cultura]
        vt_max = dados['planting_speed_kmh']['max']

        dens = dados['plant_density_per_hectare']
        germ = dados['germination_rate']

        N = cin.sementes_por_metro(dens['min'], dens['max'], germ['min'], germ['max'])
        omega = cin.velocidade_angular(vt_max, N)
        omega_rpm_val = cin.omega_rpm(omega)

        print(f"\n{cultura.upper()}:")
        print(f"  Velocidade: {vt_max:.1f} km/h")
        print(f"  Omega: {omega:.2f} rad/s ({omega_rpm_val:.0f} RPM)")

        v = cin.velocidade(theta_rad, omega, R_MM, L_MM)
        a = cin.aceleracao(theta_rad, omega, R_MM, L_MM, ALPHA_DEFAULT)
        j = cin.jerk(theta_rad, omega, ALPHA_DEFAULT, R_MM, L_MM, BETA_DEFAULT)

        velocidades_dict[cultura] = {'velocidade': v, 'omega_rpm': omega_rpm_val}
        aceleracoes_dict[cultura] = {'aceleracao': a, 'omega_rpm': omega_rpm_val}
        jerks_dict[cultura] = {'jerk': j, 'omega_rpm': omega_rpm_val}

    # Gerar gráficos
    salvar = input("\nSalvar gráficos? (s/n): ").strip().lower() == 's'
    mostrar = input("Exibir gráficos? (s/n): ").strip().lower() == 's'

    plot_cinematica.plotar_posicao(theta_deg, y_solo, theta_solo, OUTPUT_DIR, mostrar, salvar)
    plot_cinematica.plotar_velocidade(theta_deg, velocidades_dict, theta_solo, OUTPUT_DIR, mostrar, salvar)
    plot_cinematica.plotar_aceleracao(theta_deg, aceleracoes_dict, theta_solo, OUTPUT_DIR, mostrar, salvar)
    plot_cinematica.plotar_jerk(theta_deg, jerks_dict, theta_solo, OUTPUT_DIR, mostrar, salvar)

    if len(culturas) > 1:
        plot_cinematica.plotar_cinematica_completa(
            theta_deg, y_solo, velocidades_dict, aceleracoes_dict, jerks_dict,
            theta_solo, OUTPUT_DIR, mostrar, salvar
        )

    print("\n✅ Análise cinemática concluída!")


def executar_analise_torque(omega, F_VS_config):
    """Executa análise de torque e forças."""

    # Converter geometria para metros
    r_m = R_MM / 1000.0
    L_m = L_MM / 1000.0
    h_m = H_MM / 1000.0

    # Pesos
    P_haste = M_HASTE_KG * G_MS2
    P_biela = M_BIELA_KG * G_MS2

    # Malha de ângulos
    theta_deg = np.linspace(0.0, 360.0, 361)
    theta_rad = np.deg2rad(theta_deg)

    # Construir F_VS
    theta_range = None
    theta_pico = None
    F_max_info = None

    if F_VS_config['tipo'] == 'zero':
        F_VS = np.zeros_like(theta_deg)
    elif F_VS_config['tipo'] == 'constante':
        F_VS = np.full_like(theta_deg, F_VS_config['valor'])
    else:  # variável (modelo completo)
        F_VS, F_max_const, theta_pico, info = ft.construir_F_VS_variavel(
            theta_deg, R_MM, L_MM, H_MM, ALTURA_CENTRO_MM
        )
        theta_range = (info['theta_inicio'], info['theta_fim'])
        F_max_info = F_max_const

        print(f"\n📐 Parâmetros do modelo F_VS:")
        print(f"  θ início: {info['theta_inicio']:.2f}°")
        print(f"  θ pico: {info['theta_pico']:.2f}°")
        print(f"  θ fim: {info['theta_fim']:.2f}°")
        print(f"  F_VS máximo: {info['F_max']:.2f} N")
        print(f"  Profundidade alvo: {info['y_alvo_mm']:.2f} mm")

    # Calcular forças
    F_B, F_M = ft.forcas_FB_FM(theta_rad, r_m, L_m, h_m,
                                M_HASTE_KG, M_BIELA_KG,
                                P_haste, P_biela, F_VS, omega)

    # Calcular torque
    tau = ft.torque(theta_rad, r_m, L_m, h_m,
                    M_HASTE_KG, M_BIELA_KG,
                    P_haste, P_biela, F_VS, omega)

    # Estatísticas
    tau_max_abs = np.max(np.abs(tau))
    idx_max = np.argmax(np.abs(tau))
    tau_max = tau[idx_max]
    theta_max = theta_deg[idx_max]

    FB_max_abs = np.max(np.abs(F_B))
    idx_FB = np.argmax(np.abs(F_B))
    theta_FB = theta_deg[idx_FB]

    FM_max_abs = np.max(np.abs(F_M))
    idx_FM = np.argmax(np.abs(F_M))
    theta_FM = theta_deg[idx_FM]

    print(f"\n📊 RESULTADOS:")
    print(f"  Torque máximo (|τ|): {tau_max_abs:.4f} N·m")
    print(f"    em θ = {theta_max:.2f}° (τ = {tau_max:.4f} N·m)")
    print(f"\n  F_B máximo: {FB_max_abs:.2f} N em θ = {theta_FB:.2f}°")
    print(f"  F_M máximo: {FM_max_abs:.2f} N em θ = {theta_FM:.2f}°")

    # Gerar gráficos
    salvar = input("\nSalvar gráficos? (s/n): ").strip().lower() == 's'
    mostrar = input("Exibir gráficos? (s/n): ").strip().lower() == 's'

    # Preparar informações para o plot
    if F_VS_config['tipo'] == 'variavel':
        plot_info = {
            'theta_range': theta_range,
            'theta_pico': theta_pico,
            'F_max': F_max_info
        }
    else:
        plot_info = None

    plot_torque.plotar_torque(theta_deg, tau, theta_range, F_max_info, OUTPUT_DIR, mostrar, salvar)
    plot_torque.plotar_forcas(theta_deg, F_B, F_M, theta_range, OUTPUT_DIR, mostrar, salvar)

    print("\n✅ Análise de torque concluída!")


def caixa_texto(linhas, padding=2):
    # largura interna baseada na maior linha
    largura = max(len(s) for s in linhas) + padding * 2

    print()
    print("╔" + "═" * largura + "╗")
    for s in linhas:
        print("║" + s.center(largura) + "║")
    print("╚" + "═" * largura + "╝")


def menu_configurar_parametros():
    """Menu para configurar parâmetros do mecanismo."""
    print("\n" + "=" * 60)
    print("CONFIGURAÇÃO DE PARÂMETROS DO MECANISMO")
    print("=" * 60)

    global R_MM, L_MM, H_MM, ALTURA_CENTRO_MM, M_HASTE_KG, M_BIELA_KG

    try:
        print("\n📐 PARÂMETROS ATUAIS:")
        print(f"\n  GEOMETRIA:")
        print(f"    r (raio da manivela):      {R_MM:.2f} mm")
        print(f"    L (comprimento da biela):  {L_MM:.2f} mm")
        print(f"    h (altura da haste):       {H_MM:.2f} mm")
        print(f"    Altura do centro:          {ALTURA_CENTRO_MM:.2f} mm")
        print(f"\n  MASSAS:")
        print(f"    m_haste:                   {M_HASTE_KG:.5f} kg")
        print(f"    m_biela:                   {M_BIELA_KG:.5f} kg")

        print("\n" + "-" * 60)
        print("O que deseja configurar?")
        print("  1. Parâmetros geométricos (r, L, h, altura_centro)")
        print("  2. Massas (m_haste, m_biela)")
        print("  3. Todos os parâmetros")
        print("  0. Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == '0':
            return
        elif opcao in ['1', '3']:
            print("\n" + "-" * 60)
            print("PARÂMETROS GEOMÉTRICOS")
            print("-" * 60)

            resposta = input(f"\nRaio da manivela r (mm) [{R_MM:.2f}]: ").strip()
            if resposta:
                R_MM = float(resposta)

            resposta = input(f"Comprimento da biela L (mm) [{L_MM:.2f}]: ").strip()
            if resposta:
                L_MM = float(resposta)

            resposta = input(f"Altura da haste h (mm) [{H_MM:.2f}]: ").strip()
            if resposta:
                H_MM = float(resposta)

            resposta = input(f"Altura do centro (mm) [{ALTURA_CENTRO_MM:.2f}]: ").strip()
            if resposta:
                ALTURA_CENTRO_MM = float(resposta)

            print("\n✓ Parâmetros geométricos atualizados!")

        if opcao in ['2', '3']:
            print("\n" + "-" * 60)
            print("MASSAS")
            print("-" * 60)

            resposta = input(f"\nMassa da haste m_haste (kg) [{M_HASTE_KG:.5f}]: ").strip()
            if resposta:
                M_HASTE_KG = float(resposta)

            resposta = input(f"Massa da biela m_biela (kg) [{M_BIELA_KG:.5f}]: ").strip()
            if resposta:
                M_BIELA_KG = float(resposta)

            print("\n✓ Massas atualizadas!")

        print("\n" + "=" * 60)
        print("✅ Configuração concluída!")
        print("=" * 60)
        print("\n📋 NOVOS PARÂMETROS:")
        print(f"  r = {R_MM:.2f} mm")
        print(f"  L = {L_MM:.2f} mm")
        print(f"  h = {H_MM:.2f} mm")
        print(f"  altura_centro = {ALTURA_CENTRO_MM:.2f} mm")
        print(f"  m_haste = {M_HASTE_KG:.5f} kg")
        print(f"  m_biela = {M_BIELA_KG:.5f} kg")

        input("\nPressione ENTER para continuar...")

    except ValueError:
        print("\n❌ Erro: valor inválido! Use números.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")


def menu_adicionar_cultura():
    """Menu para adicionar uma nova cultura."""
    print("\n" + "=" * 60)
    print("ADICIONAR NOVA CULTURA")
    print("=" * 60)

    try:
        print("\n📝 INFORMAÇÕES NECESSÁRIAS:")
        print("\n  Para adicionar uma nova cultura, você precisará fornecer:")
        print("\n  1️⃣  Nome da cultura (ex: trigo, aveia, etc.)")
        print("  2️⃣  Espaçamento entre linhas em metros")
        print("       • Pode ter múltiplas opções (ex: 0.45, 0.50)")
        print("\n  3️⃣  Densidade de plantio (plantas/hectare)")
        print("       • Valor mínimo")
        print("       • Valor máximo")
        print("       • Passo (incremento)")
        print("\n  4️⃣  Velocidade de plantio (km/h)")
        print("       • Valor mínimo")
        print("       • Valor máximo")
        print("       • Passo (incremento)")
        print("\n  5️⃣  Taxa de germinação (%)")
        print("       • Valor mínimo (0.0 a 1.0 ou 0 a 100)")
        print("       • Valor máximo (0.0 a 1.0 ou 0 a 100)")
        print("       • Passo (incremento)")

        print("\n" + "-" * 60)
        continuar = input("\nDeseja adicionar uma nova cultura? (s/n): ").strip().lower()

        if continuar != 's':
            return

        # Nome da cultura
        nome = input("\n📌 Nome da cultura: ").strip().lower()
        if not nome:
            print("❌ Nome inválido!")
            return

        # Espaçamento entre linhas
        print(f"\n📏 Espaçamento entre linhas (metros):")
        espacamentos_str = input("   Digite um ou mais valores separados por vírgula (ex: 0.45, 0.50): ").strip()
        espacamentos = [float(x.strip()) for x in espacamentos_str.split(',')]

        # Densidade de plantio
        print(f"\n🌱 Densidade de plantio (plantas/hectare):")
        dens_min = float(input("   Valor mínimo: ").strip())
        dens_max = float(input("   Valor máximo: ").strip())
        dens_step = float(input("   Passo: ").strip())

        # Velocidade de plantio
        print(f"\n🚜 Velocidade de plantio (km/h):")
        vel_min = float(input("   Valor mínimo: ").strip())
        vel_max = float(input("   Valor máximo: ").strip())
        vel_step = float(input("   Passo: ").strip())

        # Taxa de germinação
        print(f"\n🌾 Taxa de germinação:")
        germ_min = float(input("   Valor mínimo (0-1 ou 0-100): ").strip())
        germ_max = float(input("   Valor máximo (0-1 ou 0-100): ").strip())
        germ_step = float(input("   Passo: ").strip())

        # Converter se for percentual
        if germ_min > 1:
            germ_min /= 100.0
        if germ_max > 1:
            germ_max /= 100.0
        if germ_step > 0.1:
            germ_step /= 100.0

        # Criar estrutura YAML
        print("\n" + "=" * 60)
        print("📋 DADOS DA NOVA CULTURA:")
        print("=" * 60)
        print(f"\n  - name: \"{nome}\"")
        print(f"    row_spacing_m:")
        print(f"      options: {espacamentos}")
        print(f"    plant_density_per_hectare: {{ min: {int(dens_min)}, max: {int(dens_max)}, step: {int(dens_step)} }}")
        print(f"    planting_speed_kmh:        {{ min: {vel_min:.1f}, max: {vel_max:.1f}, step: {vel_step:.1f} }}")
        print(f"    germination_rate:          {{ min: {germ_min:.2f}, max: {germ_max:.2f}, step: {germ_step:.2f} }}")

        print("\n" + "-" * 60)
        print("⚠️  ATENÇÃO:")
        print("   Para adicionar esta cultura ao sistema, copie o texto acima")
        print("   e adicione manualmente ao arquivo:")
        print(f"   {os.path.abspath('config/culturas.yaml')}")
        print("\n   Cole no final da lista 'crops', mantendo a indentação.")
        print("-" * 60)

        input("\nPressione ENTER para continuar...")

    except ValueError:
        print("\n❌ Erro: valor inválido! Use números.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")


def exibir_banner():
    caixa_texto([
        "Semeadura por Puncionamento - Sistema de Análise",
        "UFSC - José Gabriel Furlan • Prof. Sergio Idehara",
    ])

def exibir_creditos():
    caixa_texto([
        "SOBRE / CRÉDITOS",
        "Autor: José Gabriel Furlan De Barros",
        "Orientação: Prof. Sergio Junichi Idehara",
        "Projeto: TCC - Projeto de um sistema de semeadura por puncionamento",
        "Universidade Federal de Santa Catarina (UFSC)",
        "Versão: 0.1.0",
    ])
    input("\nPressione ENTER para voltar...")


# ========================================================================
# MAIN
# ========================================================================

def main():
    """Função principal do sistema."""

    exibir_banner()

    while True:
        try:
            exibir_menu()
            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == '0':
                print("\n👋 Encerrando sistema. Até logo!")
                break
            elif opcao == '1':
                menu_cinematica()
            elif opcao == '2':
                menu_torque()
            elif opcao == '3':
                menu_espacamento()
            elif opcao == '4':
                menu_ibge()
            elif opcao == '5':
                menu_configurar_parametros()
            elif opcao == '6':
                menu_adicionar_cultura()
            elif opcao == '7':
                exibir_creditos()
            else:
                print("\n❌ Opção inválida! Tente novamente.")

        except KeyboardInterrupt:
            print("\n\n👋 Encerrando sistema. Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            print("Tente novamente ou escolha outra opção.")


if __name__ == "__main__":
    main()
