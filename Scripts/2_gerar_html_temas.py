#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar HTML de Temas a partir dos JSONs
"""

import json
import os
import re
from datetime import datetime

# Mapeamento de cores para intensidades
CORES_INTENSIDADE = {
    'red': '500', 'blue': '500', 'green': '500', 'purple': '500',
    'pink': '500', 'indigo': '500', 'yellow': '500', 'orange': '500',
    'teal': '500', 'cyan': '500', 'lime': '500', 'emerald': '500',
    'violet': '500', 'fuchsia': '500', 'rose': '500', 'magenta': '500',
    'amber': '500', 'gray': '600', 'brown': '500', 'coral': '500',
    'stone': '500', 'neutral': '600', 'warmGray': '600', 'trueGray': '600',
    'coolGray': '600', 'blueGray': '600'
}

def carregar_temas(diretorio='Data'):
    """Carrega temas dos JSONs"""
    temas = {}
    
    for tribunal in ['stf', 'stj']:
        arquivo = os.path.join(diretorio, f'temas_{tribunal}.json')
        with open(arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
            temas[tribunal] = data.get('temas', [])
            print(f'   [OK] {tribunal.upper()}: {len(temas[tribunal])} temas')
    
    return temas

def gerar_card_tema(tema, tribunal):
    """Gera HTML de um card de tema"""
    numero = tema['numero']
    titulo = tema.get('titulo', '')
    tese = tema['tese']
    comentario = tema.get('comentario', '')
    cor = tema.get('cor', 'blue')
    chips = tema.get('chips', [])
    
    intensidade = CORES_INTENSIDADE.get(cor, '500')
    
    # Classes do card - sempre bg-white com borda colorida (não vinculante)
    card_classes = f"bg-white border-l-4 border-{cor}-{intensidade}"
    text_color = "text-gray-700"
    title_color = f"text-{cor}-700"
    numero_bg = f"bg-{cor}-{intensidade}"
    numero_text = "text-white"
    
    # Badge do tribunal
    badge_tribunal = 'STF' if tribunal == 'stf' else 'STJ'
    
    # Montar HTML
    html = f'''
                                <!-- Tema {numero}/{tribunal.upper()} -->
                                <div
                                    class="{card_classes} rounded-lg p-4 shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 tema-card relative"
                                    onclick="copiarTema({numero}, '{badge_tribunal}', `{tese}`)">
                                    <div class="flex items-center mb-2">
                                        <div
                                            class="{numero_bg} {numero_text} rounded-full w-10 h-10 flex items-center justify-center text-sm font-bold mr-3">
                                            {numero}</div>
'''
    
    # Adicionar título se existir
    if titulo:
        html += f'''
                                        <h4 class="font-bold {title_color}">{titulo}</h4>
'''
    
    # Adicionar chips se houver
    if chips:
        html += '''
                                        <div class="flex flex-wrap gap-1''' + (' ml-auto' if not titulo else '') + '''">
'''
        for chip in chips:
            html += f'''
                                            <span class="px-2 py-1 bg-{cor}-100 text-{cor}-700 rounded text-xs font-medium">{chip}</span>
'''
        html += '''
                                        </div>
'''
    
    html += f'''
                                    </div>
                                    <p class="text-sm {text_color} italic text-justify leading-relaxed">{tese}</p>
'''
    
    # Adicionar comentário se houver
    if comentario:
        html += f'''
                                    <p class="text-xs bg-{cor}-50 p-2 rounded border-l-2 border-{cor}-300 mt-2 text-justify">{comentario}</p>'''
    
    html += '''
                                </div>
'''
    
    return html

def gerar_secao_tribunal(tribunal, temas):
    """Gera seção HTML de um tribunal"""
    tribunal_upper = tribunal.upper()
    titulo = 'Temas de Repercussão Geral' if tribunal == 'stf' else 'Temas Repetitivos'
    titulo_curto = f'Temas do {tribunal_upper}'
    cor_titulo = 'red' if tribunal == 'stf' else 'indigo'
    cor_bg = 'red' if tribunal == 'stf' else 'blue'
    
    html = f'''
            <!-- TEMAS DO {tribunal_upper} -->
            <div class="mt-16">
                <div class="text-center mb-6 cursor-pointer" onclick="toggleTemas('{tribunal}')">
                    <h2
                        class="text-2xl font-bold text-{cor_titulo}-800 flex items-center justify-center hover:text-{cor_titulo}-600 transition-colors">
                        {titulo_curto}
                        <svg id="arrow-{tribunal}" class="w-6 h-6 ml-2 transform transition-transform duration-300"
                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M19 9l-7 7-7-7">
                            </path>
                        </svg>
                    </h2>
                    <p class="text-sm text-gray-600 mt-2">Clique para expandir/recolher • {len(temas)} temas</p>
                </div>

                <div id="temas-{tribunal}" class="overflow-hidden transition-all duration-500 max-h-0">
                    <div class="relative">
                        <div
                            class="absolute inset-0 bg-gradient-to-r from-{cor_bg}-100 via-{cor_bg}-50 to-{cor_bg}-100 rounded-2xl opacity-30">
                        </div>
                        <div class="relative grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 p-6">
'''
    
    for tema in temas:
        html += gerar_card_tema(tema, tribunal)
    
    html += '''
                        </div>
                    </div>
                </div>
            </div>
'''
    
    return html

def gerar_html_completo(temas):
    """Gera HTML completo substituindo apenas a seção de temas"""
    # Ler template HTML atual
    template_file = 'temas.html'
    
    if not os.path.exists(template_file):
        # Criar template inicial
        return gerar_template_inicial(temas)
    
    with open(template_file, 'r', encoding='utf-8') as f:
        html_atual = f.read()
    
    # Gerar HTML dos temas
    html_temas = ''
    html_temas += gerar_secao_tribunal('stf', temas['stf'])
    html_temas += gerar_secao_tribunal('stj', temas['stj'])
    
    # Substituir seção de temas
    pattern = r'(<!-- TEMAS DO STF -->.*?)(<script>)'
    html_novo = re.sub(pattern, html_temas + r'\n            \2', html_atual, flags=re.DOTALL)
    
    return html_novo

def gerar_template_inicial(temas):
    """Gera template HTML inicial para temas"""
    html_temas = ''
    html_temas += gerar_secao_tribunal('stf', temas['stf'])
    html_temas += gerar_secao_tribunal('stj', temas['stj'])
    
    return f'''<!DOCTYPE html>
<html lang="pt-BR">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Temas - Processo Penal</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {{
                theme: {{
                    extend: {{
                        colors: {{
                            magenta: {{
                                50: '#fdf2f8',
                                100: '#fce7f3',
                                200: '#fbcfe8',
                                300: '#f9a8d4',
                                400: '#f472b6',
                                500: '#e11d48',
                                600: '#be123c',
                                700: '#9f1239',
                                800: '#881337',
                                900: '#701a2e'
                            }},
                            coral: {{
                                50: '#fff1f2',
                                100: '#ffe4e6',
                                200: '#fecdd3',
                                300: '#fda4af',
                                400: '#fb7185',
                                500: '#fb7185',
                                600: '#f43f5e',
                                700: '#e11d48',
                                800: '#be123c',
                                900: '#9f1239'
                            }},
                            brown: {{
                                50: '#fefce8',
                                100: '#fef9c3',
                                200: '#fef08a',
                                300: '#fde047',
                                400: '#facc15',
                                500: '#92400e',
                                600: '#78350f',
                                700: '#78350f',
                                800: '#451a03',
                                900: '#451a03'
                            }}
                        }}
                    }}
                }}
            }}
            window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};
        </script>
        <script defer src="https://cdn.vercel-insights.com/v1/script.debug.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

            body {{
                font-family: 'Roboto', sans-serif;
                background-color: #f0f4f8;
            }}

            .section-card {{
                transition: all 0.3s ease;
            }}

            .section-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            }}

            #sidenav-backdrop {{
                transition: opacity 0.3s ease;
            }}

            #sidenav {{
                transition: transform 0.3s ease;
            }}

            .tema-card {{
                cursor: pointer;
                user-select: none;
            }}

            .tema-card:active {{
                transform: scale(0.98) !important;
            }}
        </style>
    </head>

    <body>
        <nav class="bg-blue-900 text-white shadow-lg">
            <div class="container mx-auto px-4">
                <div class="flex justify-between items-center py-4">
                    <div class="flex items-center">
                        <button id="sidenav-toggle" class="mr-4 text-white hover:text-blue-200 transition">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 6h16M4 12h16M4 18h16"></path>
                            </svg>
                        </button>
                        <div class="flex items-center gap-2">
                            <span class="text-2xl">⚖️</span>
                            <h1 class="text-2xl font-bold">Temas de Processo Penal</h1>
                        </div>
                    </div>
                    <a href="index.html" 
                       class="bg-blue-700 hover:bg-blue-600 px-4 py-2 rounded-lg transition flex items-center gap-2">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
                        </svg>
                        Início
                    </a>
                </div>
            </div>
        </nav>

        <!-- Menu Lateral -->
        <div id="sidenav-backdrop" class="fixed inset-0 bg-black opacity-0 pointer-events-none z-40"></div>
        <div id="sidenav"
            class="fixed left-0 top-0 h-full w-80 bg-white shadow-2xl transform -translate-x-full z-50 overflow-y-auto">
            <div class="p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold text-gray-800">Menu</h2>
                    <button id="sidenav-close" class="text-gray-600 hover:text-gray-800">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <nav class="space-y-2">
                    <a href="index.html"
                        class="flex items-center gap-3 p-3 rounded-lg hover:bg-blue-50 text-gray-700 hover:text-blue-600 transition">
                        <span class="text-xl">🏛️</span>
                        <span class="font-medium">Honorários</span>
                    </a>
                    <a href="sumulas.html"
                        class="flex items-center gap-3 p-3 rounded-lg hover:bg-blue-50 text-gray-700 hover:text-blue-600 transition">
                        <span class="text-xl">📋</span>
                        <span class="font-medium">Súmulas</span>
                    </a>
                    <a href="temas.html"
                        class="flex items-center gap-3 p-3 rounded-lg bg-blue-50 text-blue-600 transition">
                        <span class="text-xl">🎯</span>
                        <span class="font-medium">Temas</span>
                    </a>
                </nav>
            </div>
        </div>

        <div class="container mx-auto px-4 py-8">
            <!-- Filtros e Busca -->
            <div class="bg-white rounded-lg shadow-md p-6 mb-8">
                <div class="flex items-center gap-4 mb-4">
                    <button onclick="filtrarTribunal('todos')" id="btn-todos"
                        class="px-6 py-2 rounded-lg font-semibold bg-blue-600 text-white">
                        Todos
                    </button>
                    <button onclick="filtrarTribunal('stf')" id="btn-stf"
                        class="px-6 py-2 rounded-lg font-semibold bg-gray-200 text-gray-700 hover:bg-gray-300">
                        STF
                    </button>
                    <button onclick="filtrarTribunal('stj')" id="btn-stj"
                        class="px-6 py-2 rounded-lg font-semibold bg-gray-200 text-gray-700 hover:bg-gray-300">
                        STJ
                    </button>
                </div>
                <div class="relative">
                    <input type="text" id="busca" placeholder="🔍 Buscar temas..."
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        oninput="buscarTemas()">
                </div>
            </div>

            {html_temas}
        </div>

        <script>
            let tribunalAtual = 'todos';

            function copiarTema(numero, tribunal, tese) {{
                const texto = `Tema ${{numero}}/${{tribunal}}: "${{tese}}"`;
                navigator.clipboard.writeText(texto).then(() => {{
                    // Feedback visual
                    const card = event.currentTarget;
                    card.classList.add('ring-4', 'ring-green-400');
                    setTimeout(() => {{
                        card.classList.remove('ring-4', 'ring-green-400');
                    }}, 300);
                }});
            }}

            function filtrarTribunal(tribunal) {{
                tribunalAtual = tribunal;
                
                // Atualizar botões
                ['todos', 'stf', 'stj'].forEach(t => {{
                    const btn = document.getElementById(`btn-${{t}}`);
                    if (t === tribunal) {{
                        btn.className = 'px-6 py-2 rounded-lg font-semibold bg-blue-600 text-white';
                    }} else {{
                        btn.className = 'px-6 py-2 rounded-lg font-semibold bg-gray-200 text-gray-700 hover:bg-gray-300';
                    }}
                }});
                
                // Mostrar/ocultar seções
                document.getElementById('stf-section').style.display = 
                    (tribunal === 'todos' || tribunal === 'stf') ? 'block' : 'none';
                document.getElementById('stj-section').style.display = 
                    (tribunal === 'todos' || tribunal === 'stj') ? 'block' : 'none';
                
                buscarTemas();
            }}

            function buscarTemas() {{
                const termo = document.getElementById('busca').value.toLowerCase();
                const tribunais = tribunalAtual === 'todos' ? ['stf', 'stj'] : [tribunalAtual];
                
                tribunais.forEach(tribunal => {{
                    const cards = document.querySelectorAll(`#${{tribunal}}-grid .tema-card`);
                    cards.forEach(card => {{
                        const texto = card.textContent.toLowerCase();
                        card.style.display = texto.includes(termo) ? 'block' : 'none';
                    }});
                }});
            }}

            // Menu lateral
            const sidenavToggle = document.getElementById('sidenav-toggle');
            const sidenavClose = document.getElementById('sidenav-close');
            const sidenav = document.getElementById('sidenav');
            const sidenavBackdrop = document.getElementById('sidenav-backdrop');

            function openSidenav() {{
                sidenav.classList.remove('-translate-x-full');
                sidenavBackdrop.classList.remove('pointer-events-none', 'opacity-0');
                sidenavBackdrop.classList.add('opacity-50');
            }}

            function closeSidenav() {{
                sidenav.classList.add('-translate-x-full');
                sidenavBackdrop.classList.add('pointer-events-none', 'opacity-0');
                sidenavBackdrop.classList.remove('opacity-50');
            }}

            sidenavToggle.addEventListener('click', openSidenav);
            sidenavClose.addEventListener('click', closeSidenav);
            sidenavBackdrop.addEventListener('click', closeSidenav);
        </script>
    </body>
</html>'''

def salvar_html(html, arquivo='temas.html', backup=True):
    """Salva HTML gerando backup do original"""
    if backup and os.path.exists(arquivo):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        os.makedirs('backup', exist_ok=True)
        backup_file = f'backup/{arquivo}.backup_{timestamp}'
        
        # Copiar ao invés de renomear
        import shutil
        shutil.copy2(arquivo, backup_file)
        print(f'[OK] Backup criado: {backup_file}')
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'[OK] HTML gerado: {arquivo}')

def main():
    print('='*80)
    print('GERADOR DE HTML DE TEMAS')
    print('='*80)
    print()
    
    print('1. Carregando temas dos JSONs...')
    temas = carregar_temas()
    print()
    
    print('2. Gerando HTML...')
    html = gerar_html_completo(temas)
    print('   [OK] HTML gerado')
    print()
    
    print('3. Salvando arquivo...')
    salvar_html(html)
    print()
    
    print('='*80)
    print('[OK] CONCLUÍDO COM SUCESSO!')
    print('='*80)

if __name__ == '__main__':
    main()
