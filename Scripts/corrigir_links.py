#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir links duplicados nos arquivos HTML
Remove 'public/public\' e substitui por apenas o nome do arquivo
"""
import os
import re
from pathlib import Path

def corrigir_links_html(filepath):
    """Corrige links duplicados em um arquivo HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Padrões a corrigir
        patterns = [
            (r'public/public\\(\w+\.html)', r'\1'),  # public/public\arquivo.html -> arquivo.html
            (r'public/public/(\w+\.html)', r'\1'),   # public/public/arquivo.html -> arquivo.html
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    
    except Exception as e:
        print(f"   [ERRO] {filepath}: {e}")
        return False

def main():
    print("="*80)
    print("CORRETOR DE LINKS DUPLICADOS")
    print("="*80)
    print()
    
    # Diretórios para processar
    dirs_to_process = ['public', '.']
    
    arquivos_corrigidos = 0
    total_arquivos = 0
    
    for dir_name in dirs_to_process:
        if not os.path.exists(dir_name):
            continue
        
        # Processar HTMLs diretamente no diretório (não recursivo)
        for filename in os.listdir(dir_name):
            if filename.endswith('.html'):
                filepath = os.path.join(dir_name, filename)
                if os.path.isfile(filepath):
                    total_arquivos += 1
                    
                    if corrigir_links_html(filepath):
                        arquivos_corrigidos += 1
                        print(f"   [OK] {filepath}")
    
    print()
    print("="*80)
    print(f"CONCLUIDO!")
    print(f"Total de arquivos processados: {total_arquivos}")
    print(f"Arquivos corrigidos: {arquivos_corrigidos}")
    print("="*80)
    print()

if __name__ == '__main__':
    main()
