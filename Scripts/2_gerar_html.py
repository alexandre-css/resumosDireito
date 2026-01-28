# -*- coding: utf-8 -*-
"""
Gera o HTML das súmulas a partir dos arquivos JSON
USO: python gerar_sumulas_html.py
"""
import json
import os
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

def carregar_sumulas(diretorio='Data'):
    """Carrega súmulas dos arquivos JSON"""
    sumulas = {}
    for tribunal in ['stf', 'stj', 'eca']:
        arquivo = f'{diretorio}/{tribunal}.json'
        if os.path.exists(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                sumulas[tribunal] = data['sumulas']
        else:
            sumulas[tribunal] = []
    return sumulas

def gerar_card_sumula(sumula, tribunal):
    """Gera HTML de um card de súmula"""
    numero = sumula['numero']
    titulo = sumula['titulo']
    texto = sumula['texto']
    cor = sumula.get('cor', 'blue')
    vinculante = sumula.get('vinculante', False)
    chips = sumula.get('chips', [])
    nota = sumula.get('nota')
    modulacao_efeitos = sumula.get('modulacao_efeitos', '')
    
    intensidade = CORES_INTENSIDADE.get(cor, '500')
    
    # Determinar classes do card
    if vinculante:
        card_classes = f"bg-gradient-to-r from-{cor}-500 to-{cor}-700 border-l-4 border-{cor}-900"
        text_color = "text-white"
        title_color = "text-white"
        numero_bg = "bg-white"
        numero_text = f"text-{cor}-700"
    else:
        card_classes = f"bg-white border-l-4 border-{cor}-{intensidade}"
        text_color = "text-gray-700"
        title_color = f"text-{cor}-700"
        numero_bg = f"bg-{cor}-{intensidade}"
        numero_text = "text-white"
    
    # Montar HTML
    html = f'''
                                <!-- Súmula {numero}/{tribunal.upper()} -->
                                <div
                                    class="{card_classes} rounded-lg p-4 shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1{' relative' if chips or nota else ''}">
                                    <div class="flex items-center mb-2">
                                        <div
                                            class="{numero_bg} {numero_text} rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold mr-3">
                                            {numero}</div>
                                        <h4 class="font-bold {title_color}">{titulo}</h4>'''
    
    # Adicionar chips se houver
    if chips:
        html += '''
                                        <div class="ml-auto relative">'''
        for chip in chips:
            # Definir cor do chip
            if chip == 'VINCULANTE':
                chip_color = 'bg-yellow-400 text-gray-900'
            elif chip == 'ALTERADA':
                chip_color = 'bg-blue-500 text-white'
            elif 'SUPERADA' in chip:
                chip_color = 'bg-orange-500 text-white'
            else:
                chip_color = 'bg-gray-500 text-white'
            
            html += f'''
                                            <div
                                                class="{chip_color} px-3 py-1 rounded-full text-xs font-bold flex items-center justify-center whitespace-nowrap">
                                                {chip}</div>'''
        html += '''
                                        </div>'''
    
    html += f'''
                                    </div>
                                    <p class="text-sm {text_color} italic text-justify">{texto}</p>'''
    
    # Adicionar modulação de efeitos se houver (cor mais escura que comentário)
    if modulacao_efeitos:
        modulacao_formatada = modulacao_efeitos.replace('\n', '<br>')
        html += f'''
                                    <p class="text-xs bg-{cor}-100 p-2 rounded border-l-2 border-{cor}-400 mt-2 text-justify"><strong>Modulação de efeitos:</strong> {modulacao_formatada}</p>'''
    
    # Adicionar nota se houver
    if nota:
        nota_formatada = nota.replace('\n', '<br>')
        html += f'''
                                    <p class="text-xs bg-{cor}-50 p-2 rounded border-l-2 border-{cor}-300 mt-2 text-justify">{nota_formatada}</p>'''
    
    html += '''
                                </div>
'''
    
    return html

def gerar_secao_tribunal(tribunal, sumulas):
    """Gera HTML de uma seção completa de tribunal"""
    nome_tribunal = {
        'stf': 'STF',
        'stj': 'STJ',
        'eca': 'STJ (ECA)'
    }
    
    cor_tribunal = {
        'stf': 'red',
        'stj': 'indigo',
        'eca': 'purple'
    }
    
    gradient_tribunal = {
        'stf': 'from-red-100 via-pink-50 to-rose-100',
        'stj': 'from-indigo-100 via-purple-50 to-pink-100',
        'eca': 'from-purple-100 via-pink-50 to-fuchsia-100'
    }
    
    id_tribunal = {
        'stf': 'stf',
        'stj': 'stj-penal',
        'eca': 'stj-eca'
    }
    
    nome = nome_tribunal[tribunal]
    cor = cor_tribunal[tribunal]
    gradient = gradient_tribunal[tribunal]
    tid = id_tribunal[tribunal]
    
    html = f'''
            <!-- SÚMULAS DO {nome.upper()} -->
            <div class="mt-16">
                <div class="text-center mb-6 cursor-pointer" onclick="toggleSumulas('{tid}')">
                    <h2
                        class="text-2xl font-bold text-{cor}-800 flex items-center justify-center hover:text-{cor}-600 transition-colors">
                        Súmulas do {nome}
                        <svg id="arrow-{tid}" class="w-6 h-6 ml-2 transform transition-transform duration-300"
                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M19 9l-7 7-7-7">
                            </path>
                        </svg>
                    </h2>
                    <p class="text-sm text-gray-600 mt-2">Clique para expandir/recolher</p>
                </div>

                <div id="sumulas-{tid}" class="overflow-hidden transition-all duration-500 max-h-0">
                    <div class="relative">
                        <div
                            class="absolute inset-0 bg-gradient-to-r {gradient} rounded-2xl opacity-30">
                        </div>
                        <div class="relative grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 p-6">
'''
    
    # Adicionar cards
    for sumula in sorted(sumulas, key=lambda x: x['numero']):
        html += gerar_card_sumula(sumula, tribunal)
    
    html += '''
                        </div>
                    </div>
                </div>
            </div>
'''
    
    return html

def gerar_html_completo(sumulas):
    """Gera HTML completo substituindo apenas a seção de súmulas"""
    # Ler template HTML atual
    with open('sumulas.html', 'r', encoding='utf-8') as f:
        html_atual = f.read()
    
    # Gerar HTML das súmulas
    html_sumulas = ''
    html_sumulas += gerar_secao_tribunal('stf', sumulas['stf'])
    html_sumulas += gerar_secao_tribunal('stj', sumulas['stj'])
    html_sumulas += gerar_secao_tribunal('eca', sumulas['eca'])
    
    # Substituir seção de súmulas
    import re
    pattern = r'(<!-- SÚMULAS DO STF -->.*?)(<script>)'
    html_novo = re.sub(pattern, html_sumulas + r'\n            \2', html_atual, flags=re.DOTALL)
    
    return html_novo

def salvar_html(html, arquivo='sumulas.html', backup=True):
    """Salva HTML gerando backup do original"""
    if backup and os.path.exists(arquivo):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backup/{arquivo}.backup_{timestamp}'
        os.rename(arquivo, backup_file)
        print(f'[OK] Backup criado: {backup_file}')
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'[OK] HTML gerado: {arquivo}')

if __name__ == '__main__':
    print("="*80)
    print("GERADOR DE HTML DE SUMULAS")
    print("="*80)
    print()
    
    try:
        # Carregar súmulas
        print("1. Carregando sumulas dos JSONs...")
        sumulas = carregar_sumulas()
        print(f"   [OK] STF: {len(sumulas['stf'])} sumulas")
        print(f"   [OK] STJ: {len(sumulas['stj'])} sumulas")
        print(f"   [OK] ECA: {len(sumulas['eca'])} sumulas")
        print()
        
        # Gerar HTML
        print("2. Gerando HTML...")
        html = gerar_html_completo(sumulas)
        print("   [OK] HTML gerado")
        print()
        
        # Salvar
        print("3. Salvando arquivo...")
        salvar_html(html)
        print()
        
        print("="*80)
        print("[OK] CONCLUIDO COM SUCESSO!")
        print("="*80)
        
    except Exception as erro:
        print(f"\n[ERRO]: {erro}")
        import traceback
        traceback.print_exc()
