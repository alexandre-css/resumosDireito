@echo off
title Reorganização do Projeto - ResumosDireito
color 0A

echo ========================================
echo   REORGANIZACAO DO PROJETO
echo   ResumosDireito v2.0
echo ========================================
echo.
echo Este script vai reorganizar o projeto
echo seguindo a estrutura profissional.
echo.
echo IMPORTANTE: Faca backup antes!
echo.
pause

echo.
echo [1/5] Criando estrutura de diretorios...
mkdir public 2>nul
mkdir automation 2>nul
mkdir Scripts\generators 2>nul
mkdir Scripts\editors 2>nul
mkdir Scripts\extractors 2>nul
echo [OK] Diretorios criados

echo.
echo [2/5] Movendo arquivos HTML para public/...
move /Y acordao.html public\ >nul 2>&1
move /Y civil.html public\ >nul 2>&1
move /Y honorarios.html public\ >nul 2>&1
move /Y index.html public\ >nul 2>&1
move /Y penal.html public\ >nul 2>&1
move /Y sumulas.html public\ >nul 2>&1
move /Y temas.html public\ >nul 2>&1
echo [OK] HTMLs movidos

echo.
echo [3/5] Reorganizando scripts Python...

REM Generators
if exist "Scripts\2_gerar_html.py" (
    move /Y "Scripts\2_gerar_html.py" "Scripts\generators\1_gerar_html_sumulas.py" >nul 2>&1
)
if exist "Scripts\2_gerar_html_temas.py" (
    move /Y "Scripts\2_gerar_html_temas.py" "Scripts\generators\1_gerar_html_temas.py" >nul 2>&1
)

REM Editors
if exist "Scripts\3_servidor_editor.py" (
    move /Y "Scripts\3_servidor_editor.py" "Scripts\editors\2_servidor_sumulas.py" >nul 2>&1
)
if exist "Scripts\4_servidor_editor_temas.py" (
    move /Y "Scripts\4_servidor_editor_temas.py" "Scripts\editors\2_servidor_temas.py" >nul 2>&1
)
if exist "Scripts\5_editor_unificado.py" (
    move /Y "Scripts\5_editor_unificado.py" "Scripts\editors\3_servidor_unificado.py" >nul 2>&1
)

REM Extractors
if exist "Scripts\1_extrair_sumulas.py" (
    move /Y "Scripts\1_extrair_sumulas.py" "Scripts\extractors\" >nul 2>&1
)
if exist "Scripts\1_extrair_temas.py" (
    move /Y "Scripts\1_extrair_temas.py" "Scripts\extractors\" >nul 2>&1
)

echo [OK] Scripts reorganizados

echo.
echo [4/5] Movendo arquivos .bat para automation/...
move /Y configurar_categorias.bat automation\ >nul 2>&1
move /Y editor.bat automation\ >nul 2>&1
move /Y editor_temas.bat automation\ >nul 2>&1
move /Y gerar_html.bat automation\ >nul 2>&1
REM Manter editor_unificado.bat na raiz por ser o principal
copy /Y editor_unificado.bat automation\ >nul 2>&1
echo [OK] Automacao organizada

echo.
echo [5/5] Limpando arquivos desnecessarios...
if exist "ORGANIZACAO_CONCLUIDA.md" del "ORGANIZACAO_CONCLUIDA.md" >nul 2>&1
if exist "ESTRUTURA.md" del "ESTRUTURA.md" >nul 2>&1
echo [OK] Limpeza concluida

echo.
echo ========================================
echo   REORGANIZACAO CONCLUIDA!
echo ========================================
echo.
echo Estrutura atual:
echo   public/          - Arquivos HTML
echo   Data/            - Dados JSON
echo   Scripts/         - Scripts Python organizados
echo   automation/      - Arquivos .bat
echo   docs/            - Documentacao
echo   backup/          - Backups
echo.
echo PROXIMO PASSO:
echo   Execute: python Scripts\atualizar_referencias.py
echo   Para corrigir caminhos nos arquivos
echo.
pause
