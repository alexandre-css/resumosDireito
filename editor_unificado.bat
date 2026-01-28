@echo off
title Editor Unificado - Súmulas e Temas
color 0B

echo ========================================
echo   Editor Unificado - Sistema Completo
echo ========================================
echo.

REM Iniciar editor de súmulas em segundo plano
echo [1/3] Iniciando editor de súmulas (porta 8001)...
start "Editor Sumulas" /MIN cmd /c "python Scripts\3_servidor_editor.py"

REM Aguardar 2 segundos
timeout /t 2 /nobreak >nul

REM Iniciar editor de temas em segundo plano
echo [2/3] Iniciando editor de temas (porta 8002)...
start "Editor Temas" /MIN cmd /c "python Scripts\4_servidor_editor_temas.py"

REM Aguardar 2 segundos
timeout /t 2 /nobreak >nul

REM Iniciar editor unificado (abrirá o navegador automaticamente)
echo [3/3] Iniciando editor unificado (porta 8000)...
echo.
echo ========================================
echo   PRONTO!
echo ========================================
echo.
echo   Editor Unificado: http://localhost:8000
echo   Editor Sumulas:   http://localhost:8001
echo   Editor Temas:     http://localhost:8002
echo.
echo   Servidores rodando em segundo plano:
echo   - Editor de Sumulas (porta 8001)
echo   - Editor de Temas (porta 8002)
echo   - Editor Unificado (porta 8000)
echo.
echo   Feche TODAS as janelas para parar
echo ========================================
echo.

python Scripts\5_editor_unificado.py

pause
