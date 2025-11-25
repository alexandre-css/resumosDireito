@echo off
chcp 65001 > nul
title Editor de Súmulas - Servidor Web
color 0B

echo ================================================================================
echo                     EDITOR DE SÚMULAS - SERVIDOR WEB
echo ================================================================================
echo.

cd /d "%~dp0"
python Scripts/3_servidor_editor.py
