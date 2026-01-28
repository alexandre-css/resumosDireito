@echo off
chcp 65001 > nul
title Atualizar Súmulas - HTML Generator
color 0A

echo ================================================================================
echo                     GERADOR DE HTML DE SÚMULAS
echo ================================================================================
echo.

cd /d "%~dp0"
python Scripts/generators/1_gerar_html_sumulas.py

echo.
echo ================================================================================
echo Pressione qualquer tecla para fechar...
pause > nul

