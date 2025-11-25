@echo off
chcp 65001 > nul
title Configurar Categorias - Súmulas
color 0B

echo ================================================================================
echo                  CONFIGURAR CATEGORIAS DAS CORES
echo ================================================================================
echo.
echo Este utilitário abre o navegador para configurar as categorias.
echo.
echo Certifique-se de que o editor está rodando!
echo.
echo Pressione qualquer tecla para abrir...
pause > nul

start http://localhost:8080/config
