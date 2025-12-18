#!/usr/bin/env pwsh
# ============================================================================
# Script de Setup Automático - Dosador de Sementes
# ============================================================================
# Este script cria um ambiente virtual Python e instala todas as dependências
# Autor: José Gabriel Furlan De Barros
# ============================================================================

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host " SETUP AUTOMÁTICO - Dosador de Sementes" -ForegroundColor Cyan
Write-Host " Sistema de Análise de Semeadura por Puncionamento" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[1/4] Python encontrado:" -ForegroundColor Green
    Write-Host "      $pythonVersion" -ForegroundColor White
    Write-Host ""
}
catch {
    Write-Host "[ERRO] Python não encontrado!" -ForegroundColor Red
    Write-Host "Por favor, instale Python 3.8 ou superior: https://www.python.org/" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Criar ambiente virtual
Write-Host "[2/4] Criando ambiente virtual..." -ForegroundColor Yellow

if (Test-Path "venv") {
    Write-Host "Ambiente virtual já existe." -ForegroundColor Yellow
    $recriar = Read-Host "Deseja recriar? (S/N)"

    if ($recriar -eq "S" -or $recriar -eq "s") {
        Write-Host "Removendo ambiente virtual antigo..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force venv
        python -m venv venv
        Write-Host "Ambiente virtual recriado!" -ForegroundColor Green
    }
    else {
        Write-Host "Usando ambiente virtual existente." -ForegroundColor Green
    }
}
else {
    python -m venv venv
    Write-Host "Ambiente virtual criado!" -ForegroundColor Green
}
Write-Host ""

# Ativar ambiente virtual
Write-Host "[3/4] Ativando ambiente virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "Ambiente virtual ativado!" -ForegroundColor Green
Write-Host ""

# Instalar dependências
Write-Host "[4/4] Instalando dependências..." -ForegroundColor Yellow
Write-Host "Isso pode levar alguns minutos..." -ForegroundColor Cyan
Write-Host ""

python -m pip install --upgrade pip --quiet
pip install -r requirements.txt

Write-Host ""

# Verificar instalação
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Verificando instalação..." -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

try {
    python -c "from core import cinematica; print('>>> Módulos OK!')"
    Write-Host "[OK] Instalação concluída com sucesso!" -ForegroundColor Green
}
catch {
    Write-Host "[AVISO] Erro ao importar módulos. Verifique a instalação." -ForegroundColor Yellow
}
Write-Host ""

# Instruções finais
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host " INSTALAÇÃO CONCLUÍDA!" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para usar o sistema:" -ForegroundColor White
Write-Host "  1. Ative o ambiente virtual: .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "  2. Execute o sistema: python main.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ou simplesmente execute: .\run.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "No VS Code, o ambiente virtual será ativado automaticamente!" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Pressione Enter para sair"
