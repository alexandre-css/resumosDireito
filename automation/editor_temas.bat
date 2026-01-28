@echo off
chcp 65001 > nul
title Editor de Temas - Servidor Web
color 0B

echo ================================================================================
echo                      EDITOR DE TEMAS - SERVIDOR WEB
echo ================================================================================
echo.

cd /d "%~dp0"
python Scripts/editors/2_servidor_temas.py
