@echo off
REM ============================================================================
REM Script de Setup Automatico - Dosador de Sementes
REM ============================================================================
REM Este script cria um ambiente virtual Python e instala todas as dependencias
REM Autor: Jose Gabriel Furlan De Barros
REM ============================================================================

echo.
echo ============================================================================
echo  SETUP AUTOMATICO - Dosador de Sementes
echo  Sistema de Analise de Semeadura por Puncionamento
echo ============================================================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale Python 3.8 ou superior: https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo [1/4] Python encontrado:
python --version
echo.

REM Criar ambiente virtual
echo [2/4] Criando ambiente virtual...
if exist "venv" (
    echo Ambiente virtual ja existe. Deseja recriar? (S/N)
    set /p recriar=
    if /i "%recriar%"=="S" (
        echo Removendo ambiente virtual antigo...
        rmdir /s /q venv
        python -m venv venv
        echo Ambiente virtual recriado!
    ) else (
        echo Usando ambiente virtual existente.
    )
) else (
    python -m venv venv
    echo Ambiente virtual criado!
)
echo.

REM Ativar ambiente virtual
echo [3/4] Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo Ambiente virtual ativado!
echo.

REM Instalar dependencias
echo [4/4] Instalando dependencias...
echo Isso pode levar alguns minutos...
echo.
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Verificar instalacao
echo ============================================================================
echo Verificando instalacao...
echo ============================================================================
python -c "from core import cinematica; print('>>> Modulos OK!')" 2>nul
if errorlevel 1 (
    echo [AVISO] Erro ao importar modulos. Verifique a instalacao.
) else (
    echo [OK] Instalacao concluida com sucesso!
)
echo.

REM Instrucoes finais
echo ============================================================================
echo  INSTALACAO CONCLUIDA!
echo ============================================================================
echo.
echo Para usar o sistema:
echo   1. Ative o ambiente virtual: venv\Scripts\activate
echo   2. Execute o sistema: python main.py
echo.
echo Ou simplesmente execute: run.bat
echo.
echo No VS Code, o ambiente virtual sera ativado automaticamente!
echo ============================================================================
echo.

pause
