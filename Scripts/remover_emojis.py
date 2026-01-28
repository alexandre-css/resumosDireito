#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove todos os emojis e substitui por Google Material Symbols
"""
import os
import re

# Mapeamento de emojis para Material Symbols
EMOJI_TO_ICON = {
    '📝': '<span class="material-symbols-outlined">edit_note</span>',
    '🔄': '<span class="material-symbols-outlined">sync</span>',
    '🚀': '<span class="material-symbols-outlined">rocket_launch</span>',
    '📋': '<span class="material-symbols-outlined">description</span>',
    '🎯': '<span class="material-symbols-outlined">target</span>',
    '💡': '<span class="material-symbols-outlined">lightbulb</span>',
    '⏳': '<span class="material-symbols-outlined">hourglass_empty</span>',
    '✓': '<span class="material-symbols-outlined">check</span>',
    '✅': '<span class="material-symbols-outlined">check_circle</span>',
    '❌': '<span class="material-symbols-outlined">cancel</span>',
    '⚠️': '<span class="material-symbols-outlined">warning</span>',
    '📊': '<span class="material-symbols-outlined">bar_chart</span>',
    '🔍': '<span class="material-symbols-outlined">search</span>',
    '✏️': '<span class="material-symbols-outlined">edit</span>',
    '➕': '<span class="material-symbols-outlined">add</span>',
    '🗑️': '<span class="material-symbols-outlined">delete</span>',
    '📦': '<span class="material-symbols-outlined">inventory_2</span>',
    '🔧': '<span class="material-symbols-outlined">build</span>',
    '👈': '<span class="material-symbols-outlined">arrow_back</span>',
    '⚙️': '<span class="material-symbols-outlined">settings</span>',
    '💾': '<span class="material-symbols-outlined">save</span>',
    '✖': '<span class="material-symbols-outlined">close</span>',
    '✖️': '<span class="material-symbols-outlined">close</span>',
}

def adicionar_material_symbols_link(content):
    """Adiciona o link do Google Material Symbols se não existir"""
    if 'fonts.googleapis.com/css2?family=Material+Symbols+Outlined' in content:
        return content
    
    # Procurar pela tag </head> e adicionar antes dela
    head_close = '</head>'
    if head_close in content:
        link_tag = '''
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />'''
        content = content.replace(head_close, link_tag + '\n' + head_close)
    
    return content

def substituir_emojis(content):
    """Substitui emojis por Material Symbols"""
    for emoji, icon in EMOJI_TO_ICON.items():
        content = content.replace(emoji, icon)
    return content

def processar_arquivo(filepath):
    """Processa um arquivo substituindo emojis"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Adicionar link do Material Symbols se for HTML
        if 'text/html' in content or '<html' in content.lower():
            content = adicionar_material_symbols_link(content)
        
        # Substituir emojis
        content = substituir_emojis(content)
        
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
    print("REMOVEDOR DE EMOJIS - Substituição por Material Symbols")
    print("="*80)
    print()
    
    arquivos_processados = 0
    arquivos_modificados = 0
    
    # Processar editores
    editores = [
        'Scripts/editors/2_servidor_sumulas.py',
        'Scripts/editors/2_servidor_temas.py',
        'Scripts/editors/3_servidor_unificado.py'
    ]
    
    print("Processando editores...")
    for arquivo in editores:
        if os.path.exists(arquivo):
            arquivos_processados += 1
            if processar_arquivo(arquivo):
                arquivos_modificados += 1
                print(f"   [OK] {arquivo}")
    
    print()
    print("="*80)
    print(f"CONCLUÍDO!")
    print(f"Arquivos processados: {arquivos_processados}")
    print(f"Arquivos modificados: {arquivos_modificados}")
    print("="*80)
    print()
    print("NOTA: Os ícones Material Symbols serão carregados via CDN")
    print("Link adicionado: https://fonts.googleapis.com/css2...")
    print()

if __name__ == '__main__':
    main()
