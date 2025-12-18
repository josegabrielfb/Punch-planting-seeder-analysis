#!/usr/bin/env pwsh
# ============================================================================
# Script de Execução Rápida - Dosador de Sementes
# ============================================================================

Write-Host "Ativando ambiente virtual..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

Write-Host "Executando sistema..." -ForegroundColor Green
python main.py

Read-Host "Pressione Enter para sair"
