#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Atualização de Referências
Atualiza caminhos de arquivos após reorganização do projeto
"""
import os
import re
from pathlib import Path

# Mapeamento de mudanças de caminho
UPDATES = {
    # Scripts Python - geradores
    'Scripts/2_gerar_html.py': 'Scripts/generators/1_gerar_html_sumulas.py',
    'Scripts/2_gerar_html_temas.py': 'Scripts/generators/1_gerar_html_temas.py',
    
    # Scripts Python - editores
    'Scripts/3_servidor_editor.py': 'Scripts/editors/2_servidor_sumulas.py',
    'Scripts/4_servidor_editor_temas.py': 'Scripts/editors/2_servidor_temas.py',
    'Scripts/5_editor_unificado.py': 'Scripts/editors/3_servidor_unificado.py',
    
    # Scripts Python - extractors
    'Scripts/1_extrair_sumulas.py': 'Scripts/extractors/extrair_sumulas.py',
    'Scripts/1_extrair_temas.py': 'Scripts/extractors/extrair_temas.py',
    
    # HTMLs
    'sumulas.html': 'public/sumulas.html',
    'temas.html': 'public/temas.html',
    'index.html': 'public/index.html',
    'penal.html': 'public/penal.html',
    'civil.html': 'public/civil.html',
    'acordao.html': 'public/acordao.html',
    'honorarios.html': 'public/honorarios.html',
}

def atualizar_arquivo(filepath, updates):
    """Atualiza referências em um arquivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modificado = False
        
        for old_path, new_path in updates.items():
            # Normalizar barras
            old_path_normalized = old_path.replace('/', '\\')
            new_path_normalized = new_path.replace('/', '\\')
            
            # Substituir no conteúdo
            if old_path in content or old_path_normalized in content:
                content = content.replace(old_path, new_path)
                content = content.replace(old_path_normalized, new_path_normalized)
                modificado = True
        
        if modificado:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    
    except Exception as e:
        print(f"   [ERRO] {filepath}: {e}")
        return False

def main():
    print("="*80)
    print("ATUALIZADOR DE REFERENCIAS - ResumosDireito")
    print("="*80)
    print()
    
    # Diretórios para processar
    dirs_to_process = [
        'Scripts',
        'automation',
        'public',
        'docs'
    ]
    
    arquivos_atualizados = 0
    total_arquivos = 0
    
    for dir_name in dirs_to_process:
        if not os.path.exists(dir_name):
            continue
        
        print(f"Processando: {dir_name}/")
        
        for root, dirs, files in os.walk(dir_name):
            for filename in files:
                if filename.endswith(('.py', '.bat', '.html', '.md')):
                    filepath = os.path.join(root, filename)
                    total_arquivos += 1
                    
                    if atualizar_arquivo(filepath, UPDATES):
                        arquivos_atualizados += 1
                        print(f"   [OK] {filepath}")
    
    print()
    print("="*80)
    print(f"CONCLUIDO!")
    print(f"Total de arquivos processados: {total_arquivos}")
    print(f"Arquivos atualizados: {arquivos_atualizados}")
    print("="*80)
    print()
    print("PROXIMO PASSO:")
    print("   Teste todas as funcionalidades:")
    print("   1. Execute: editor_unificado.bat")
    print("   2. Verifique se os editores abrem corretamente")
    print("   3. Teste a geracao de HTML")
    print()

if __name__ == '__main__':
    main()
