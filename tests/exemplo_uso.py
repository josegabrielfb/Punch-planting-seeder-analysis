"""
Exemplos de Uso do Sistema de Análise de Dosador de Sementes
==============================================================

Este arquivo demonstra como usar todas as funcionalidades do sistema:

1. Análise Cinemática
2. Análise de Torque e Forças
3. Distribuição de Sementes
4. Dados IBGE
5. Carregamento de Configurações

Cada exemplo é independente e pode ser executado separadamente.

Autor: José Gabriel Furlan De Barros
Projeto: TCC - Sistema de Semeadura por Puncionamento
UFSC - 2025
"""

import numpy as np
import sys
import os

# Adicionar o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import cinematica as cin
from core import forcas_torque as ft
from core import espacamento as esp
from visualization import plot_cinematica, plot_torque, plot_espacamento, plot_ibge
from data import ibge_loader
from utils import config_loader

# =============================================================================
# CONFIGURAÇÃO GLOBAL
# =============================================================================

OUTPUT_DIR = 'output/images/exemplos'
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print(" " * 20 + "EXEMPLOS DE USO DO SISTEMA")
print(" " * 15 + "Dosador de Sementes - UFSC 2025")
print("=" * 80)

# =============================================================================
# EXEMPLO 1: ANÁLISE CINEMÁTICA BÁSICA
# =============================================================================

def exemplo_cinematica_basica():
    """
    Demonstra o cálculo básico de cinemática:
    - Posição, velocidade, aceleração e jerk
    - Ângulos de contato com o solo
    """
    print("\n" + "=" * 80)
    print("EXEMPLO 1: ANÁLISE CINEMÁTICA BÁSICA")
    print("=" * 80)
    
    # Parâmetros geométricos (mm)
    r, L, h = 84.01, 210.0, 347.46
    altura_centro = 591.47
    
    # Velocidade angular (rad/s)
    omega = 20.0
    
    # Vetor de ângulos
    theta_deg = np.arange(0, 361)
    theta_rad = np.deg2rad(theta_deg)
    
    print(f"\n📐 Parâmetros: r={r} mm, L={L} mm, h={h} mm")
    print(f"⚙️  Velocidade: ω={omega} rad/s ({cin.omega_rpm(omega):.0f} RPM)")
    
    # Calcular cinemática
    y_solo = cin.y_solo_mm(theta_rad, r, L, h, altura_centro)
    v = cin.velocidade(theta_rad, omega, r, L)
    a = cin.aceleracao(theta_rad, omega, r, L, alpha=0)
    j = cin.jerk(theta_rad, omega, 0, r, L, 0)
    
    # Encontrar ângulos de solo
    theta_solo = cin.encontrar_theta_solo(r, L, h, altura_centro)
    
    # Exibir resultados
    print(f"\n📊 Resultados:")
    print(f"  Profundidade máxima:  {np.min(y_solo):.2f} mm")
    print(f"  Velocidade máxima:    {np.max(np.abs(v)):.2f} mm/s")
    print(f"  Aceleração máxima:    {np.max(np.abs(a))/1000:.2f} m/s²")
    print(f"  θ descida:            {theta_solo['descida']:.2f}°")
    print(f"  θ subida:             {theta_solo['subida']:.2f}°")
    
    return theta_deg, y_solo, v, a, j, theta_solo


# =============================================================================
# EXEMPLO 2: COMPARAÇÃO ENTRE CULTURAS
# =============================================================================

def exemplo_comparacao_culturas():
    """
    Demonstra como comparar a cinemática de diferentes culturas
    com suas respectivas velocidades angulares.
    """
    print("\n" + "=" * 80)
    print("EXEMPLO 2: COMPARAÇÃO ENTRE CULTURAS")
    print("=" * 80)
    
    # Carregar culturas
    culturas_yaml = config_loader.carregar_culturas()
    
    # Parâmetros geométricos
    r, L, h = 84.01, 210.0, 347.46
    theta_deg = np.arange(0, 361)
    theta_rad = np.deg2rad(theta_deg)
    
    # Calcular velocidades para cada cultura
    print(f"\n📊 Velocidades angulares por cultura:")
    
    velocidades_dict = {}
    for nome, dados in list(culturas_yaml.items())[:3]:  # Primeiras 3 culturas
        vt_max = dados['planting_speed_kmh']['max']
        dens = dados['plant_density_per_hectare']
        germ = dados['germination_rate']
        
        N = cin.numero_sementes_por_metro(
            dens['min'], dens['max'],
            germ['min'], germ['max']
        )
        
        omega = cin.velocidade_angular(vt_max, N)
        velocidades_dict[nome] = cin.velocidade(theta_rad, omega, r, L)
        
        print(f"  {nome.capitalize():12s} - ω = {omega:.2f} rad/s")
    
    return velocidades_dict


# =============================================================================
# EXEMPLO 3: CÁLCULO DE TORQUE COM F_VS VARIÁVEL
# =============================================================================

def exemplo_torque_fvs_variavel():
    """
    Demonstra o cálculo completo de torque usando o modelo
    F_VS variável (mais realista).
    """
    print("\n" + "=" * 80)
    print("EXEMPLO 3: TORQUE COM F_VS VARIÁVEL")
    print("=" * 80)
    
    # Parâmetros
    R_MM, L_MM, H_MM = 84.01, 210.0, 347.46
    ALTURA_CENTRO_MM = 591.47
    m_haste, m_biela = 1.16094, 0.75022
    omega = 20.0
    
    theta_deg = np.linspace(0, 360, 361)
    theta_rad = np.deg2rad(theta_deg)
    
    # Construir F_VS variável
    print("\n🔧 Construindo modelo F_VS variável...")
    F_VS, F_max, theta_pico, info = ft.construir_F_VS_variavel(
        theta_deg, R_MM, L_MM, H_MM, ALTURA_CENTRO_MM
    )
    
    print(f"  ✓ θ início: {info['theta_inicio']:.2f}°")
    print(f"  ✓ θ pico:   {info['theta_pico']:.2f}°")
    print(f"  ✓ F_max:    {info['F_max']:.2f} N")
    
    # Calcular torque
    r_m = R_MM / 1000
    L_m = L_MM / 1000
    h_m = H_MM / 1000
    P_haste = m_haste * 9.81
    P_biela = m_biela * 9.81
    
    tau = ft.torque(theta_rad, r_m, L_m, h_m,
                    m_haste, m_biela, P_haste, P_biela,
                    F_VS, omega)
    
    print(f"\n📊 Torque máximo: {np.max(np.abs(tau)):.4f} N·m")
    
    return theta_deg, tau, F_VS, info


# =============================================================================
# EXEMPLO 4: DISTRIBUIÇÃO DE SEMENTES
# =============================================================================

def exemplo_distribuicao_sementes():
    """
    Demonstra como calcular a distribuição de sementes
    para diferentes culturas.
    """
    print("\n" + "=" * 80)
    print("EXEMPLO 4: DISTRIBUIÇÃO DE SEMENTES")
    print("=" * 80)
    
    # Carregar culturas
    culturas_yaml = config_loader.carregar_culturas()
    
    # Preparar dados
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
    
    # Calcular espaçamento para 3 metros
    distancia = 3.0
    resultados = esp.calcular_espacamento_culturas(culturas_dict, distancia)
    
    print(f"\n📊 Espaçamento para {distancia} metros:")
    for cultura, res in list(resultados.items())[:4]:
        print(f"\n  {cultura.upper()}:")
        print(f"    Sementes/metro: {res['sementes_por_metro']:.2f}")
        print(f"    Espaçamento:    {res['espacamento_cm']:.2f} cm")
        print(f"    Total:          {res['total_sementes']:.0f} sementes")
    
    return resultados


# =============================================================================
# EXEMPLO 5: CARREGAMENTO DE CONFIGURAÇÕES
# =============================================================================

def exemplo_configuracoes():
    """
    Demonstra como carregar e usar as configurações do sistema.
    """
    print("\n" + "=" * 80)
    print("EXEMPLO 5: CARREGAMENTO DE CONFIGURAÇÕES")
    print("=" * 80)
    
    # Carregar configurações do mecanismo
    config = config_loader.carregar_config()
    
    print(f"\n⚙️  Configurações do mecanismo:")
    print(f"  r = {config['mechanics']['crank_radius_mm']} mm")
    print(f"  L = {config['mechanics']['rod_length_mm']} mm")
    print(f"  h = {config['mechanics']['offset_h_mm']} mm")
    
    # Carregar culturas
    culturas = config_loader.carregar_culturas()
    print(f"\n🌾 Culturas disponíveis ({len(culturas)}):")
    for nome in culturas.keys():
        print(f"  • {nome.capitalize()}")
    
    # Extrair dados de uma cultura específica
    soja = config_loader.extrair_faixas_cultura('soja')
    print(f"\n📊 Dados da Soja:")
    print(f"  Densidade:   {soja['density_min']}-{soja['density_max']} pl/ha")
    print(f"  Velocidade:  {soja['speed_min']}-{soja['speed_max']} km/h")
    print(f"  Germinação:  {soja['germ_min']*100:.0f}-{soja['germ_max']*100:.0f}%")
    
    return config, culturas


# =============================================================================
# EXEMPLO 6: DADOS IBGE (OPCIONAL)
# =============================================================================

def exemplo_dados_ibge():
    """
    Demonstra como carregar e processar dados do IBGE.
    Requer arquivos de dados do IBGE na pasta data/.
    """
    print("\n" + "=" * 80)
    print("EXEMPLO 6: DADOS IBGE (OPCIONAL)")
    print("=" * 80)
    
    try:
        # Carregar dados
        dados = ibge_loader.carregar_dados_ibge()
        
        if dados:
            print(f"\n✓ Dados IBGE carregados com sucesso!")
            print(f"  Número de tabelas: {len(dados)}")
            
            # Processar síntese
            sintese = ibge_loader.processar_tabela_sintese(dados)
            if sintese is not None:
                print(f"\n📊 Culturas no dataset: {len(sintese)}")
                for cultura in list(sintese.columns)[:5]:
                    print(f"  • {cultura}")
        else:
            print(f"\n⚠️  Dados IBGE não disponíveis")
            print(f"   (Opcional - não afeta outros exemplos)")
            
    except Exception as e:
        print(f"\n⚠️  Erro ao carregar dados IBGE: {e}")
        print(f"   (Opcional - não afeta outros exemplos)")


# =============================================================================
# EXEMPLO 7: GERAÇÃO DE TODOS OS GRÁFICOS
# =============================================================================

def exemplo_gerar_graficos():
    """
    Demonstra como gerar todos os tipos de gráficos do sistema.
    """
    print("\n" + "=" * 80)
    print("EXEMPLO 7: GERAÇÃO DE GRÁFICOS")
    print("=" * 80)
    
    gerar = input("\nGerar todos os gráficos de exemplo? (s/n): ").strip().lower()
    
    if gerar != 's':
        print("  Pulando geração de gráficos...")
        return
    
    print(f"\n🎨 Gerando gráficos em {OUTPUT_DIR}...")
    
    # Preparar dados
    r, L, h = 84.01, 210.0, 347.46
    altura_centro = 591.47
    theta_deg = np.arange(0, 361)
    theta_rad = np.deg2rad(theta_deg)
    
    # Dados de cinemática
    y_solo = cin.y_solo_mm(theta_rad, r, L, h, altura_centro)
    theta_solo = cin.encontrar_theta_solo(r, L, h, altura_centro)
    
    # Gráfico de posição
    print("  • Gráfico de posição...")
    plot_cinematica.plotar_posicao(
        theta_deg, y_solo, theta_solo,
        OUTPUT_DIR, mostrar=False, salvar=True
    )
    
    print(f"\n✅ Gráficos salvos em {OUTPUT_DIR}/")


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """
    Executa todos os exemplos em sequência.
    """
    
    print("\nEste script demonstra todos os recursos do sistema.")
    print("Cada exemplo é independente e pode ser executado separadamente.\n")
    
    # Menu de opções
    print("=" * 80)
    print("ESCOLHA UM EXEMPLO:")
    print("=" * 80)
    print("\n  1. Análise Cinemática Básica")
    print("  2. Comparação entre Culturas")
    print("  3. Torque com F_VS Variável")
    print("  4. Distribuição de Sementes")
    print("  5. Carregamento de Configurações")
    print("  6. Dados IBGE (opcional)")
    print("  7. Geração de Gráficos")
    print("  8. Executar TODOS os exemplos")
    print("  0. Sair")
    
    opcao = input("\nEscolha uma opção: ").strip()
    
    if opcao == '0':
        print("\n👋 Encerrando...")
        return
    
    elif opcao == '1':
        exemplo_cinematica_basica()
    
    elif opcao == '2':
        exemplo_comparacao_culturas()
    
    elif opcao == '3':
        exemplo_torque_fvs_variavel()
    
    elif opcao == '4':
        exemplo_distribuicao_sementes()
    
    elif opcao == '5':
        exemplo_configuracoes()
    
    elif opcao == '6':
        exemplo_dados_ibge()
    
    elif opcao == '7':
        exemplo_gerar_graficos()
    
    elif opcao == '8':
        print("\n🚀 Executando TODOS os exemplos...\n")
        exemplo_cinematica_basica()
        exemplo_comparacao_culturas()
        exemplo_torque_fvs_variavel()
        exemplo_distribuicao_sementes()
        exemplo_configuracoes()
        exemplo_dados_ibge()
        exemplo_gerar_graficos()
    
    else:
        print("\n❌ Opção inválida!")
        return
    
    # Finalização
    print("\n" + "=" * 80)
    print("✅ EXEMPLO(S) CONCLUÍDO(S)!")
    print("=" * 80)
    print("\n💡 Dicas:")
    print("  • Use 'python main.py' para interface completa")
    print("  • Veja 'docs/INICIO_RAPIDO.md' para mais exemplos")
    print("  • Leia 'README.md' para documentação completa")
    print("\n📖 TCC completo: https://repositorio.ufsc.br/handle/123456789/270766")
    print("=" * 80)


if __name__ == "__main__":
    main()
