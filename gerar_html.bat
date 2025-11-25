@echo off
chcp 65001 > nul
title Atualizar Súmulas - HTML Generator
color 0A

echo ================================================================================
echo                     GERADOR DE HTML DE SÚMULAS
echo ================================================================================
echo.

cd /d "%~dp0"
python Scripts/2_gerar_html.py

echo.
echo ================================================================================
echo Pressione qualquer tecla para fechar...
pause > nul

