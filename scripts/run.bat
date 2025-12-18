@echo off
REM ============================================================================
REM Script de Execucao Rapida - Dosador de Sementes
REM ============================================================================

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo Executando sistema...
python main.py

pause
